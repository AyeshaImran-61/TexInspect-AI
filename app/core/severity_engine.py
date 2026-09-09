# --------------------------------------------------
# TexInspect AI - Severity Engine
# --------------------------------------------------

def calculate_severity(defect):
    """
    Calculate severity based on defect size.

    These are prototype QC rules and can later
    be customized for a textile company.
    """

    relative_area = defect["relative_area_percent"]

    # Size-based severity
    if relative_area >= 5:
        severity = "CRITICAL"

    elif relative_area >= 2:
        severity = "MAJOR"

    elif relative_area >= 0.5:
        severity = "MODERATE"

    else:
        severity = "MINOR"

    return severity


def apply_severity_to_defects(defects):
    """
    Add severity to all analyzed defects.
    """

    results = []

    for defect in defects:

        defect["severity"] = calculate_severity(defect)

        results.append(defect)

    return results