# Hệ Thống Phát Hiện Buồn Ngủ

Hệ thống phát hiện buồn ngủ real-time sử dụng YOLOv8 và Deep Learning.

## 📖 Tổng Quan

### Mục Tiêu

Phát hiện sớm dấu hiệu buồn ngủ để cảnh báo kịp thời, giảm thiểu tai nạn giao thông và tai nạn lao động.

### Ứng Dụng

- 🚗 Cảnh báo tài xế khi lái xe
- 🏭 Giám sát công nhân vận hành máy móc
- 🚛 Theo dõi tài xế đường dài

---

## 🎯 Phương Án Kỹ Thuật

### Kiến Trúc Hệ Thống

```
Camera → Preprocessing → YOLOv8 Model → Detection → Alert/Display
```

### Model: YOLOv8m

**Thông số:**
- Parameters: 25.8M
- Model Size: 50MB
- Input: 640x640x3
- Output: Bounding boxes + Classes (awake/drowsy)

**Tại sao chọn YOLO:**
- Real-time: 30-60 FPS (GPU)
- Độ chính xác cao: 94.27% mAP
- Single-stage: Nhanh và hiệu quả
- Dễ deploy

### Dataset

- **Tổng số**: 3,050 ảnh
  - Training: 2,439 ảnh (80%)
  - Test: 611 ảnh (20%)
- **Classes**: 2 classes (awake, drowsy)
- **Format**: YOLO format (txt)

### Training

**Hyperparameters:**
```python
epochs = 20
batch_size = 32
image_size = 640
optimizer = 'AdamW'
learning_rate = 0.001
```

**Data Augmentation:**
- Rotation: ±10°
- Translation: ±10%
- Scaling: ±20%
- Horizontal flip: 50%


**Per-class:**
- Awake: 89.0% mAP50, 80.4% mAP50-95
- Drowsy: 93.3% mAP50, 85.1% mAP50-95

### Performance

| Device | FPS | Time/Frame |
|--------|-----|------------|
| GPU (RTX 3060) | 42 FPS | 24ms |
| CPU (i7) | 8 FPS | 125ms |

---

## 🏗️ Cấu Trúc Dự Án

```
Drowsiness-Detection/
├── config.py              # Cấu hình tập trung
├── Detect/                # Detection scripts
│   ├── dtrt.py           # Real-time webcam
│   ├── detect_video.py   # Video processing
│   └── img_detect.py     # Batch images
├── Scripts/               # Utilities
├── data/                  # Dataset (images + labels)
├── runs/                  # Training results
└── main.ipynb            # Training notebook
```
---

## 🔧 Tính Năng Chính

### Đã Hoàn Thành ✅

- Real-time detection qua webcam
- Video file processing
- Batch image processing
- CUDA/CPU auto-detection
- Configuration management
- Error handling
- FPS counter và statistics

### Sắp Tới 🚧

- Alert âm thanh khi drowsy
- Tracking thời gian buồn ngủ
- Statistics dashboard
- Multi-face detection
- Web interface

---

## 📊 So Sánh Phương Pháp

| Phương pháp | Độ chính xác | Tốc độ | Robust |
|-------------|--------------|--------|--------|
| Eye Aspect Ratio | 70-80% | Rất nhanh | Thấp |
| Facial Landmarks | 75-85% | Trung bình | Trung bình |
| CNN Classification | 85-90% | Chậm | Cao |
| **YOLO (Ours)** | **94%+** | **Nhanh** | **Cao** |

---

## 💻 Yêu Cầu Hệ Thống

### Minimum
- Python 3.8+
- 4GB RAM
- Webcam
- CPU: Intel i5+

### Recommended
- Python 3.12
- 8GB RAM
- GPU: NVIDIA GTX 1660+ (6GB VRAM)
- Webcam 1080p

### Dependencies

```
torch==2.3.0
torchvision==0.18.0
ultralytics>=8.3.0
opencv-python==4.10.0.84
numpy>=1.26.0
```
---
## 📚 Tài Liệu

- **[HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md)** - Hướng dẫn chi tiết cách chạy
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start 5 phút
- **[DOCS.md](DOCS.md)** - Giải thích các files



**📘 Xem hướng dẫn sử dụng: [HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md)**
