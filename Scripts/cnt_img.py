import os

# Đường dẫn tới thư mục chứa ảnh
folder_path = 'data/test/images'

# Các đuôi file ảnh phổ biến
image_extensions = ('.txt','.jpg')

# Đếm số file là ảnh trong thư mục
num_images = len([f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)])

print(f"Số lượng ảnh trong thư mục '{folder_path}': {num_images}")