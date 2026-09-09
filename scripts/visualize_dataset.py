from pathlib import Path
import random

import cv2
import matplotlib.pyplot as plt


# ============================================================
# TEXINSPECT AI - DATASET VISUAL INSPECTION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_ROOT / "data" / "raw"

CLASS_NAMES = [
    "Foreign-Body-Defect",
    "Hole-Defect",
    "Stain-Defect",
    "Thread-Defect"
]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

SPLITS = ["train", "valid", "test"]

SAMPLES_PER_SPLIT = 6


def get_image_files(images_path):
    """Return all supported image files."""
    return [
        file
        for file in images_path.iterdir()
        if file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def read_yolo_labels(label_path, image_width, image_height):
    """Read YOLO labels and convert them to pixel coordinates."""

    boxes = []

    if not label_path.exists():
        return boxes

    with open(label_path, "r") as file:
        lines = file.readlines()

    for line in lines:

        parts = line.strip().split()

        if len(parts) != 5:
            continue

        class_id = int(parts[0])

        x_center = float(parts[1]) * image_width
        y_center = float(parts[2]) * image_height
        box_width = float(parts[3]) * image_width
        box_height = float(parts[4]) * image_height

        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)

        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        boxes.append(
            (
                class_id,
                x1,
                y1,
                x2,
                y2
            )
        )

    return boxes


def draw_annotations(image, boxes):
    """Draw bounding boxes and class names."""

    annotated_image = image.copy()

    for class_id, x1, y1, x2, y2 in boxes:

        label = CLASS_NAMES[class_id]

        cv2.rectangle(
            annotated_image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            annotated_image,
            label,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    return annotated_image


def visualize_split(split_name):

    print("\n" + "=" * 60)
    print(f"VISUAL INSPECTION: {split_name.upper()}")
    print("=" * 60)

    images_path = DATASET_PATH / split_name / "images"
    labels_path = DATASET_PATH / split_name / "labels"

    image_files = get_image_files(images_path)

    if not image_files:

        print("No images found.")
        return

    sample_count = min(
        SAMPLES_PER_SPLIT,
        len(image_files)
    )

    selected_images = random.sample(
        image_files,
        sample_count
    )

    figure, axes = plt.subplots(
        2,
        3,
        figsize=(16, 10)
    )

    axes = axes.flatten()

    for axis, image_path in zip(
        axes,
        selected_images
    ):

        image = cv2.imread(str(image_path))

        if image is None:
            continue

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        height, width = image.shape[:2]

        label_path = (
            labels_path /
            f"{image_path.stem}.txt"
        )

        boxes = read_yolo_labels(
            label_path,
            width,
            height
        )

        annotated_image = draw_annotations(
            image,
            boxes
        )

        axis.imshow(annotated_image)

        if boxes:

            defect_names = list(
                {
                    CLASS_NAMES[box[0]]
                    for box in boxes
                }
            )

            title = ", ".join(defect_names)

        else:

            title = "NO ANNOTATION"

        axis.set_title(
            title,
            fontsize=10
        )

        axis.axis("off")

    plt.tight_layout()

    # --------------------------------------------------------
    # SAVE VISUAL EVIDENCE
    # --------------------------------------------------------

    output_path = (
        PROJECT_ROOT /
        "evidence" /
        f"{split_name}_visual_inspection.png"
    )

    output_path.parent.mkdir(
        exist_ok=True
    )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    print(
        f"\nEvidence saved to:\n"
        f"{output_path}"
    )

    plt.show()


def main():

    print("\n" + "=" * 60)
    print("TEXINSPECT AI")
    print("VISUAL DATASET INSPECTION")
    print("=" * 60)

    for split in SPLITS:

        visualize_split(split)

    print("\n" + "=" * 60)
    print("VISUAL INSPECTION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()