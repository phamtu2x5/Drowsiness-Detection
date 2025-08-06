import cv2
import time
from ultralytics import YOLO
import os
import glob

# Load model
model = YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')

# Input and output paths
source_path = 'data1/images'
result_path = 'Test/Result'

# Create result directory if it doesn't exist
os.makedirs(result_path, exist_ok=True)

def resize_image_manual(img_path, target_size=(640, 640)):
    # Đọc ảnh
    img = cv2.imread(img_path)
    # Resize ảnh
    resized_img = cv2.resize(img, target_size)
    return resized_img

# Get all image files from source directory
image_extensions = ['*.jpg', '*.jpeg']
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(os.path.join(source_path, ext)))
    image_files.extend(glob.glob(os.path.join(source_path, ext.upper())))

print(f"Tìm thấy {len(image_files)} ảnh trong thư mục {source_path}")

if len(image_files) == 0:
    print("Không tìm thấy ảnh nào trong thư mục source!")
    exit()

start_time = time.time()

# Process each image
for i, img_file in enumerate(image_files):
    print(f"Đang xử lý ảnh {i+1}/{len(image_files)}: {os.path.basename(img_file)}")
    
    # Process image
    results = model(img_file, conf=0.5, iou=0.5)
    
    # Get result image with bounding boxes
    results_img = results[0].plot()
    
    # Save result with original filename
    output_filename = os.path.basename(img_file)
    output_filepath = os.path.join(result_path, output_filename)
    cv2.imwrite(output_filepath, results_img)
    
    print(f"  -> Đã lưu kết quả: {output_filename}")

total_time = time.time() - start_time

print(f"\nHoàn thành!")
print(f"Tổng thời gian xử lý: {total_time:.2f} giây")
print(f"Thời gian trung bình mỗi ảnh: {total_time/len(image_files):.2f} giây")
print(f"Đã xử lý {len(image_files)} ảnh")
print(f"Kết quả được lưu trong thư mục: {result_path}")
