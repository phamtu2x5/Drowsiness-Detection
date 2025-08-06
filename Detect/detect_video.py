import cv2
import time
from ultralytics import YOLO

# Load model
model = YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')

# Open video file
video_path = "Test/Source/test.mp4"  
cap = cv2.VideoCapture(video_path)

# Get video properties for output
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Setup video writer
output_path = "Test/Result/test_detected.mp4"  # Tên file output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

start_time = time.time()
processed_frames = 0
total_frames = 0
skip_frames = 3  # Bỏ qua 3 frame, chỉ xử lý frame thứ 4
last_results_img = None
total_processing_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    total_frames += 1
    
    # Chỉ xử lý mỗi frame thứ skip_frames + 1
    if total_frames % (skip_frames + 1) == 0:
        # Run detection
        frame_start_time = time.time()
        results = model(frame, conf=0.5, iou=0.5)
        last_results_img = results[0].plot()
        frame_processing_time = time.time() - frame_start_time
        total_processing_time += frame_processing_time
        processed_frames += 1
        results_img = last_results_img
    else:
        # Sử dụng kết quả detection của frame trước đó
        if last_results_img is not None:
            # Vẽ bounding box từ frame trước lên frame hiện tại
            results_img = last_results_img
        else:
            results_img = frame
    
    # Save frame to output video
    writer.write(results_img)

cap.release()
writer.release()  
cv2.destroyAllWindows()

total_time = time.time() - start_time
read_fps = total_frames / total_time if total_time > 0 else 0
processing_fps = processed_frames / total_time if total_time > 0 else 0
avg_frame_time = total_processing_time / processed_frames if processed_frames > 0 else 0

print(f"Tổng thời gian xử lý: {total_time:.2f} giây")
print(f"Đọc: {read_fps:.2f} frame/giây")
print(f"Xử lý: {processing_fps:.2f} frame/giây")
print(f"Thời gian xử lý 1 frame trung bình: {avg_frame_time*1000:.2f} ms")
