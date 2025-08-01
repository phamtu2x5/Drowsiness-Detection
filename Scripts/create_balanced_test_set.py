import os
import shutil
import random
from pathlib import Path

def get_all_image_files(directory):
    """Lấy tất cả file ảnh trong thư mục và các thư mục con"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(file)
    
    return set(image_files)

def get_images_by_prefix(directory, prefix):
    """Lấy tất cả ảnh có tiền tố cụ thể trong thư mục"""
    images = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                if file.startswith(prefix):
                    images.append(file)
    return images

def create_balanced_test_set():
    """Tạo tập test cân bằng với 400 ảnh"""
    
    # Đường dẫn các thư mục
    train_data_path = "data/train_data"
    images_path = "data/images"
    test_data_path = "data/test"
    
    # Tạo thư mục test nếu chưa tồn tại
    os.makedirs(test_data_path, exist_ok=True)
    os.makedirs(os.path.join(test_data_path, "images"), exist_ok=True)
    
    # Lấy danh sách ảnh đã có trong thư mục images
    existing_images = get_all_image_files(images_path)
    print(f"Số ảnh đã có trong thư mục images: {len(existing_images)}")
    
    # Các tiền tố cần lấy
    prefixes = ['001', '002', '005', '006']
    
    # Lưu trữ ảnh được chọn
    selected_images = []
    
    for prefix in prefixes:
        print(f"\nĐang xử lý tiền tố: {prefix}")
        
        # Lấy ảnh drowsy cho tiền tố này
        drowsy_images = get_images_by_prefix(os.path.join(train_data_path, "drowsy"), prefix)
        drowsy_available = [img for img in drowsy_images if img not in existing_images]
        
        # Lấy ảnh notdrowsy cho tiền tố này
        notdrowsy_images = get_images_by_prefix(os.path.join(train_data_path, "notdrowsy"), prefix)
        notdrowsy_available = [img for img in notdrowsy_images if img not in existing_images]
        
        print(f"  - Drowsy có sẵn: {len(drowsy_available)}")
        print(f"  - Notdrowsy có sẵn: {len(notdrowsy_available)}")
        
        # Chọn 50 ảnh drowsy và 50 ảnh notdrowsy cho tiền tố này
        if len(drowsy_available) >= 50:
            selected_drowsy = random.sample(drowsy_available, 50)
        else:
            selected_drowsy = drowsy_available
            print(f"  ⚠️  Chỉ có {len(drowsy_available)} ảnh drowsy cho tiền tố {prefix}")
        
        if len(notdrowsy_available) >= 50:
            selected_notdrowsy = random.sample(notdrowsy_available, 50)
        else:
            selected_notdrowsy = notdrowsy_available
            print(f"  ⚠️  Chỉ có {len(notdrowsy_available)} ảnh notdrowsy cho tiền tố {prefix}")
        
        # Thêm vào danh sách được chọn
        for img in selected_drowsy:
            selected_images.append(("drowsy", img))
        for img in selected_notdrowsy:
            selected_images.append(("notdrowsy", img))
    
    print(f"\nTổng số ảnh sẽ được thêm vào tập test: {len(selected_images)}")
    
    # Copy ảnh vào tập test
    copied_count = 0
    for category, filename in selected_images:
        source_path = os.path.join(train_data_path, category, filename)
        dest_path = os.path.join(test_data_path, "images", filename)
        
        try:
            shutil.copy2(source_path, dest_path)
            copied_count += 1
            if copied_count % 50 == 0:
                print(f"Đã copy {copied_count} ảnh...")
        except Exception as e:
            print(f"Lỗi khi copy {filename}: {e}")
    
    print(f"\nTổng kết:")
    print(f"- Đã copy {copied_count} ảnh vào tập test")
    print(f"- Tập test được lưu tại: {test_data_path}/images")
    
    # Thống kê theo category
    drowsy_count = len([img for img in selected_images if img[0] == "drowsy"])
    notdrowsy_count = len([img for img in selected_images if img[0] == "notdrowsy"])
    
    print(f"- Drowsy: {drowsy_count} ảnh")
    print(f"- Not drowsy: {notdrowsy_count} ảnh")
    
    # Thống kê theo tiền tố
    for prefix in prefixes:
        prefix_drowsy = len([img for img in selected_images if img[0] == "drowsy" and img[1].startswith(prefix)])
        prefix_notdrowsy = len([img for img in selected_images if img[0] == "notdrowsy" and img[1].startswith(prefix)])
        print(f"- Tiền tố {prefix}: {prefix_drowsy} drowsy + {prefix_notdrowsy} notdrowsy = {prefix_drowsy + prefix_notdrowsy} ảnh")

if __name__ == "__main__":
    # Set seed để có kết quả nhất quán
    random.seed(42)
    create_balanced_test_set() 