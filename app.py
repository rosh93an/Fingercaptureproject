import streamlit as st
import cv2
import os
from fpdf import FPDF
from PIL import Image
from pdf2image import convert_from_bytes  # for preview

# Ensure folders exist
os.makedirs("input_images", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("FingerCapture Demo")

# Upload fingerprint
uploaded_file = st.file_uploader("Upload fingerprint", type=["jpg", "png", "jpeg"])
if uploaded_file:
    # Save uploaded file
    img_path = os.path.join("input_images", uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process image (replicate.py logic)
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

    # Display processed fingerprint
    st.image(Image.fromarray(resized), caption="Processed Fingerprint")
    st.success(f"✅ Processed and saved: {output_path}")

    # Export to PDF (pdf_export.py logic)
    if st.button("Export to PDF"):
        with st.spinner("📄 Generating PDF..."):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Loop through all processed images
            for img_name in os.listdir("processed"):
                if img_name.lower().endswith((".jpg", ".png", ".jpeg")):
                    pdf.add_page()
                    pdf.image(os.path.join("processed", img_name), x=10, y=10, w=100)

            # Save PDF to memory
            pdf_bytes = pdf.output(dest="S").encode("latin1")

            # Preview first page
            try:
                images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
                st.image(images[0], caption="📄 PDF Preview (Page 1)")
            except Exception as e:
                st.warning(f"Could not render PDF preview: {e}")

            # Download button
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name="finger_scans.pdf",
                mime="application/pdf"
            )




