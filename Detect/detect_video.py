import cv2
import time
import os
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

# Open video file
video_path = os.path.join(config.TEST_SOURCE_VIDEO, "test.mp4")
print(f"🎬 Đang mở video: {video_path}")
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError(f"❌ Không thể mở video: {video_path}")

# Get video properties for output
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames_in_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"📊 Thông tin video:")
print(f"   - Resolution: {width}x{height}")
print(f"   - FPS: {fps}")
print(f"   - Total frames: {total_frames_in_video}")
print()

# Setup video writer
output_path = os.path.join(config.TEST_RESULT_VIDEO, "test_detected.mp4")
os.makedirs(config.TEST_RESULT_VIDEO, exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print(f"💾 Output sẽ được lưu tại: {output_path}")
print(f"⚙️  Đang xử lý video...\n")

start_time = time.time()
processed_frames = 0
total_frames = 0
skip_frames = config.SKIP_FRAMES
last_results_img = None
total_processing_time = 0

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        total_frames += 1
        
        # Hiển thị progress
        if total_frames % 30 == 0:
            progress = (total_frames / total_frames_in_video) * 100 if total_frames_in_video > 0 else 0
            print(f"⏳ Đang xử lý: {total_frames}/{total_frames_in_video} frames ({progress:.1f}%)")
        
        # Chỉ xử lý mỗi frame thứ skip_frames + 1
        if total_frames % (skip_frames + 1) == 0:
            # Run detection với device
            frame_start_time = time.time()
            results = model(frame, conf=config.CONF_THRESHOLD, iou=config.IOU_THRESHOLD, device=device)
            last_results_img = results[0].plot()
            frame_processing_time = time.time() - frame_start_time
            total_processing_time += frame_processing_time
            processed_frames += 1
            results_img = last_results_img
        else:
            # Sử dụng kết quả detection của frame trước đó
            if last_results_img is not None:
                results_img = last_results_img
            else:
                results_img = frame
        
        # Save frame to output video
        writer.write(results_img)

except KeyboardInterrupt:
    print("\n⚠️  Đã dừng bởi người dùng (Ctrl+C)")
except Exception as e:
    print(f"\n❌ Lỗi: {e}")
finally:
    cap.release()
    writer.release()  
    cv2.destroyAllWindows()

total_time = time.time() - start_time
read_fps = total_frames / total_time if total_time > 0 else 0
processing_fps = processed_frames / total_time if total_time > 0 else 0
avg_frame_time = total_processing_time / processed_frames if processed_frames > 0 else 0

print("\n" + "=" * 60)
print("✅ HOÀN THÀNH XỬ LÝ VIDEO")
print("=" * 60)
print(f"🖥️  Device: {device.upper()}")
print(f"⏱️  Tổng thời gian xử lý: {total_time:.2f} giây")
print(f"📊 Tổng frames: {total_frames}")
print(f"🎯 Frames đã xử lý: {processed_frames}")
print(f"📈 Đọc: {read_fps:.2f} frame/giây")
print(f"🚀 Xử lý: {processing_fps:.2f} frame/giây")
print(f"⚡ Thời gian xử lý 1 frame trung bình: {avg_frame_time*1000:.2f} ms")
print(f"💾 Output: {output_path}")
