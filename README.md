# Drowsiness Detection Web Application

Ứng dụng web để phát hiện trạng thái buồn ngủ (drowsiness detection) sử dụng YOLO model đã được train.

## Tính năng

- **Real-time Detection**: Phát hiện trạng thái buồn ngủ theo thời gian thực qua webcam
- **Image Upload**: Upload và phân tích ảnh tĩnh
- **Beautiful UI**: Giao diện đẹp với Bootstrap và custom CSS
- **Detection Results**: Hiển thị kết quả phát hiện với độ tin cậy
- **Responsive Design**: Tương thích với nhiều thiết bị

## Cài đặt

### 1. Kích hoạt môi trường conda

```bash
conda activate myenv
```

### 2. Cài đặt dependencies

```bash
pip install flask opencv-python ultralytics pillow numpy torch torchvision
```

### 3. Kiểm tra model

Đảm bảo file model `best.pt` có sẵn tại đường dẫn:
```
runs/train/exp2_m_20_cur_best/weights/best.pt
```

## Chạy ứng dụng

### Chạy locally

```bash
python app.py
```

Sau đó mở trình duyệt và truy cập: `http://localhost:8080`

### Chạy trên server

```bash
python app.py
```

Ứng dụng sẽ chạy trên `http://0.0.0.0:8080` và có thể truy cập từ bên ngoài.

## Cách sử dụng

### 1. Real-time Detection

1. Click nút "Start Detection" để bắt đầu
2. Cho phép truy cập webcam khi được yêu cầu
3. Model sẽ phân tích video stream và hiển thị kết quả
4. Click "Stop Detection" để dừng

### 2. Upload Image

1. Click "Choose File" để chọn ảnh
2. Click "Analyze Image" để phân tích
3. Kết quả sẽ hiển thị bên dưới

### 3. Kết quả phát hiện

- **Awake**: Trạng thái tỉnh táo (màu xanh)
- **Drowsy**: Trạng thái buồn ngủ (màu đỏ)
- Hiển thị độ tin cậy (confidence) của mỗi phát hiện

## Cấu trúc dự án

```
Drowsiness Detection/
├── app.py                 # Flask web application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS
│   └── js/
│       └── script.js     # JavaScript functionality
├── runs/train/exp2_m_20_cur_best/weights/
│   └── best.pt           # Trained YOLO model
└── data.yaml             # Model configuration
```

## API Endpoints

- `GET /`: Trang chủ
- `GET /video_feed`: Video stream với detection
- `POST /start_detection`: Bắt đầu detection
- `POST /stop_detection`: Dừng detection
- `GET /get_detection_result`: Lấy kết quả detection
- `POST /upload_image`: Upload và phân tích ảnh

## Troubleshooting

### Lỗi webcam không hoạt động
- Đảm bảo webcam được kết nối và hoạt động
- Cho phép truy cập webcam trong trình duyệt
- Kiểm tra quyền truy cập camera

### Lỗi model không load
- Kiểm tra đường dẫn model trong `app.py`
- Đảm bảo file `best.pt` tồn tại
- Kiểm tra quyền đọc file

### Lỗi port đã được sử dụng
- Trên macOS, port 5000 có thể bị chiếm bởi AirPlay Receiver
- Ứng dụng đã được cấu hình để chạy trên port 8080
- Nếu vẫn gặp lỗi, thay đổi port trong `app.py`

### Lỗi dependencies
```bash
conda activate myenv
pip install --upgrade pip
pip install flask opencv-python ultralytics pillow numpy torch torchvision
```

## Deployment

### Deploy lên Heroku

1. Tạo file `Procfile`:
```
web: python app.py
```

2. Deploy:
```bash
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku main
```

### Deploy lên VPS/Server

1. Cài đặt dependencies:
```bash
conda activate myenv
pip install flask opencv-python ultralytics pillow numpy torch torchvision
```

2. Chạy với gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

3. Sử dụng nginx làm reverse proxy (tùy chọn)

## Model Information

- **Framework**: YOLO (Ultralytics)
- **Classes**: 17 classes (bao gồm 'awake', 'drowsy')
- **Model Path**: `runs/train/exp2_m_20_cur_best/weights/best.pt`
- **Confidence Threshold**: 0.5
- **IoU Threshold**: 0.5
- **Port**: 8080 (tránh xung đột với AirPlay Receiver trên macOS)

## Environment Setup

- **Conda Environment**: myenv
- **Python Version**: 3.12
- **Key Dependencies**: Flask, OpenCV, Ultralytics, PyTorch

## License

MIT License 