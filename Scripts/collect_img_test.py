import uuid
import time
import os
import cv2

IMAGE_PATH=os.path.join('data','images')
labels=['awake','drowsy']
number_imgs=20

cap=cv2.VideoCapture(0)
for label in labels:
    print('Collecting images for {}'.format(label))
    time.sleep(5)

    for img_num in range(number_imgs):
        print('Collecting images for {} number {}'.format(label,img_num))
        ret,frame=cap.read()
        imgname=os.path.join(IMAGE_PATH,label+'.'+str(uuid.uuid1())+'.jpg')
        cv2.imwrite(imgname,frame)
        cv2.imshow('IMAGE COLLECTION',frame)
        time.sleep(2)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()