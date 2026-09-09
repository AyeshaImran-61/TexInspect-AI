# 🏗️ TexInspect AI — System Architecture

## Overview

TexInspect AI follows a modular architecture designed to separate the user interface, Computer Vision processing, quality intelligence, database services, and utility layers.

The architecture enables the application to process textile images through a structured AI inspection pipeline and persist inspection results for historical analysis.

---

# System Architecture

```text
                         USER
                           │
                           ▼
                ┌─────────────────────┐
                │  STREAMLIT FRONTEND │
                └──────────┬──────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼

       HOME         NEW INSPECTION        HISTORY
                                          
                           │
                           ▼
                ┌─────────────────────┐
                │   YOLO11n DETECTOR  │
                │    detector.py      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   DEFECT ANALYSIS   │
                │ defect_analysis.py  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   SEVERITY ENGINE   │
                │ severity_engine.py  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  DECISION ENGINE    │
                │ decision_engine.py  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ INSPECTION SERVICE  │
                │inspection_service.py│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ SQLITE + SQLALCHEMY │
                │    texinspect.db    │
                └─────────────────────┘
```

---

# AI Inspection Pipeline

```text
Fabric Image
     │
     ▼
Image Validation
     │
     ▼
YOLO11n Model
     │
     ▼
Defect Detection
     │
     ▼
Detection Results
     │
     ▼
Defect Analysis
     │
     ├── Bounding Box
     ├── Area
     ├── Relative Area
     ├── Center Point
     └── Location
     │
     ▼
Severity Classification
     │
     ├── MINOR
     ├── MODERATE
     ├── MAJOR
     └── CRITICAL
     │
     ▼
Quality Decision
     │
     ├── PASS
     ├── WARNING
     └── FAIL
     │
     ▼
Database Persistence
     │
     ▼
History + Analytics
```

---

# Application Layers

## 1. Presentation Layer

**Technology:** Streamlit

Responsible for:

* Dashboard
* Image upload
* Inspection workflow
* Inspection results
* History
* Analytics
* Quality rules
* Model information

Files:

```text
app/Home.py

app/pages/
├── 1_New_Inspection.py
├── 2_Inspection_History.py
├── 3_Quality_Analytics.py
├── 4_Quality_Rules.py
└── 5_Model_Information.py
```

---

## 2. AI Processing Layer

Responsible for Computer Vision and quality intelligence.

```text
app/core/
├── detector.py
├── defect_analysis.py
├── severity_engine.py
└── decision_engine.py
```

### Components

| Component          | Responsibility             |
| ------------------ | -------------------------- |
| TexInspectDetector | Runs YOLO11n detection     |
| Defect Analysis    | Analyzes defect geometry   |
| Severity Engine    | Assigns severity           |
| Decision Engine    | Generates quality decision |

---

## 3. Database Layer

Responsible for inspection persistence.

```text
app/database/
├── db.py
├── models.py
├── inspection_service.py
└── image_service.py
```

### Technologies

* SQLite
* SQLAlchemy ORM

Database:

```text
data/database/texinspect.db
```

---

## 4. Storage Layer

Stores inspection images.

```text
data/external/inspections/
│
└── TXI-YYYYMMDD-XXXXXX/
    ├── original.jpg
    └── annotated.jpg
```

---

# Database Architecture

```text
                    INSPECTION
                         │
                         │
                         │ 1
                         │
                         ▼
                    DEFECT
                         │
                         │ N
```

### Inspection

Stores inspection-level information:

```text
Inspection ID
Image Name
Image Dimensions
Confidence Threshold
Defect Count
Decision
Decision Reason
Timestamp
```

### Defect

Stores defect-level information:

```text
Defect Type
Confidence
Bounding Box
Width
Height
Area
Relative Area
Location
Severity
```

---

# Component Interaction

```text
Streamlit UI
     │
     ▼
TexInspectDetector
     │
     ▼
Defect Analysis
     │
     ▼
Severity Engine
     │
     ▼
Decision Engine
     │
     ▼
Inspection Service
     │
     ├──────────────► Image Service
     │
     ▼
SQLAlchemy ORM
     │
     ▼
SQLite Database
```

---

# Project Architecture

```text
TexInspect-AI
│
├── Presentation Layer
│   └── Streamlit
│
├── AI Processing Layer
│   ├── YOLO11n
│   ├── Defect Analysis
│   ├── Severity Engine
│   └── Decision Engine
│
├── Persistence Layer
│   ├── SQLAlchemy
│   ├── SQLite
│   └── Image Storage
│
└── Intelligence Layer
    ├── Quality Rules
    └── Explainable Decisions
```

---

# Architecture Principles

TexInspect AI follows:

### Modular Design

Each core responsibility is separated into independent modules.

### Separation of Concerns

UI, AI processing, database services, and utilities are separated.

### Explainable Intelligence

The system transforms raw AI predictions into understandable quality decisions.

### Extensibility

The architecture can support future additions such as:

* Anomaly detection
* Cloud databases
* REST APIs
* Industrial cameras
* Authentication
* Real-time inspection

---

# Future Architecture

```text
Industrial Camera
       │
       ▼
Real-Time Stream
       │
       ▼
AI Inspection Service
       │
       ├── YOLO Detection
       │
       ├── Anomaly Detection
       │
       └── Quality Intelligence
               │
               ▼
           Cloud API
               │
       ┌───────┴────────┐
       ▼                ▼
 Cloud Database    Manufacturing
                       Systems
```

---

## Summary

TexInspect AI combines Computer Vision, rule-based intelligence, database persistence, and interactive analytics into a modular textile quality inspection architecture.

The platform is designed as a prototype foundation that can be extended toward real-world industrial textile inspection.
