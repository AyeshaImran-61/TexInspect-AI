# --------------------------------------------------
# TexInspect AI - Database Models
# --------------------------------------------------

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import relationship

from app.database.db import Base


# ==================================================
# INSPECTION MODEL
# ==================================================

class Inspection(Base):

    __tablename__ = "inspections"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # --------------------------------------------------
    # Inspection Identification
    # --------------------------------------------------

    inspection_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # Image Information
    # --------------------------------------------------

    image_name = Column(
        String(255),
        nullable=True
    )

    image_width = Column(
        Integer,
        nullable=True
    )

    image_height = Column(
        Integer,
        nullable=True
    )

    # --------------------------------------------------
    # Inspection Information
    # --------------------------------------------------

    confidence = Column(
        Float,
        nullable=True
    )

    defect_count = Column(
        Integer,
        default=0,
        nullable=False
    )

    # --------------------------------------------------
    # Quality Decision
    # --------------------------------------------------

    decision = Column(
        String(20),
        nullable=False
    )

    decision_reason = Column(
        Text,
        nullable=True
    )

    # --------------------------------------------------
    # Timestamp
    # --------------------------------------------------

    inspected_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # Relationship
    # --------------------------------------------------

    defects = relationship(
        "Defect",
        back_populates="inspection",
        cascade="all, delete-orphan"
    )


# ==================================================
# DEFECT MODEL
# ==================================================

class Defect(Base):

    __tablename__ = "defects"

    # --------------------------------------------------
    # Primary Key
    # --------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # --------------------------------------------------
    # Foreign Key
    # --------------------------------------------------

    inspection_id = Column(
        Integer,
        ForeignKey(
            "inspections.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # Defect Information
    # --------------------------------------------------

    defect_type = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=True
    )

    # --------------------------------------------------
    # Bounding Box
    # --------------------------------------------------

    x1 = Column(
        Float,
        nullable=True
    )

    y1 = Column(
        Float,
        nullable=True
    )

    x2 = Column(
        Float,
        nullable=True
    )

    y2 = Column(
        Float,
        nullable=True
    )

    # --------------------------------------------------
    # Defect Analysis
    # --------------------------------------------------

    bbox_width = Column(
        Float,
        nullable=True
    )

    bbox_height = Column(
        Float,
        nullable=True
    )

    bbox_area = Column(
        Float,
        nullable=True
    )

    relative_area = Column(
        Float,
        nullable=True
    )

    center_x = Column(
        Float,
        nullable=True
    )

    center_y = Column(
        Float,
        nullable=True
    )

    location = Column(
        String(100),
        nullable=True
    )

    # --------------------------------------------------
    # Severity
    # --------------------------------------------------

    severity = Column(
        String(20),
        nullable=True
    )

    # --------------------------------------------------
    # Relationship
    # --------------------------------------------------

    inspection = relationship(
        "Inspection",
        back_populates="defects"
    )