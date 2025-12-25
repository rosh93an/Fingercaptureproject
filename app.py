import streamlit as st
import cv2
import os
from fpdf import FPDF
from PIL import Image

# Ensure folders exist
os.makedirs("input_images", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

st.title("FingerCapture Demo")

# Upload fingerprint
uploaded_file = st.file_uploader("Upload fingerprint", type=["jpg", "png", "jpeg"])
if uploaded_file:
    img_path = os.path.join("input_images", uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process image (replicate.py logic)
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.equalizeHist(gray)
    h, w = enhanced.shape
    crop = enhanced[h//4:h*3//4, w//4:w*3//4]
    resized = cv2.resize(crop, (300, 300))

    output_path = os.path.join("processed", f"processed_{uploaded_file.name}")
    cv2.imwrite(output_path, resized)

    st.image(resized, caption="Processed Fingerprint")
    st.success(f"Processed and saved: {output_path}")

    # Export to PDF (pdf_export.py logic)
    if st.button("Export to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.image(output_path, x=10, y=10, w=100)
        pdf_path = os.path.join("output", "finger_scans.pdf")
        pdf.output(pdf_path)
        st.success(f"PDF created: {pdf_path}")
