# Drowsiness Detection System

A computer vision-based drowsiness detection system that uses YOLO (You Only Look Once) object detection to identify drowsy and awake states in real-time video streams.

## 🚀 Features

- **Real-time Detection**: Monitor drowsiness levels in live video feeds
- **YOLO-based Model**: Uses Ultralytics YOLO for accurate object detection
- **Multiple Input Sources**: Support for webcam, video files, and images
- **17-Class Detection**: Includes drowsy/awake states plus various other objects
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Webcam or video input device
- Sufficient RAM for real-time processing

### Python Dependencies
```bash
pip install -r requirements.txt
```

Key dependencies include:
- **Ultralytics** (≥8.0.0) - YOLO model framework
- **OpenCV** (≥4.8.0) - Computer vision operations
- **PyTorch** (≥2.0.0) - Deep learning framework
- **NumPy** (≥1.26.0) - Numerical computations

## 🏗️ Project Structure

```
Drowsiness-Detection/
├── data/                   # Training and validation data
├── Detect/                 # Detection scripts
│   ├── detect_real_time.py # Real-time webcam detection
│   ├── detect_video.py     # Video file detection
│   └── img_detect.py       # Image detection
├── Scripts/                # Utility and data processing scripts
│   ├── collect_img_test.py # Test image collection
│   ├── validation.py       # Data validation
│   ├── check_data.py       # Data integrity checks
│   ├── cnt_img.py          # Image counting utility
│   └── cnt_labels.py       # Label counting utility
├── Test/                   # Test data and results
├── runs/                   # Training outputs and results
├── main.ipynb              # Main Jupyter notebook
├── data.yaml               # Dataset configuration
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Drowsiness-Detection
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Real-time Detection
```bash
python Detect/detect_real_time.py
```

### 4. Test with Video File
```bash
python Detect/detect_video.py --source path/to/video.mp4
```

### 5. Analyze Single Image
```bash
python Detect/img_detect.py --source path/to/image.jpg
```

## 📊 Dataset Configuration

The system is configured for 17 classes as defined in [`data.yaml`](data.yaml):

- **Drowsiness Classes**: `awake`, `drowsy`
- **Other Objects**: `person`, `car`, `tv`, `cat`, `dog`, and various food items

## 🔧 Usage Examples

### Real-time Webcam Detection
```python
from Detect.detect_real_time import detect_drowsiness

# Start real-time drowsiness detection
detect_drowsiness()
```

### Video File Analysis
```python
from Detect.detect_video import process_video

# Process video file for drowsiness detection
process_video("input_video.mp4", "output_video.mp4")
```

### Image Analysis
```python
from Detect.img_detect import detect_image

# Analyze single image
results = detect_image("test_image.jpg")
```

## 📈 Training and Model

The project uses YOLO models trained on custom drowsiness detection datasets. Training configurations and results are stored in the `runs/` directory.

### Training Data
- **Training Images**: `data/images/`
- **Validation Images**: `data/images/`
- **Test Images**: `data/test/`

## 🛠️ Development

### Running Jupyter Notebook
```bash
jupyter notebook main.ipynb
```

### Data Validation
```bash
python Scripts/validation.py
python Scripts/check_data.py
```

### Data Statistics
```bash
python Scripts/cnt_img.py      # Count images
python Scripts/cnt_labels.py    # Count labels
```

## 📝 Notes

- The system requires a webcam for real-time detection
- Ensure sufficient lighting for optimal detection accuracy
- Model performance may vary based on hardware capabilities
- For best results, position the camera to capture clear facial features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the repository for specific licensing information.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the existing documentation
2. Review the Jupyter notebook examples
3. Open an issue in the repository
4. Check the utility scripts in the `Scripts/` folder for debugging

---

**Happy detecting! 🚀**
