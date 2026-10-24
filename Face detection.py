import time
from collections import Counter, deque

import cv2
from ultralytics import YOLO

MODEL = "best.pt"
CAMERA_INDEX = 0
IMGSZ = 416
START_CONF = 0.45     
KEEP_CONF = 0.20      
MIN_HITS = 3          
MAX_MISSED = 8        
SMOOTH = 0.6          
VOTE_WINDOW = 10     

model = YOLO(MODEL)
tracks = {}  


def smooth_box(old, new, a=SMOOTH):
    return [a * o + (1 - a) * n for o, n in zip(old, new)]


cap = cv2.VideoCapture(CAMERA_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
prev = time.time()
fps = 0.0

while True:
    ok, frame = cap.read()
    if not ok:
        break

    res = model.track(frame, imgsz=IMGSZ, conf=KEEP_CONF, persist=True,
                      tracker="bytetrack.yaml", verbose=False)[0]

    seen = set()
    if res.boxes is not None and res.boxes.id is not None:
        for b in res.boxes:
            tid = int(b.id[0])
            conf = float(b.conf[0])
            cls = int(b.cls[0])
            box = b.xyxy[0].tolist()
            seen.add(tid)

            t = tracks.get(tid)
            if t is None:
                if conf < START_CONF:
                    continue  
                tracks[tid] = {"box": box, "votes": deque([cls], maxlen=VOTE_WINDOW),
                               "hits": 1, "missed": 0, "conf": conf}
            else:
                t["box"] = smooth_box(t["box"], box)
                t["votes"].append(cls)
                t["hits"] += 1
                t["missed"] = 0
                t["conf"] = 0.7 * t["conf"] + 0.3 * conf

    for tid in list(tracks):
        if tid not in seen:
            tracks[tid]["missed"] += 1
            if tracks[tid]["missed"] > MAX_MISSED:
                del tracks[tid]

    for tid, t in tracks.items():
        if t["hits"] < MIN_HITS:
            continue
        cls = Counter(t["votes"]).most_common(1)[0][0]
        x1, y1, x2, y2 = map(int, t["box"])
        color = (0, 255, 0) if t["missed"] == 0 else (0, 200, 255)  
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{model.names[cls]} {t['conf']:.2f}", (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    now = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev, 1e-6))
    prev = now
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Stable detection (q to quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()