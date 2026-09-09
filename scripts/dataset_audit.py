from pathlib import Path
from collections import Counter
from PIL import Image
import hashlib


# ============================================================
# TEXINSPECT AI - DATASET AUDIT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "raw" 

SPLITS = ["train", "valid", "test"]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def get_image_files(folder):
    """Return all supported image files."""
    return [
        file
        for file in folder.iterdir()
        if file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def calculate_file_hash(file_path):
    """Calculate MD5 hash for duplicate detection."""
    hasher = hashlib.md5()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def audit_split(split_name, class_counter, image_hashes):
    """Audit one dataset split."""

    split_path = DATASET_PATH / split_name
    images_path = split_path / "images"
    labels_path = split_path / "labels"

    print("\n" + "=" * 60)
    print(f"AUDITING: {split_name.upper()}")
    print("=" * 60)

    if not images_path.exists():
        print(f"ERROR: Images folder not found: {images_path}")
        return

    if not labels_path.exists():
        print(f"ERROR: Labels folder not found: {labels_path}")
        return

    image_files = get_image_files(images_path)

    total_images = len(image_files)
    missing_labels = []
    empty_labels = []
    corrupt_images = []
    resolutions = []

    for image_path in image_files:

        # Expected YOLO label file
        label_path = labels_path / f"{image_path.stem}.txt"

        # ----------------------------------------------------
        # CHECK MISSING LABELS
        # ----------------------------------------------------

        if not label_path.exists():
            missing_labels.append(image_path.name)

        # ----------------------------------------------------
        # CHECK EMPTY LABELS
        # ----------------------------------------------------

        elif label_path.stat().st_size == 0:
            empty_labels.append(image_path.name)

        # ----------------------------------------------------
        # READ YOLO LABELS
        # ----------------------------------------------------

        else:
            with open(label_path, "r") as file:

                for line in file:

                    parts = line.strip().split()

                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        class_counter[class_id] += 1

        # ----------------------------------------------------
        # CHECK IMAGE CORRUPTION + RESOLUTION
        # ----------------------------------------------------

        try:
            with Image.open(image_path) as image:
                image.verify()

            with Image.open(image_path) as image:
                resolutions.append(image.size)

        except Exception:
            corrupt_images.append(image_path.name)

        # ----------------------------------------------------
        # DUPLICATE DETECTION
        # ----------------------------------------------------

        try:
            file_hash = calculate_file_hash(image_path)
            image_hashes[file_hash].append(
                f"{split_name}/{image_path.name}"
            )

        except Exception:
            pass

    # ========================================================
    # PRINT SPLIT RESULTS
    # ========================================================

    print(f"\nTotal Images: {total_images}")
    print(f"Missing Labels: {len(missing_labels)}")
    print(f"Empty Labels: {len(empty_labels)}")
    print(f"Corrupt Images: {len(corrupt_images)}")

    if resolutions:

        widths = [resolution[0] for resolution in resolutions]
        heights = [resolution[1] for resolution in resolutions]

        print("\nIMAGE RESOLUTION:")

        print(f"Minimum Width: {min(widths)}")
        print(f"Maximum Width: {max(widths)}")
        print(f"Average Width: {sum(widths) / len(widths):.2f}")

        print(f"Minimum Height: {min(heights)}")
        print(f"Maximum Height: {max(heights)}")
        print(f"Average Height: {sum(heights) / len(heights):.2f}")

    if missing_labels:

        print("\nMissing Label Files:")

        for image_name in missing_labels[:10]:
            print(f"  - {image_name}")

    if empty_labels:

        print("\nEmpty Label Files:")

        for image_name in empty_labels[:10]:
            print(f"  - {image_name}")

    if corrupt_images:

        print("\nCorrupt Images:")

        for image_name in corrupt_images[:10]:
            print(f"  - {image_name}")


def main():

    print("\n" + "=" * 60)
    print("TEXINSPECT AI")
    print("PROFESSIONAL DATASET AUDIT")
    print("=" * 60)

    print(f"\nDataset Path:")
    print(DATASET_PATH)

    # --------------------------------------------------------
    # CHECK DATASET PATH
    # --------------------------------------------------------

    if not DATASET_PATH.exists():

        print("\nERROR: Dataset folder not found.")
        print("Please check DATASET_PATH.")

        return

    class_counter = Counter()
    image_hashes = {}

    # Convert defaultdict behavior manually
    from collections import defaultdict

    image_hashes = defaultdict(list)

    # --------------------------------------------------------
    # AUDIT EACH SPLIT
    # --------------------------------------------------------

    for split in SPLITS:
        audit_split(
            split,
            class_counter,
            image_hashes
        )

    # ========================================================
    # CLASS DISTRIBUTION
    # ========================================================

    print("\n" + "=" * 60)
    print("CLASS DISTRIBUTION")
    print("=" * 60)

    if class_counter:

        for class_id, count in sorted(class_counter.items()):

            print(
                f"Class {class_id}: "
                f"{count} annotations"
            )

    else:

        print("No annotations found.")

    # ========================================================
    # DUPLICATE ANALYSIS
    # ========================================================

    duplicates = {
        file_hash: files
        for file_hash, files in image_hashes.items()
        if len(files) > 1
    }

    print("\n" + "=" * 60)
    print("DUPLICATE ANALYSIS")
    print("=" * 60)

    print(
        f"Duplicate Groups Found: "
        f"{len(duplicates)}"
    )

    if duplicates:

        print("\nExamples:")

        for _, files in list(duplicates.items())[:10]:

            print()

            for file_name in files:
                print(f"  - {file_name}")

    print("\n" + "=" * 60)
    print("DATASET AUDIT COMPLETED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()