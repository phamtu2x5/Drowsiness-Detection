from PIL import Image
import os
import shutil
import numpy as np

input_dir = 'data/test'
output_image_dir = 'data/test_gray/images'
output_label_dir = 'data/test_gray/labels'

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

for fname in os.listdir(input_dir):
    in_path = os.path.join(input_dir, fname)

    # Trường hợp ảnh
    if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        base_name = os.path.splitext(fname)[0]
        out_img_path = os.path.join(output_image_dir, base_name + '.jpg')

        # Chuyển sang grayscale
        img = Image.open(in_path).convert('L')
        arr = np.array(img)

        # Stretch dải giá trị về 0–255
        if arr.max() > arr.min():
            arr = ((arr - arr.min()) / (arr.max() - arr.min()) * 255).astype(np.uint8)
        else:
            arr = np.zeros_like(arr, dtype=np.uint8)  # Trường hợp ảnh toàn 1 màu

        # Chuyển sang RGB
        img_rgb = Image.fromarray(arr, mode='L').convert('RGB')
        img_rgb.save(out_img_path, format='JPEG')

    # Trường hợp file nhãn .txt
    elif fname.lower().endswith('.txt'):
        out_lbl_path = os.path.join(output_label_dir, fname)
        shutil.copy2(in_path, out_lbl_path)