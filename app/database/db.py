# --------------------------------------------------
# TexInspect AI - Database Configuration
# --------------------------------------------------

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "texinspect.db"


# --------------------------------------------------
# Database URL
# --------------------------------------------------

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# --------------------------------------------------
# SQLAlchemy Engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)


# --------------------------------------------------
# Base Model
# --------------------------------------------------

Base = declarative_base()


# --------------------------------------------------
# Session Factory
# --------------------------------------------------

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# --------------------------------------------------
# Database Initialization
# --------------------------------------------------

def init_db():
    """
    Create all database tables.
    """

    # Import models here so SQLAlchemy knows about them.
    from app.database import models

    Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# Database Session Helper
# --------------------------------------------------

def get_db():
    """
    Provide a database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()