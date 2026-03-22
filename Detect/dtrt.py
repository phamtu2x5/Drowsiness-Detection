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

# Mở webcam
print("📷 Đang mở webcam...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("❌ Không thể mở webcam! Kiểm tra camera của bạn.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)

print("🎥 Webcam đã sẵn sàng!")
print("📌 Nhấn 'q' để thoát\n")
print("=" * 50)

# FPS counter
fps_start_time = time.time()
fps_frame_count = 0
fps_display = 0

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("⚠️  Không đọc được frame từ webcam")
            break
        
        # Inference với device đã set
        results = model(frame, conf=config.CONF_THRESHOLD, iou=config.IOU_THRESHOLD, device=device)
        results_img = results[0].plot()
        
        # Tính FPS
        fps_frame_count += 1
        if fps_frame_count >= 10:
            fps_end_time = time.time()
            fps_display = fps_frame_count / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
            fps_frame_count = 0
        
        # Hiển thị FPS và device trên frame
        cv2.putText(results_img, f"FPS: {fps_display:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(results_img, f"Device: {device.upper()}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow('Drowsiness Detection', results_img)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("\n👋 Đang thoát...")
            break

except KeyboardInterrupt:
    print("\n⚠️  Đã dừng bởi người dùng (Ctrl+C)")
except Exception as e:
    print(f"\n❌ Lỗi: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Đã đóng webcam và cửa sổ")