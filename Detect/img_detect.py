import matplotlib.pyplot as plt
import cv2
from ultralytics import YOLO

model = YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')

img_path = 'data/images/001_glasses_nonsleepyCombination_0_notdrowsy copy.jpg'

def resize_image_manual(img_path, target_size=(640, 640)):
    # Đọc ảnh
    img = cv2.imread(img_path)
    # Resize ảnh
    resized_img = cv2.resize(img, target_size)
    return resized_img

resized_img = resize_image_manual(img_path, (640, 640))
results = model(resized_img)

# Hiển thị kết quả
results_img = results[0].plot()
results_img_rgb = cv2.cvtColor(results_img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 8))
plt.imshow(results_img)
plt.title('Drowsiness Detection (Manual Resize: 640x640)')
plt.axis('off')
plt.show()
