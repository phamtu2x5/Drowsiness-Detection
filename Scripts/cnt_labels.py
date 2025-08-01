import os

label_dir = 'data/test/labels'  
awake_count = 0
drowsy_count = 0

for filename in os.listdir(label_dir):
    if not filename.endswith('.txt'):
        continue
    file_path = os.path.join(label_dir, filename)
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip() == '':
                continue
            class_id = line.strip().split()[0]
            if class_id == '15':
                awake_count += 1
            elif class_id == '16':
                drowsy_count += 1

print(f"Số nhãn awake (class 15): {awake_count}")
print(f"Số nhãn drowsy (class 16): {drowsy_count}")