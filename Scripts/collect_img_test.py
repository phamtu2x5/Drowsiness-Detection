import uuid
import time
import os
import cv2

IMAGE_PATH=os.path.join('Datatest','Images')
labels=['awake']
number_imgs=50

cap=cv2.VideoCapture(0)
# Tối ưu camera settings
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

for label in labels:
    print('Collecting images for {}'.format(label))
    time.sleep(3) 

    for img_num in range(number_imgs):
        print('Collecting images for {} number {}'.format(label,img_num))
        
        # Đọc và xử lý frame
        ret,frame=cap.read()
        if not ret:
            print("Không thể đọc frame từ camera")
            continue
            
        # Tạo tên file
        imgname=os.path.join(IMAGE_PATH,'Tu_a1'+label+'.'+str(uuid.uuid1())+'.jpg')
        
        # Ghi ảnh
        cv2.imwrite(imgname,frame)
        
        # Hiển thị ảnh
        cv2.imshow('IMAGE COLLECTION',frame)
        
        time.sleep(2)
        
        # Xử lý phím nhấn
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

cap.release()
cv2.destroyAllWindows()