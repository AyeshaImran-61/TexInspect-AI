from pathlib import Path
import random
import csv

import cv2
import matplotlib.pyplot as plt


# ============================================================
# TEXINSPECT AI
# EMPTY LABEL INVESTIGATION
# ============================================================


# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------
# DATASET PATH
# ------------------------------------------------------------

DATASET_PATH = PROJECT_ROOT / "data" / "raw"


# ------------------------------------------------------------
# OUTPUT PATH
# ------------------------------------------------------------

OUTPUT_DIR = (
    PROJECT_ROOT
    / "evidence"
    / "empty_label_inspection"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# DATASET SPLITS
# ------------------------------------------------------------

SPLITS = {
    "train": "train",
    "valid": "valid",
    "test": "test"
}


# ------------------------------------------------------------
# IMAGE EXTENSIONS
# ------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
}


# ------------------------------------------------------------
# FIND IMAGE FILES
# ------------------------------------------------------------

def get_images(images_dir):

    images = []

    for file in images_dir.iterdir():

        if file.suffix.lower() in IMAGE_EXTENSIONS:

            images.append(file)

    return sorted(images)


# ------------------------------------------------------------
# CHECK LABEL STATUS
# ------------------------------------------------------------

def get_label_status(image_path, labels_dir):

    label_path = (
        labels_dir
        / f"{image_path.stem}.txt"
    )

    # Missing label file
    if not label_path.exists():

        return "MISSING"

    # Read label content
    content = label_path.read_text(
        encoding="utf-8"
    ).strip()

    # Empty label
    if not content:

        return "EMPTY"

    # Annotated
    return "ANNOTATED"


# ------------------------------------------------------------
# CREATE CSV REPORT
# ------------------------------------------------------------

def generate_csv_report(rows):

    csv_path = (
        OUTPUT_DIR
        / "empty_label_report.csv"
    )

    with open(
        csv_path,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "split",
                "filename",
                "label_status"
            ]
        )

        writer.writerows(rows)

    print(
        f"\nCSV report saved:"
        f"\n{csv_path}"
    )


# ------------------------------------------------------------
# VISUALIZE EMPTY LABEL IMAGES
# ------------------------------------------------------------

def visualize_empty_images(
    split_name,
    empty_images,
    sample_size=16
):

    if not empty_images:

        print(
            f"\nNo empty-label images found "
            f"for {split_name}"
        )

        return


    # Select sample
    sample_count = min(
        sample_size,
        len(empty_images)
    )

    selected_images = random.sample(
        empty_images,
        sample_count
    )


    # Grid settings
    columns = 4

    rows = (
        sample_count + columns - 1
    ) // columns


    fig, axes = plt.subplots(
        rows,
        columns,
        figsize=(16, rows * 4)
    )


    # Convert axes to flat list
    axes = axes.flatten()


    for index, image_path in enumerate(
        selected_images
    ):

        image = cv2.imread(
            str(image_path)
        )

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        axes[index].imshow(image)

        axes[index].set_title(
            image_path.name,
            fontsize=9
        )

        axes[index].axis("off")


    # Hide unused cells
    for index in range(
        sample_count,
        len(axes)
    ):

        axes[index].axis("off")


    plt.suptitle(
        f"TexInspect AI — "
        f"{split_name.upper()} "
        f"EMPTY LABEL INSPECTION",
        fontsize=16,
        fontweight="bold"
    )


    plt.tight_layout()


    output_path = (
        OUTPUT_DIR
        / f"{split_name}_empty_labels.png"
    )


    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight"
    )


    plt.close()


    print(
        f"\nEvidence image saved:"
        f"\n{output_path}"
    )


# ------------------------------------------------------------
# MAIN FUNCTION
# ------------------------------------------------------------

def main():

    print("\n")
    print("=" * 65)

    print(
        "TEXINSPECT AI"
    )

    print(
        "EMPTY LABEL INVESTIGATION"
    )

    print("=" * 65)


    all_rows = []


    for split_name, folder_name in SPLITS.items():

        print("\n")
        print("-" * 65)

        print(
            f"PROCESSING SPLIT: "
            f"{split_name.upper()}"
        )

        print("-" * 65)


        split_path = (
            DATASET_PATH
            / folder_name
        )


        images_dir = (
            split_path
            / "images"
        )


        labels_dir = (
            split_path
            / "labels"
        )


        # Validate paths
        if not images_dir.exists():

            print(
                f"ERROR: Images folder not found:"
                f"\n{images_dir}"
            )

            continue


        if not labels_dir.exists():

            print(
                f"ERROR: Labels folder not found:"
                f"\n{labels_dir}"
            )

            continue


        # Get images
        images = get_images(
            images_dir
        )


        empty_images = []

        annotated_count = 0

        empty_count = 0

        missing_count = 0


        # Process each image
        for image_path in images:

            status = get_label_status(
                image_path,
                labels_dir
            )


            all_rows.append(
                [
                    split_name,
                    image_path.name,
                    status
                ]
            )


            if status == "EMPTY":

                empty_images.append(
                    image_path
                )

                empty_count += 1


            elif status == "ANNOTATED":

                annotated_count += 1


            elif status == "MISSING":

                missing_count += 1


        # Print summary
        print(
            f"Total Images: "
            f"{len(images)}"
        )

        print(
            f"Annotated Images: "
            f"{annotated_count}"
        )

        print(
            f"Empty Label Images: "
            f"{empty_count}"
        )

        print(
            f"Missing Label Files: "
            f"{missing_count}"
        )


        # Visual inspection
        visualize_empty_images(
            split_name,
            empty_images
        )


    # Create CSV report
    generate_csv_report(
        all_rows
    )


    print("\n")
    print("=" * 65)

    print(
        "EMPTY LABEL INVESTIGATION COMPLETE"
    )

    print("=" * 65)

    print(
        f"\nOutput directory:"
        f"\n{OUTPUT_DIR}"
    )


# ------------------------------------------------------------
# RUN SCRIPT
# ------------------------------------------------------------

if __name__ == "__main__":

    main()