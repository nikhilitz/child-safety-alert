# Child Safety Alert System

⚠️ **Child Safety Alert System** is a real-time computer vision application that detects children near hazardous zones—such as fire, pools, roads, or weapons—using a YOLO object detection model (Ultralytics).

This project helps enhance safety monitoring in public places, schools, homes, or any environment where child safety is critical.

---

## 🚀 Features

✅ Detects:
- Children (Class 0)
- Fire (Class 1)
- Pool (Class 2)
- Road (Class 3)
- Weapon (Class 4)

✅ Calculates overlap (IoU) between children and hazards

✅ Displays real-time alerts on video frames

✅ Works with webcam or video files

---

## 🖥 Example Alert

When a child approaches a hazard, the system overlays a red warning on the video feed, e.g.:

⚠️ ALERT: CHILD near FIRE


---

## 🛠 Installation

1. Clone this repository:

```bash
git clone https://github.com/nikhilitz/child-safety-alert.git
cd child-safety-alert
Install dependencies:
pip install -r requirements.txt
⚙️ Configuration

Open child_alert.py and check these settings:

Variable	Description	Default
WEIGHTS	Path to your YOLO model weights file	"besttop.pt"
SRC	Video source:
0 = webcam, or path to video file	0
IOU_THRESHOLD	Overlap threshold for child/hazard alert	0.01
ALERT_DURATION	How long to show alert text on the frame (in seconds)	2.0
🎥 Usage

Run the system:

python child_alert.py
Press ESC to quit.
🧠 Custom Model Training

This system uses custom YOLO classes:

Class ID	Label
0	child
1	fire
2	pool
3	road
4	weapon
To train your own model:

Prepare a dataset labeled with these classes.
Train using Ultralytics YOLO:
from ultralytics import YOLO

model = YOLO('yolov8n.pt')   # or another YOLO architecture
model.train(data='data.yaml', epochs=100, imgsz=640)
model.export(format='pt')
Replace besttop.pt in this repo with your fine-tuned weights.

📂 Repository Structure

child-safety-alert/
├── child_alert.py
├── besttop.pt
├── requirements.txt
├── README.md
├── .gitignore