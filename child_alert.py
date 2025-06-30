import cv2
import numpy as np
import time
from ultralytics import YOLO

WEIGHTS = 'besttop.pt'             
SRC     = 0                             
IOU_THRESHOLD = 0.01                     
ALERT_DURATION = 2.0                    

model = YOLO(WEIGHTS)

HAZARD_MAP = {1: 'fire', 2: 'pool', 3: 'road', 4: 'weapon'}

alert_active = False
last_alert_time = 0
current_alert_text = ""

def compute_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA) * max(0, yB - yA)
    if interArea == 0:
        return 0.0

    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

cap = cv2.VideoCapture(SRC)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video source '{SRC}'")

print('[INFO] Press ESC to quit.')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)[0]

    child_boxes = []
    hazard_boxes = []  # (box, class_id)

    if results.boxes is not None:
        for box, cls in zip(results.boxes.xyxy.cpu().numpy(),
                            results.boxes.cls.cpu().numpy().astype(int)):
            if cls == 0:
                child_boxes.append(box)
            elif cls in HAZARD_MAP:
                hazard_boxes.append((box, cls))

    current_time = time.time()
    alert_triggered_this_frame = False

    for cbox in child_boxes:
        # Draw green box for child
        cv2.rectangle(frame, tuple(cbox[:2].astype(int)),
                      tuple(cbox[2:].astype(int)), (0, 255, 0), 2)

        for hbox, hcls in hazard_boxes:
            # Draw red box for hazard
            cv2.rectangle(frame, tuple(hbox[:2].astype(int)),
                          tuple(hbox[2:].astype(int)), (0, 0, 255), 2)

            # Check for overlap
            if compute_iou(cbox, hbox) > IOU_THRESHOLD:
                alert_triggered_this_frame = True
                last_alert_time = current_time
                current_alert_text = f'⚠️ ALERT: CHILD near {HAZARD_MAP[hcls].upper()}'

    # Show alert if within alert duration
    if current_time - last_alert_time < ALERT_DURATION:
        cv2.putText(frame, current_alert_text,
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 0, 255), 3)

    # Display frame
    cv2.imshow('Child Safety Alert System', frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
