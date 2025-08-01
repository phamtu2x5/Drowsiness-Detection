import cv2
import time
from ultralytics import YOLO
model=YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')
cap=cv2.VideoCapture(0)
while cap.isOpened():
    ret,frame=cap.read()
    results=model(frame,conf=0.5,iou=0.5)
    results_img=results[0].plot()
    cv2.imshow('Drowsiness Detection',results_img)
    time.sleep(0.1)
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()