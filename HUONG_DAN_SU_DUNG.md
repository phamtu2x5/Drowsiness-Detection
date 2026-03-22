# 📘 Hướng Dẫn Sử Dụng

## 🚀 Cài Đặt

### Bước 1: Clone Project

```bash
cd /Users/phamvantu/Desktop/Drowsiness-Detection
```

### Bước 2: Tạo Environment

```bash
# Conda (khuyến nghị)
conda create -n drowsiness python=3.12 -y
conda activate drowsiness

# Hoặc venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### Bước 3: Cài Dependencies

```bash
pip install -r requirements.txt
```


---

## 🎬 Chạy Detection

### 1. Real-time Webcam

```bash
python Detect/dtrt.py
```

**Nhấn `q` để thoát**

**Output:**
- Cửa sổ video với bounding box
- FPS và device hiển thị trên màn hình
- Label: awake hoặc drowsy

### 2. Xử Lý Video

```bash
# Đặt video vào Test/Source/Video/test.mp4
python Detect/detect_video.py
# Kết quả: Test/Result/Video/test_detected.mp4
```

### 3. Xử Lý Ảnh

```bash
# Đặt ảnh vào Test/Source/Pictures/
python Detect/img_detect.py
# Kết quả: Test/Result/Pictures/
```
---
## ⚙️ Tùy Chỉnh
### File config.py

```python
# Thay đổi model
MODEL_PATH = 'runs/train/exp_s_20/weights/best.pt'

# Điều chỉnh độ nhạy
CONF_THRESHOLD = 0.3  # Nhạy hơn
CONF_THRESHOLD = 0.7  # Chặt chẽ hơn

# Tối ưu tốc độ video
SKIP_FRAMES = 4  # Nhanh hơn

# Camera settings
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
```
---

## 🐛 Xử Lý Lỗi

### Lỗi 1: torch/torchvision incompatible

```bash
pip uninstall torch torchvision -y
pip install torch==2.3.0 torchvision==0.18.0
```

### Lỗi 2: Cannot open webcam

**Giải pháp:**
- Đóng Zoom, Skype, FaceTime
- Kiểm tra quyền camera (System Preferences → Privacy → Camera)
- Thử camera khác: sửa `cv2.VideoCapture(1)` trong code

### Lỗi 3: Model not found

```bash
# Chạy từ đúng thư mục
cd /Users/phamvantu/Desktop/Drowsiness-Detection
python Detect/dtrt.py
```

### Lỗi 4: CUDA out of memory

```python
# Trong config.py, force CPU
def get_device():
    return 'cpu'
```

### Lỗi 5: FPS thấp

**Giải pháp:**
```python
# Trong config.py
SKIP_FRAMES = 4  # Tăng frame skipping
CAMERA_WIDTH = 640  # Giảm resolution
```

### Lỗi 6: ModuleNotFoundError

```bash
# Kiểm tra environment
conda activate drowsiness
pip install -r requirements.txt
```

---

## 💡 Tips

### Tăng Tốc Độ

```python
# config.py
SKIP_FRAMES = 4
CONF_THRESHOLD = 0.6
```

### Tăng Độ Chính Xác

- Sử dụng camera HD
- Đảm bảo ánh sáng tốt
- Giảm CONF_THRESHOLD

### Debug

```python
# Thêm logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎓 Training Model Mới

### Chuẩn Bị Data

```
data/
├── images/  # Ảnh training
└── labels/  # Labels (YOLO format)
```

### Training

```python
from ultralytics import YOLO

model = YOLO('yolov8m.pt')
model.train(
    data='data.yaml',
    epochs=20,
    imgsz=640,
    batch=32,
    device='cuda'
)
```

### Validation

```bash
python Scripts/validation.py
```

---

## 🆘 FAQ

**Q: Có thể chạy trên Raspberry Pi không?**  
A: Có, dùng YOLOv8n (model nhỏ), expect 2-5 FPS.

**Q: Làm sao cải thiện độ chính xác?**  
A: Thu thập thêm data, train thêm epochs.

**Q: Có thể detect nhiều người không?**  
A: Có, YOLO hỗ trợ multi-object detection.

**Q: Chạy offline được không?**  
A: Có, hoàn toàn offline.

---

## 📞 Hỗ Trợ

Khi báo lỗi, cung cấp:

```bash
python --version
python check_device.py
pip list | grep -E "torch|ultralytics|opencv"
```

Mở issue tại GitHub.

---

**Xem thêm: [README.md](README.md) - Tài liệu kỹ thuật**
