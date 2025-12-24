import cv2
import os

# Create output folder if it doesn't exist
os.makedirs("processed", exist_ok=True)

# List of input images
input_folder = "input_images"
output_folder = "processed"
image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

# Loop through each image
for img_name in image_files:
    # Load image
    img_path = os.path.join(input_folder, img_name)
    img = cv2.imread(img_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Enhance contrast
    enhanced = cv2.equalizeHist(gray)

    # Crop center region (adjust as needed)
    h, w = enhanced.shape
    crop = enhanced[h//4:h*3//4, w//4:w*3//4]

    # Resize to 300x300
    resized = cv2.resize(crop, (300, 300))

    # Save processed image
    output_path = os.path.join(output_folder, f"processed_{img_name}")
    cv2.imwrite(output_path, resized)

    print(f"Processed and saved: {output_path}")
