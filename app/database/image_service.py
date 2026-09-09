# ============================================================
# TexInspect AI - Inspection Image Storage Service
# ============================================================

from pathlib import Path

from PIL import Image
import numpy as np


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INSPECTIONS_DIR = (
    PROJECT_ROOT
    / "data"
    / "inspections"
)

INSPECTIONS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# GET INSPECTION DIRECTORY
# ============================================================

def get_inspection_directory(inspection_id):
    """
    Return the storage directory for one inspection.
    """

    inspection_directory = (
        INSPECTIONS_DIR
        / str(inspection_id)
    )

    inspection_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return inspection_directory


# ============================================================
# SAVE ORIGINAL IMAGE
# ============================================================

def save_original_image(
    inspection_id,
    image_bytes,
    original_filename
):
    """
    Save the original uploaded fabric image.
    """

    inspection_directory = (
        get_inspection_directory(
            inspection_id
        )
    )

    extension = (
        Path(original_filename)
        .suffix
        .lower()
    )

    if extension not in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:
        extension = ".jpg"

    original_path = (
        inspection_directory
        / f"original{extension}"
    )

    with open(
        original_path,
        "wb"
    ) as file:
        file.write(image_bytes)

    return original_path


# ============================================================
# SAVE ANNOTATED IMAGE
# ============================================================

def save_annotated_image(
    inspection_id,
    annotated_image
):
    """
    Save the AI-generated annotated image.

    Supports:
    - PIL Image
    - NumPy array
    """

    inspection_directory = (
        get_inspection_directory(
            inspection_id
        )
    )

    annotated_path = (
        inspection_directory
        / "annotated.jpg"
    )

    if annotated_image is None:
        return None

    # --------------------------------------------------------
    # PIL IMAGE
    # --------------------------------------------------------

    if isinstance(
        annotated_image,
        Image.Image
    ):

        image = annotated_image.convert(
            "RGB"
        )

        image.save(
            annotated_path,
            format="JPEG",
            quality=95
        )

        return annotated_path

    # --------------------------------------------------------
    # NUMPY IMAGE
    # --------------------------------------------------------

    if isinstance(
        annotated_image,
        np.ndarray
    ):

        image_array = annotated_image

        # Ultralytics plot() normally returns
        # an OpenCV BGR NumPy image.
        if (
            len(image_array.shape) == 3
            and image_array.shape[2] == 3
        ):

            image_array = image_array[:, :, ::-1]

        image = Image.fromarray(
            image_array.astype(np.uint8)
        )

        image.save(
            annotated_path,
            format="JPEG",
            quality=95
        )

        return annotated_path

    raise TypeError(
        "Unsupported annotated image type: "
        f"{type(annotated_image)}"
    )


# ============================================================
# SAVE BOTH INSPECTION IMAGES
# ============================================================

def save_inspection_images(
    inspection_id,
    image_bytes,
    original_filename,
    annotated_image
):
    """
    Save both original and annotated images
    for a completed inspection.
    """

    try:

        original_path = save_original_image(
            inspection_id=inspection_id,
            image_bytes=image_bytes,
            original_filename=original_filename
        )

        annotated_path = save_annotated_image(
            inspection_id=inspection_id,
            annotated_image=annotated_image
        )

        return {
            "success": True,
            "original_path": str(
                original_path
            ),
            "annotated_path": (
                str(annotated_path)
                if annotated_path
                else None
            ),
            "message": (
                "Inspection images saved successfully."
            )
        }

    except Exception as e:

        return {
            "success": False,
            "original_path": None,
            "annotated_path": None,
            "message": (
                f"Failed to save inspection images: {str(e)}"
            )
        }


# ============================================================
# GET INSPECTION IMAGE PATHS
# ============================================================

def get_inspection_image_paths(
    inspection_id
):
    """
    Return stored image paths for an inspection.
    """

    inspection_directory = (
        INSPECTIONS_DIR
        / str(inspection_id)
    )

    if not inspection_directory.exists():
        return {
            "original": None,
            "annotated": None
        }

    # --------------------------------------------------------
    # FIND ORIGINAL IMAGE
    # --------------------------------------------------------

    original_path = None

    for extension in [
        ".jpg",
        ".jpeg",
        ".png"
    ]:

        candidate = (
            inspection_directory
            / f"original{extension}"
        )

        if candidate.exists():
            original_path = candidate
            break

    # --------------------------------------------------------
    # ANNOTATED IMAGE
    # --------------------------------------------------------

    annotated_path = (
        inspection_directory
        / "annotated.jpg"
    )

    if not annotated_path.exists():
        annotated_path = None

    return {
        "original": original_path,
        "annotated": annotated_path
    }


# ============================================================
# CHECK IMAGE AVAILABILITY
# ============================================================

def inspection_images_exist(
    inspection_id
):
    """
    Check whether stored inspection images exist.
    """

    paths = get_inspection_image_paths(
        inspection_id
    )

    return (
        paths["original"] is not None
        or paths["annotated"] is not None
    )