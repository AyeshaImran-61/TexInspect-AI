# --------------------------------------------------
# TexInspect AI - Quality Decision Engine
# --------------------------------------------------

def make_quality_decision(defects):
    """
    Generate final PASS / WARNING / FAIL decision.
    """

    defect_count = len(defects)

    # No detected defects
    if defect_count == 0:

        return {
            "decision": "PASS",
            "reason": "No known defects were detected."
        }

    severities = [
        defect["severity"]
        for defect in defects
    ]

    # Critical defect
    if "CRITICAL" in severities:

        return {
            "decision": "FAIL",
            "reason": "Critical defect detected."
        }

    # Multiple major defects
    major_count = severities.count("MAJOR")

    if major_count >= 2:

        return {
            "decision": "FAIL",
            "reason": "Multiple major defects detected."
        }

    # One major defect
    if "MAJOR" in severities:

        return {
            "decision": "FAIL",
            "reason": "Major defect detected."
        }

    # Multiple defects
    if defect_count >= 3:

        return {
            "decision": "FAIL",
            "reason": "Multiple defects detected."
        }

    # Moderate defects
    if "MODERATE" in severities:

        return {
            "decision": "WARNING",
            "reason": "Moderate defect requires quality review."
        }

    # Minor defects
    return {
        "decision": "WARNING",
        "reason": "Minor defect detected."
    }