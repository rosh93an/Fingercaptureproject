from fpdf import FPDF
import os

# Folders
processed_folder = "processed"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Create PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)

# Loop through processed images
for img_name in os.listdir(processed_folder):
    if img_name.endswith((".jpg", ".png", ".jpeg")):
        pdf.add_page()
        img_path = os.path.join(processed_folder, img_name)
        pdf.image(img_path, x=10, y=10, w=100)

# Save PDF
pdf.output(os.path.join(output_folder, "finger_scans.pdf"))
print("PDF created: output/finger_scans.pdf")
