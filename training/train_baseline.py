from ultralytics import YOLO

# TexInspect Detector V1 — Baseline
model = YOLO("yolo11n.pt")

results = model.train(
    data=r"D:\projects\computer vision fellowship\TexInspect-AI\data\raw\data.yaml",
    epochs=50,
    imgsz=640,
    batch=4,
    device="cpu",
    workers=2,
    patience=10,
    cache=False,
    project="training/runs",
    name="texinspect_detector_v1_baseline",
    exist_ok=True
)

print("\nTraining completed successfully.")
print("Results saved to: training/runs/texinspect_detector_v1_baseline")