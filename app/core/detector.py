from ultralytics import YOLO
from pathlib import Path
import numpy as np


# --------------------------------------------------
# TexInspect AI - YOLO Detector
# --------------------------------------------------

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Model path
MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "detector"
    / "texinspect_detector_v1"
    / "best.pt"
)

# Official defect classes
CLASS_NAMES = {
    0: "Foreign-Body-Defect",
    1: "Hole-Defect",
    2: "Stain-Defect",
    3: "Thread-Defect",
}


class TexInspectDetector:

    def __init__(self, model_path=MODEL_PATH):
        """
        Load the trained TexInspect YOLO model.
        """

        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"Model not found at:\n{model_path}"
            )

        print("Loading TexInspect Detector V1...")

        self.model = YOLO(str(model_path))

        print("TexInspect Detector loaded successfully.")


    def inspect(
        self,
        image,
        confidence=0.25
    ):
        """
        Run defect detection on an image.

        Parameters:
            image:
                Image path, PIL image, numpy array,
                or OpenCV image.

            confidence:
                Minimum detection confidence.

        Returns:
            Dictionary containing detection results.
        """

        results = self.model.predict(
            source=image,
            conf=confidence,
            device="cpu",
            verbose=False
        )

        result = results[0]

        detections = []

        # Process detected bounding boxes
        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(box.cls[0].item())
                confidence_score = float(box.conf[0].item())

                x1, y1, x2, y2 = (
                    box.xyxy[0]
                    .cpu()
                    .numpy()
                    .tolist()
                )

                detection = {

                    "class_id": class_id,

                    "class_name": CLASS_NAMES.get(
                        class_id,
                        "Unknown"
                    ),

                    "confidence": round(
                        confidence_score,
                        4
                    ),

                    "bbox": {
                        "x1": round(x1, 2),
                        "y1": round(y1, 2),
                        "x2": round(x2, 2),
                        "y2": round(y2, 2)
                    }

                }

                detections.append(detection)

        # Get annotated image
        annotated_image = result.plot()

        return {

            "detections": detections,

            "defect_count": len(detections),

            "annotated_image": annotated_image,

            "image_width": int(result.orig_shape[1]),

            "image_height": int(result.orig_shape[0])

        }


# --------------------------------------------------
# Quick Local Test
# --------------------------------------------------

if __name__ == "__main__":

    detector = TexInspectDetector()

    print("\nDetector test successful.")
    print("Model path:")
    print(MODEL_PATH)