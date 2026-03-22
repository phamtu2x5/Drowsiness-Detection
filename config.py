"""
Configuration file for Drowsiness Detection System
"""
import os
import torch

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Model configuration
MODEL_PATH = os.path.join(PROJECT_ROOT, 'runs/train/exp_s_20 2/weights/best.pt')
DATA_YAML = os.path.join(PROJECT_ROOT, 'data.yaml')

# Detection thresholds
CONF_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5

# Camera configuration
CAMERA_WIDTH = 680
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Video processing
SKIP_FRAMES = 2  # Bỏ qua 2 frame, chỉ xử lý frame thứ 3

# Paths
TEST_SOURCE_VIDEO = os.path.join(PROJECT_ROOT, 'Test/Source/Video')
TEST_SOURCE_PICTURES = os.path.join(PROJECT_ROOT, 'Test/Source/Pictures')
TEST_RESULT_VIDEO = os.path.join(PROJECT_ROOT, 'Test/Result/Video')
TEST_RESULT_PICTURES = os.path.join(PROJECT_ROOT, 'Test/Result/Pictures')

# Device configuration
def get_device():
    """
    Tự động detect và trả về device phù hợp (cuda/cpu)
    """
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return device

def print_device_info():
    """
    In thông tin device đang sử dụng
    """
    device = get_device()
    print(f"🖥️  Đang sử dụng device: {device.upper()}")
    if device == 'cuda':
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("   ⚠️  Đang chạy trên CPU - tốc độ sẽ chậm hơn")
    return device

# Class names
CLASS_NAMES = {
    15: 'awake',
    16: 'drowsy'
}

# Alert configuration
DROWSY_ALERT_THRESHOLD = 3  # Số frame liên tiếp phát hiện drowsy trước khi cảnh báo
ALERT_SOUND_ENABLED = True
