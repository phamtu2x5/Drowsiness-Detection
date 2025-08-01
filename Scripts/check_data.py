import os

# Đường dẫn tới thư mục chứa ảnh và nhãn
img_dir = 'data/test/images'    # Thay bằng đường dẫn thực tế tới thư mục ảnh
label_dir = 'data/test/labels'  # Thay bằng đường dẫn thực tế tới thư mục nhãn

# Lấy danh sách tên file (không có đuôi mở rộng)
img_files = [os.path.splitext(f)[0] for f in os.listdir(img_dir) if f.lower().endswith(('.jpg'))]
label_files = [os.path.splitext(f)[0] for f in os.listdir(label_dir) if f.endswith('.txt')]

# Tìm các ảnh chưa có nhãn tương ứng
img_without_label = [f for f in img_files if f not in label_files]

if img_without_label:
    print("Các ảnh chưa có nhãn tương ứng:")
    for f in img_without_label:
        print(f)
else:
    print("Tất cả ảnh đều đã có nhãn tương ứng.")