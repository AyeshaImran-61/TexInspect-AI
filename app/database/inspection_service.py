# --------------------------------------------------
# TexInspect AI - Inspection Persistence Service
# --------------------------------------------------

from datetime import datetime
from uuid import uuid4

from app.database.db import SessionLocal
from app.database.models import Inspection, Defect


# ==================================================
# INSPECTION ID GENERATOR
# ==================================================

def generate_inspection_id():
    """
    Generate a unique human-readable inspection ID.

    Example:
    TXI-20260908-A1B2C3
    """
    date_part = datetime.now().strftime("%Y%m%d")
    unique_part = uuid4().hex[:6].upper()

    return f"TXI-{date_part}-{unique_part}"


# ==================================================
# SAVE INSPECTION
# ==================================================

def save_inspection(
    image_name,
    image_width,
    image_height,
    confidence,
    defects,
    decision
):
    """
    Save one complete fabric inspection and all
    detected defects into the database.
    """
    db = SessionLocal()

    try:
        # --------------------------------------------------
        # Generate Inspection ID
        # --------------------------------------------------
        inspection_id = generate_inspection_id()

        # --------------------------------------------------
        # Decision Information
        # --------------------------------------------------
        if isinstance(decision, dict):
            final_decision = (
                decision.get("decision")
                or decision.get("status")
                or decision.get("result")
                or "WARNING"
            )

            decision_reason = (
                decision.get("reason")
                or decision.get("message")
                or decision.get("explanation")
                or ""
            )
        else:
            final_decision = str(decision)
            decision_reason = ""

        final_decision = str(final_decision).upper()

        # --------------------------------------------------
        # Create Inspection Record
        # --------------------------------------------------
        inspection = Inspection(
            inspection_id=inspection_id,
            image_name=image_name,
            image_width=image_width,
            image_height=image_height,
            confidence=float(confidence),
            defect_count=len(defects),
            decision=final_decision,
            decision_reason=decision_reason,
            inspected_at=datetime.utcnow()
        )

        # --------------------------------------------------
        # Add Inspection
        # --------------------------------------------------
        db.add(inspection)
        db.flush()  # Generate database primary key

        # --------------------------------------------------
        # Save Detected Defects
        # --------------------------------------------------
        for defect in defects:
            defect_type = (
                defect.get("defect_type")
                or defect.get("class_name")
                or defect.get("name")
                or defect.get("class")
                or "Unknown"
            )

            defect_confidence = (
                defect.get("confidence")
                if defect.get("confidence") is not None
                else defect.get("conf")
            )

            relative_area = (
                defect.get("relative_area")
                if defect.get("relative_area") is not None
                else defect.get("relative_area_percent")
            )

            location = defect.get("location")
            if location is not None:
                if isinstance(location, dict):
                    location = ", ".join(
                        f"{key}: {value}"
                        for key, value in location.items()
                    )
                else:
                    location = str(location)

            db_defect = Defect(
                inspection_id=inspection.id,
                defect_type=str(defect_type),
                confidence=(
                    float(defect_confidence)
                    if defect_confidence is not None
                    else None
                ),
                x1=defect.get("x1"),
                y1=defect.get("y1"),
                x2=defect.get("x2"),
                y2=defect.get("y2"),
                bbox_width=defect.get("bbox_width"),
                bbox_height=defect.get("bbox_height"),
                bbox_area=defect.get("bbox_area"),
                relative_area=relative_area,
                center_x=defect.get("center_x"),
                center_y=defect.get("center_y"),
                location=location,
                severity=(
                    str(defect.get("severity")).upper()
                    if defect.get("severity") is not None
                    else None
                )
            )

            db.add(db_defect)

        # --------------------------------------------------
        # Commit Transaction
        # --------------------------------------------------
        db.commit()
        db.refresh(inspection)

        return {
            "success": True,
            "inspection_id": inspection.inspection_id,
            "database_id": inspection.id,
            "message": "Inspection saved successfully."
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "inspection_id": None,
            "database_id": None,
            "message": f"Failed to save inspection: {str(e)}"
        }

    finally:
        db.close()


# ==================================================
# GET ALL INSPECTIONS
# ==================================================

def get_all_inspections():
    """
    Return all inspections with newest first.
    """
    db = SessionLocal()

    try:
        inspections = (
            db.query(Inspection)
            .order_by(Inspection.inspected_at.desc())
            .all()
        )
        return inspections

    finally:
        db.close()


# ==================================================
# GET SINGLE INSPECTION
# ==================================================

def get_inspection_by_id(inspection_id):
    """
    Retrieve one inspection using its
    human-readable inspection ID.
    """
    db = SessionLocal()

    try:
        inspection = (
            db.query(Inspection)
            .filter(Inspection.inspection_id == inspection_id)
            .first()
        )
        return inspection

    finally:
        db.close()


# ==================================================
# GET INSPECTION STATISTICS
# ==================================================

def get_inspection_statistics():
    """
    Calculate inspection statistics for
    History and Analytics pages.
    """
    db = SessionLocal()

    try:
        inspections = db.query(Inspection).all()

        total = len(inspections)

        passed = sum(
            1 for inspection in inspections
            if inspection.decision == "PASS"
        )

        warning = sum(
            1 for inspection in inspections
            if inspection.decision == "WARNING"
        )

        failed = sum(
            1 for inspection in inspections
            if inspection.decision == "FAIL"
        )

        total_defects = sum(
            inspection.defect_count or 0
            for inspection in inspections
        )

        pass_rate = (passed / total * 100) if total > 0 else 0

        return {
            "total_inspections": total,
            "passed": passed,
            "warning": warning,
            "failed": failed,
            "total_defects": total_defects,
            "pass_rate": round(pass_rate, 2)
        }

    finally:
        db.close()


# ==================================================
# GET DASHBOARD STATISTICS (REFACTORED WITH ORM)
# ==================================================

def get_dashboard_statistics():
    """
    Retrieve statistics tailored for the home dashboard using SQLAlchemy.
    """
    db = SessionLocal()

    try:
        total_inspections = db.query(Inspection).count()
        
        passed_inspections = (
            db.query(Inspection)
            .filter(Inspection.decision == "PASS")
            .count()
        )

        warning_inspections = (
            db.query(Inspection)
            .filter(Inspection.decision == "WARNING")
            .count()
        )

        failed_inspections = (
            db.query(Inspection)
            .filter(Inspection.decision == "FAIL")
            .count()
        )

        total_defects = db.query(Defect).count()

        pass_rate = (
            round((passed_inspections / total_inspections) * 100, 2)
            if total_inspections > 0
            else 0.0
        )

        return {
            "success": True,
            "total_inspections": total_inspections,
            "passed_inspections": passed_inspections,
            "warning_inspections": warning_inspections,
            "failed_inspections": failed_inspections,
            "total_defects": total_defects,
            "pass_rate": pass_rate
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "total_inspections": 0,
            "passed_inspections": 0,
            "warning_inspections": 0,
            "failed_inspections": 0,
            "total_defects": 0,
            "pass_rate": 0.0
        }

    finally:
        db.close()