import cv2
import time
from ultralytics import YOLO
import os

# Load model
model = YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')

# Input image path
img_path = 'Datatest/Images/Tu_awake.0efb479e-721a-11f0-8002-5ec8661e9e52.jpg'

def resize_image_manual(img_path, target_size=(640, 640)):
    # Đọc ảnh
    img = cv2.imread(img_path)
    # Resize ảnh
    resized_img = cv2.resize(img, target_size)
    return resized_img
start_time = time.time()

# Process image
# resized_img = resize_image_manual(img_path, (640, 640))
results = model(img_path, conf=0.5, iou=0.5)

# Get result image with bounding boxes
results_img = results[0].plot()

# Save result
output_path = 'Test/Result/detected_image.jpg'
cv2.imwrite(output_path, results_img)

total_time = time.time() - start_time

print(f"Thời gian xử lý: {total_time:.2f} giây")
print(f"Ảnh đã được lưu tại: {output_path}")
