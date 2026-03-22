import cv2
import time
import os
import glob
import sys

# Thêm thư mục gốc vào path để import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from ultralytics import YOLO

# Hiển thị thông tin device
device = config.print_device_info()

# Kiểm tra model file có tồn tại không
if not os.path.exists(config.MODEL_PATH):
    raise FileNotFoundError(f"❌ Không tìm thấy model tại: {config.MODEL_PATH}")

print(f"📦 Đang load model từ: {config.MODEL_PATH}")
model = YOLO(config.MODEL_PATH)
model.to(device)
print("✅ Model đã load thành công!\n")

# Input and output paths
source_path = config.TEST_SOURCE_PICTURES
result_path = config.TEST_RESULT_PICTURES

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

print(f"📁 Tìm thấy {len(image_files)} ảnh trong thư mục {source_path}\n")

if len(image_files) == 0:
    print("❌ Không tìm thấy ảnh nào trong thư mục source!")
    exit()

start_time = time.time()

# Process each image
try:
    for i, img_file in enumerate(image_files):
        print(f"🖼️  [{i+1}/{len(image_files)}] Đang xử lý: {os.path.basename(img_file)}")
        
        # Process image với device
        img_start = time.time()
        results = model(img_file, conf=config.CONF_THRESHOLD, iou=config.IOU_THRESHOLD, device=device)
        img_time = time.time() - img_start
        
        # Get result image with bounding boxes
        results_img = results[0].plot()
        
        # Save result with original filename
        output_filename = os.path.basename(img_file)
        output_filepath = os.path.join(result_path, output_filename)
        cv2.imwrite(output_filepath, results_img)
        
        print(f"   ✅ Đã lưu kết quả: {output_filename} ({img_time*1000:.0f}ms)")

except KeyboardInterrupt:
    print("\n⚠️  Đã dừng bởi người dùng (Ctrl+C)")
except Exception as e:
    print(f"\n❌ Lỗi: {e}")

total_time = time.time() - start_time

print("\n" + "=" * 60)
print("✅ HOÀN THÀNH XỬ LÝ ẢNH")
print("=" * 60)
print(f"🖥️  Device: {device.upper()}")
print(f"⏱️  Tổng thời gian xử lý: {total_time:.2f} giây")
print(f"📊 Đã xử lý: {len(image_files)} ảnh")
print(f"⚡ Thời gian trung bình mỗi ảnh: {total_time/len(image_files):.2f} giây")
print(f"💾 Kết quả được lưu trong: {result_path}")
