from ultralytics import YOLO

model = YOLO("runs/detect/runs/detect/models/neu_det_v2/weights/best.pt")

# FP16 半精度导出（指定 GPU）
model.export(format="torchscript", half=True, device=0)
print("FP16 done -> best.torchscript")

# ONNX 跨平台导出（指定 GPU）
model.export(format="onnx", half=True, device=0)
print("ONNX done -> best.onnx")
