from ultralytics import YOLO
import json

m = YOLO("best.pt")
m.export(format="onnx", imgsz=416, opset=12)   # creates best.onnx
json.dump([m.names[i] for i in sorted(m.names)], open("classes.json", "w"))
print(m.names)