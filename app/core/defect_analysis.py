# --------------------------------------------------
# TexInspect AI - Defect Analysis Engine
# --------------------------------------------------

def get_defect_location(x_center, y_center, image_width, image_height):
    """
    Determine approximate defect location on fabric.
    """

    horizontal = (
        "Left" if x_center < image_width / 3
        else "Right" if x_center > (image_width * 2 / 3)
        else "Center"
    )

    vertical = (
        "Top" if y_center < image_height / 3
        else "Bottom" if y_center > (image_height * 2 / 3)
        else "Middle"
    )

    return f"{vertical}-{horizontal}"


def analyze_detection(detection, image_width, image_height):
    """
    Analyze one YOLO detection and calculate
    useful quality control information.
    """

    bbox = detection["bbox"]

    x1 = bbox["x1"]
    y1 = bbox["y1"]
    x2 = bbox["x2"]
    y2 = bbox["y2"]

    # Bounding box dimensions
    width = max(0, x2 - x1)
    height = max(0, y2 - y1)

    # Bounding box area
    bbox_area = width * height

    # Total image area
    image_area = image_width * image_height

    # Relative affected area
    relative_area = (
        (bbox_area / image_area) * 100
        if image_area > 0
        else 0
    )

    # Bounding box center
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2

    location = get_defect_location(
        x_center,
        y_center,
        image_width,
        image_height
    )

    return {
        "class_id": detection["class_id"],
        "class_name": detection["class_name"],
        "confidence": detection["confidence"],

        "bbox": bbox,

        "width_px": round(width, 2),
        "height_px": round(height, 2),

        "affected_area_px": round(bbox_area, 2),

        "relative_area_percent": round(
            relative_area,
            4
        ),

        "location": location
    }


def analyze_all_detections(
    detections,
    image_width,
    image_height
):
    """
    Analyze all detected defects.
    """

    analyzed_defects = []

    for detection in detections:

        analysis = analyze_detection(
            detection,
            image_width,
            image_height
        )

        analyzed_defects.append(analysis)

    return analyzed_defects