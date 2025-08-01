from ultralytics import YOLO
model=YOLO('runs/train/exp2_m_20_cur_best/weights/best.pt')
metrics = model.val(
    data='data.yaml',
    split='test',
    project='runs/val',
    name='val_exp3_m_30',
    )
print(metrics)