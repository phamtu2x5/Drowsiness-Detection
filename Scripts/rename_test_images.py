import os
import shutil
from pathlib import Path

def rename_test_images():
    """Đổi tên các ảnh trong tập test thành format rút gọn"""
    
    test_images_path = "data/test/images"
    
    if not os.path.exists(test_images_path):
        print("Thư mục test/images không tồn tại!")
        return
    
    # Lấy danh sách tất cả ảnh
    image_files = []
    for file in os.listdir(test_images_path):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            image_files.append(file)
    
    print(f"Tìm thấy {len(image_files)} ảnh cần đổi tên")
    
    # Tạo mapping cho việc đổi tên
    rename_mapping = {}
    prefix_counters = {
        '001': {'drowsy': 0, 'notdrowsy': 0},
        '002': {'drowsy': 0, 'notdrowsy': 0},
        '005': {'drowsy': 0, 'notdrowsy': 0},
        '006': {'drowsy': 0, 'notdrowsy': 0}
    }
    
    for filename in image_files:
        # Phân tích tên file để lấy prefix và category
        parts = filename.split('_')
        if len(parts) >= 3:
            prefix = parts[0]  # 001, 002, 005, 006
            category = 'drowsy' if '_drowsy' in filename else 'notdrowsy'
            
            if prefix in prefix_counters:
                prefix_counters[prefix][category] += 1
                counter = prefix_counters[prefix][category]
                
                # Tạo tên mới
                new_name = f"{prefix}_{category}_{counter:02d}.jpg"
                rename_mapping[filename] = new_name
    
    print(f"Sẽ đổi tên {len(rename_mapping)} ảnh")
    
    # Thực hiện đổi tên
    renamed_count = 0
    for old_name, new_name in rename_mapping.items():
        old_path = os.path.join(test_images_path, old_name)
        new_path = os.path.join(test_images_path, new_name)
        
        try:
            os.rename(old_path, new_path)
            renamed_count += 1
            if renamed_count % 50 == 0:
                print(f"Đã đổi tên {renamed_count} ảnh...")
        except Exception as e:
            print(f"Lỗi khi đổi tên {old_name}: {e}")
    
    print(f"\nHoàn thành! Đã đổi tên {renamed_count} ảnh")
    
    # Thống kê kết quả
    print("\nThống kê theo tiền tố:")
    for prefix in ['001', '002', '005', '006']:
        drowsy_count = len([f for f in os.listdir(test_images_path) 
                           if f.startswith(f"{prefix}_drowsy")])
        notdrowsy_count = len([f for f in os.listdir(test_images_path) 
                              if f.startswith(f"{prefix}_notdrowsy")])
        print(f"- {prefix}: {drowsy_count} drowsy + {notdrowsy_count} notdrowsy = {drowsy_count + notdrowsy_count} ảnh")

if __name__ == "__main__":
    rename_test_images() 