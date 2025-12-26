import streamlit as st
import cv2
import os
from fpdf import FPDF
from PIL import Image
from pdf2image import convert_from_bytes  # extra dependency

# Ensure folders exist
os.makedirs("input_images", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("FingerCapture Demo")

# Track last uploaded file in session state
if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

# Upload fingerprint
uploaded_file = st.file_uploader("Upload fingerprint", type=["jpg", "png", "jpeg"])
if uploaded_file and uploaded_file.name != st.session_state.last_uploaded:
    st.session_state.last_uploaded = uploaded_file.name

    img_path = os.path.join("input_images", uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Show spinner while processing
    with st.spinner("🔄 Processing fingerprint..."):
        img = cv2.imread(img_path)
        if img is None:
            st.error("❌ Failed to read image. Please try a different file or format.")
            st.stop()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.equalizeHist(gray)
        h, w = enhanced.shape
        crop = enhanced[h // 4:h * 3 // 4, w // 4:w * 3 // 4]
        resized = cv2.resize(crop, (300, 300))

        output_path = os.path.join("processed", f"processed_{uploaded_file.name}")
        cv2.imwrite(output_path, resized)

    # Display safely
    st.image(Image.fromarray(resized), caption="Processed Fingerprint")
    st.success(f"✅ Processed and saved: {output_path}")

    # Export to PDF
    if st.button("Export to PDF"):
        with st.spinner("📄 Generating PDF..."):
            pdf = FPDF()
            pdf.add_page()
            pdf.image(output_path, x=10, y=10, w=100)

            # Get PDF as bytes instead of saving only to disk
            pdf_bytes = pdf.output(dest="S").encode("latin1")

            # Preview first page of PDF
            try:
                images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
                st.image(images[0], caption="📄 PDF Preview (Page 1)")
            except Exception as e:
                st.warning(f"Could not render PDF preview: {e}")

            # Streamlit download button
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="finger_scans.pdf",
                mime="application/pdf"
            )

# Clear upload button
if st.button("Clear uploaded file"):
    st.session_state.last_uploaded = None
    st.experimental_rerun()


