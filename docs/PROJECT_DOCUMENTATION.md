# 🧵 TexInspect AI

## Intelligent Textile Quality Inspection & Defect Intelligence Platform

---

# Project Documentation

**Project Name:** TexInspect AI
**Project Type:** Computer Vision / Artificial Intelligence Application
**Domain:** Textile Manufacturing & Quality Control
**Architecture:** YOLO11n + Streamlit + SQLAlchemy + SQLite
**Primary Language:** Python

---

# Table of Contents

1. Introduction
2. Background and Problem Statement
3. Project Objectives
4. Proposed Solution
5. System Overview
6. Technology Stack
7. System Architecture
8. Computer Vision Model
9. Dataset
10. AI Inspection Pipeline
11. Defect Analysis Engine
12. Severity Classification Engine
13. Quality Decision Engine
14. Database Architecture
15. Inspection Image Storage
16. Application Interface
17. Application Workflow
18. Project Structure
19. Testing and Validation
20. Results
21. Limitations
22. Future Enhancements
23. Conclusion

---

# 1. Introduction

Textile quality inspection is an important process in textile manufacturing. Fabric defects can affect product quality, increase material waste, and create financial losses if they are not detected early.

Traditional textile inspection often depends on manual visual examination. While experienced quality inspectors can identify many defects, manual inspection may be affected by factors such as fatigue, inconsistency, human error, and the difficulty of maintaining structured inspection records.

**TexInspect AI** is an Artificial Intelligence-powered textile quality inspection platform developed to explore how Computer Vision can support modern fabric quality control.

The platform uses a custom-trained **YOLO11n object detection model** to identify textile defects from fabric images. The raw AI predictions are then processed through multiple intelligence layers that analyze defect characteristics, classify defect severity, and generate an explainable quality decision.

The final inspection result is categorized as:

* PASS
* WARNING
* FAIL

Inspection data and defect information are stored in a database and can be reviewed through inspection history and quality analytics interfaces.

---

# 2. Background and Problem Statement

Textile manufacturers must maintain consistent product quality while inspecting large volumes of fabric.

Manual inspection introduces several challenges.

## Key Challenges

### Human Error

Defects may be missed during visual inspection.

### Inspector Fatigue

Long inspection sessions can reduce attention and consistency.

### Inconsistent Classification

Different inspectors may interpret defects differently.

### Limited Traceability

Manual inspection records may not provide structured historical data.

### Limited Analytics

Without centralized inspection data, identifying defect trends can be difficult.

---

## Problem Statement

The problem addressed by TexInspect AI is:

> How can Computer Vision and intelligent quality decision support be used to assist textile defect inspection and transform raw defect detections into structured, explainable quality information?

---

# 3. Project Objectives

The primary objective of TexInspect AI is to develop an intelligent prototype for automated textile quality inspection.

## Specific Objectives

* Detect textile defects from images using Computer Vision.
* Use a trained YOLO11n object detection model.
* Identify multiple textile defect classes.
* Generate annotated inspection images.
* Analyze defect geometry and characteristics.
* Calculate defect area and relative area.
* Determine approximate defect location.
* Classify defects by severity.
* Generate explainable quality decisions.
* Store inspection records in a database.
* Store individual defect records.
* Maintain inspection history.
* Store inspection image evidence.
* Provide quality analytics.
* Create a professional Streamlit-based user interface.

---

# 4. Proposed Solution

TexInspect AI provides an end-to-end AI inspection workflow.

```text
Fabric Image
     │
     ▼
Image Upload
     │
     ▼
YOLO11n Detection
     │
     ▼
Defect Detection
     │
     ▼
Defect Analysis
     │
     ▼
Severity Classification
     │
     ▼
Quality Decision
     │
     ▼
PASS / WARNING / FAIL
     │
     ▼
Database Persistence
     │
 ┌───┴─────────────┐
 ▼                 ▼
History         Analytics
```

The solution combines Computer Vision with rule-based intelligence and structured data persistence.

---

# 5. System Overview

TexInspect AI consists of five primary layers.

## 1. Presentation Layer

The Streamlit interface provides interaction between the user and the AI inspection system.

Users can:

* Upload fabric images.
* Configure detection confidence.
* Run AI inspections.
* Review detection results.
* Review quality decisions.
* View inspection history.
* Analyze quality data.
* Review quality rules.
* View AI model information.

---

## 2. Computer Vision Layer

The Computer Vision layer performs textile defect detection.

Technology:

```text
YOLO11n
Ultralytics
Python
```

Output:

* Defect class
* Confidence score
* Bounding box
* Detection coordinates
* Annotated image

---

## 3. Intelligence Layer

The intelligence layer processes raw detections.

Components:

```text
Defect Analysis Engine
        │
        ▼
Severity Engine
        │
        ▼
Quality Decision Engine
```

---

## 4. Persistence Layer

Inspection data is stored using:

```text
SQLite
+
SQLAlchemy ORM
```

The persistence layer manages:

* Inspection records
* Defect records
* Inspection metadata
* Inspection images

---

## 5. Analytics Layer

The analytics layer transforms stored inspection data into quality insights.

Examples include:

* Total inspections
* Pass rate
* Defect distribution
* Severity distribution
* Decision distribution
* Inspection trends
* Frequently detected defects

---

# 6. Technology Stack

| Technology  | Purpose                   |
| ----------- | ------------------------- |
| Python      | Core programming language |
| Streamlit   | Web application interface |
| YOLO11n     | Object detection model    |
| Ultralytics | YOLO framework            |
| PyTorch     | Deep learning framework   |
| Pillow      | Image processing          |
| OpenCV      | Computer Vision utilities |
| SQLAlchemy  | Database ORM              |
| SQLite      | Local database            |
| Pandas      | Data processing           |
| Plotly      | Interactive analytics     |

---

# 7. System Architecture

TexInspect AI follows a modular architecture.

```text
                         USER
                           │
                           ▼
                ┌─────────────────────┐
                │  STREAMLIT FRONTEND │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
        HOME        NEW INSPECTION       HISTORY
                           │
                           ▼
                 ┌───────────────────┐
                 │  YOLO11n DETECTOR │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  DEFECT ANALYSIS  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  SEVERITY ENGINE  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ DECISION ENGINE   │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ INSPECTION SERVICE│
                 └─────────┬─────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
              IMAGE STORAGE    DATABASE
```

---

# 8. Computer Vision Model

## TexInspect Detector V1

TexInspect AI uses a trained YOLO11n object detection model.

### Model Purpose

The model receives a fabric image and identifies known textile defects.

The model returns:

```text
Defect Type

Confidence

Bounding Box Coordinates

Detection Position

Annotated Image
```

---

## Model Location

```text
models/
└── detector/
    └── texinspect_detector_v1/
        ├── best.pt
        └── last.pt
```

The primary deployment model is:

```text
best.pt
```

---

## Why YOLO11n?

YOLO11n was selected because it provides:

* Efficient inference
* Lightweight architecture
* Object detection capability
* Suitable performance for prototype deployment
* Easy integration with Python applications

---

# 9. Dataset

The project was developed using the:

**Patterned Fabric TILDA Dataset — Version 2**

---

## Dataset Profile

| Property          | Value     |
| ----------------- | --------- |
| Total Images      | 500       |
| Image Size        | 640 × 640 |
| Training          | 400       |
| Validation        | 50        |
| Testing           | 50        |
| Classes           | 4         |
| Total Annotations | 475       |

---

## Defect Classes

### 1. Foreign Body Defect

Annotations:

```text
149
```

### 2. Hole Defect

Annotations:

```text
116
```

### 3. Stain Defect

Annotations:

```text
107
```

### 4. Thread Defect

Annotations:

```text
103
```

---

## Dataset Configuration

```yaml
nc: 4

names:
  - Foreign-Body-Defect
  - Hole-Defect
  - Stain-Defect
  - Thread-Defect
```

---

## Dataset Validation

The dataset was audited before training.

The audit included:

* Missing label checks
* Corrupt image checks
* Empty label analysis
* Duplicate detection
* Annotation distribution
* Image inspection

Results:

```text
Missing Labels: 0

Corrupt Images: 0

Duplicate Groups: 0

Empty Label Images: 100
```

Important:

> An empty YOLO label file means that no YOLO annotation is present. It does not automatically prove that the fabric image is defect-free.

Detailed dataset information is available in:

```text
docs/dataset_profile.md
```

---

# 10. AI Inspection Pipeline

The AI inspection pipeline processes each image through multiple stages.

---

## Stage 1: Image Input

The user uploads a fabric image.

Supported formats:

```text
JPG
JPEG
PNG
```

---

## Stage 2: Detection Confidence

The user can configure the detection confidence threshold.

Default:

```text
0.25
```

Available range:

```text
0.05 – 0.95
```

---

## Stage 3: YOLO Detection

The image is processed by the trained YOLO11n model.

The model generates one or more detections.

Each detection includes:

```text
Class

Confidence

Bounding Box
```

---

## Stage 4: Defect Analysis

Raw detections are processed into structured defect information.

---

## Stage 5: Severity Classification

Each defect is assigned a severity level.

---

## Stage 6: Quality Decision

The complete inspection is evaluated.

Result:

```text
PASS

WARNING

FAIL
```

---

## Stage 7: Persistence

The inspection and defect data are stored.

---

# 11. Defect Analysis Engine

File:

```text
app/core/defect_analysis.py
```

The Defect Analysis Engine transforms raw YOLO output into meaningful inspection data.

---

## Calculated Information

For each defect:

### Bounding Box

```text
x1
y1
x2
y2
```

---

### Width

```text
width = x2 - x1
```

---

### Height

```text
height = y2 - y1
```

---

### Bounding Box Area

```text
area = width × height
```

---

### Relative Area

The relative area estimates the proportion of the image affected by the defect.

Conceptually:

```text
Relative Area
=
Defect Area
────────────
Image Area
```

---

### Center Coordinates

```text
center_x

center_y
```

---

### Defect Location

The system determines an approximate defect location.

Examples:

```text
TOP LEFT

TOP CENTER

TOP RIGHT

CENTER LEFT

CENTER

CENTER RIGHT

BOTTOM LEFT

BOTTOM CENTER

BOTTOM RIGHT
```

---

# 12. Severity Classification Engine

File:

```text
app/core/severity_engine.py
```

The Severity Engine assigns an inspection severity level to every detected defect.

---

## Severity Levels

### MINOR

Low-impact defect.

---

### MODERATE

Noticeable defect that requires attention.

---

### MAJOR

Significant defect affecting quality.

---

### CRITICAL

Severe defect requiring immediate attention.

---

## Severity Factors

Severity evaluation may consider:

* Defect type
* Defect size
* Relative area
* Number of defects
* Location
* Configured quality rules

---

# 13. Quality Decision Engine

File:

```text
app/core/decision_engine.py
```

The Quality Decision Engine converts defect intelligence into a final inspection decision.

---

## PASS

The inspection passes when no significant quality issues are identified according to the configured decision rules.

---

## WARNING

The inspection receives a warning when quality concerns require attention but do not meet the failure conditions.

---

## FAIL

The inspection fails when significant quality issues are detected.

For example:

```text
MAJOR

or

CRITICAL
```

defects may contribute to a failure decision according to configured rules.

---

## Explainability

The Decision Engine generates:

```text
Decision

Decision Reason
```

Example:

```text
FAIL

Major textile defects were detected during inspection.
```

This makes the AI inspection workflow easier to understand.

---

# 14. Database Architecture

TexInspect AI uses:

```text
SQLite
+
SQLAlchemy ORM
```

---

## Database Location

```text
data/database/texinspect.db
```

---

# Inspection Entity

Each inspection represents one AI inspection process.

Typical data includes:

```text
ID

Inspection ID

Image Name

Image Width

Image Height

Confidence Threshold

Defect Count

Decision

Decision Reason

Inspection Timestamp
```

---

## Inspection ID

Example:

```text
TXI-20260909-0BA53E
```

Format:

```text
TXI
+
DATE
+
UNIQUE IDENTIFIER
```

---

# Defect Entity

Each inspection can contain multiple defect records.

Defect data includes:

```text
Defect Type

Confidence

x1

y1

x2

y2

Bounding Box Width

Bounding Box Height

Bounding Box Area

Relative Area

Center X

Center Y

Location

Severity
```

---

# Entity Relationship

```text
                  ONE
             INSPECTION
                  │
                  │
                  │
                 MANY
                  │
                  ▼
               DEFECT
```

---

# 15. Inspection Image Storage

TexInspect AI stores visual inspection evidence.

Storage location:

```text
data/external/inspections/
```

---

## Inspection Structure

```text
TXI-YYYYMMDD-XXXXXX/
│
├── original.jpg
│
└── annotated.jpg
```

---

## Original Image

Stores the original fabric image uploaded by the user.

---

## Annotated Image

Stores the AI-generated image containing:

* Bounding boxes
* Defect labels
* AI detections

---

# 16. Application Interface

TexInspect AI contains multiple application pages.

---

# Home

## Textile Quality Command Center

The dashboard provides an overview of system activity.

Features include:

```text
Total Inspections

Pass Rate

Defects Detected

AI Model
```

---

# New Inspection

The primary AI inspection workspace.

Features:

* Fabric image upload
* Confidence configuration
* AI detection
* Original image display
* Annotated image display
* Detection summary
* Quality decision
* Defect analysis
* Inspection persistence

---

# Inspection History

Provides access to stored inspections.

Features:

* Search
* Decision filtering
* Sorting
* Inspection records
* Inspection details
* Defect details
* Inspection images

---

# Quality Analytics

Provides analytical insights.

Metrics include:

```text
Total Inspections

Pass Rate

Total Defects

Average Defects Per Inspection
```

Visual analysis can include:

```text
Decision Distribution

Defect Distribution

Severity Distribution

Inspection Trends

Top Defects
```

---

# Quality Rules

Displays the configured quality intelligence and evaluation logic.

---

# Model Information

Provides details about:

```text
TexInspect Detector V1

YOLO11n

Defect Classes

Model Capabilities

System Limitations
```

---

# 17. Application Workflow

The complete user workflow is:

```text
USER
 │
 ▼

OPEN TEXINSPECT AI
 │
 ▼

NEW INSPECTION
 │
 ▼

UPLOAD FABRIC IMAGE
 │
 ▼

CONFIGURE CONFIDENCE
 │
 ▼

RUN AI INSPECTION
 │
 ▼

YOLO DETECTION
 │
 ▼

DEFECT ANALYSIS
 │
 ▼

SEVERITY CLASSIFICATION
 │
 ▼

QUALITY DECISION
 │
 ▼

SAVE INSPECTION
 │
 ├───────────────┐
 ▼               ▼

HISTORY       ANALYTICS
```

---

# 18. Project Structure

```text
TexInspect-AI/
│
├── app/
│   │
│   ├── core/
│   │   ├── decision_engine.py
│   │   ├── defect_analysis.py
│   │   ├── detector.py
│   │   └── severity_engine.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── image_service.py
│   │   ├── inspection_service.py
│   │   └── models.py
│   │
│   ├── pages/
│   │   ├── 1_New_Inspection.py
│   │   ├── 2_Inspection_History.py
│   │   ├── 3_Quality_Analytics.py
│   │   ├── 4_Quality_Rules.py
│   │   └── 5_Model_Information.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   └── image_utils.py
│   │
│   └── Home.py
│
├── data/
│   ├── database/
│   │   └── texinspect.db
│   │
│   └── external/
│       └── inspections/
│
├── docs/
│   ├── screenshots/
│   ├── ARCHITECTURE.md
│   ├── dataset_profile.md
│   ├── INSTALLATION.md
│   ├── PROJECT_DOCUMENTATION.md
│   └── USAGE_GUIDE.md
│
├── evidence/
│   └── empty_label_inspection/
│
├── models/
│   ├── anomaly/
│   ├── classifier/
│   └── detector/
│       └── texinspect_detector_v1/
│
├── scripts/
│   ├── dataset_audit.py
│   ├── investigate_empty_labels.py
│   └── visualize_dataset.py
│
├── tests/
│
└── training/
```

---

# 19. Testing and Validation

The project was developed using an iterative implementation approach.

---

## Dataset Validation

The dataset was checked for:

* Missing labels
* Corrupt images
* Duplicate images
* Empty labels
* Annotation distribution

---

## Model Validation

The trained model was tested using fabric images to verify:

* Model loading
* Image inference
* Detection generation
* Class identification
* Bounding box generation
* Annotated image generation

---

## Defect Analysis Testing

Verified:

* Bounding box extraction
* Width calculation
* Height calculation
* Area calculation
* Relative area
* Center coordinates
* Location analysis

---

## Severity Testing

Verified that detected defects pass through the severity classification process.

---

## Decision Testing

Verified generation of:

```text
PASS

WARNING

FAIL
```

decisions and associated reasons.

---

## Database Testing

The persistence layer should be verified by:

1. Running a new inspection.
2. Confirming inspection creation.
3. Confirming defect record creation.
4. Opening Inspection History.
5. Verifying inspection details.
6. Verifying defect details.

---

# 20. Results

TexInspect AI successfully demonstrates an end-to-end AI inspection workflow.

The system can:

* Receive a fabric image.
* Detect trained textile defect classes.
* Generate detection confidence.
* Generate bounding boxes.
* Create annotated images.
* Analyze defect characteristics.
* Calculate relative defect area.
* Determine defect location.
* Assign severity.
* Generate quality decisions.
* Store inspections.
* Store defects.
* Store inspection images.
* Retrieve inspection history.
* Generate quality analytics.

The project demonstrates how Computer Vision predictions can be integrated with business and quality intelligence.

---

# 21. Limitations

TexInspect AI is currently a prototype.

Current limitations include:

* Limited to four trained defect classes.
* Dependent on dataset quality and diversity.
* Image-based inspection workflow.
* Not yet validated in a production textile environment.
* Prototype quality decision rules.
* CPU processing may be slower than GPU inference.
* No real-time industrial camera integration.
* Local SQLite database architecture.
* No authentication system.

---

# 22. Future Enhancements

Potential future development includes:

---

## Real-Time Inspection

```text
Industrial Camera
       │
       ▼
Live Video Stream
       │
       ▼
AI Detection
```

---

## Conveyor Belt Integration

Integration with industrial fabric inspection systems.

---

## Additional Defect Classes

Train the system using a broader textile defect taxonomy.

---

## Anomaly Detection

Detect previously unseen defects.

---

## Cloud Database

Migrate from:

```text
SQLite
```

to:

```text
PostgreSQL
```

or another cloud database.

---

## Authentication

Add:

* User accounts
* Login
* Role-based access

---

## REST API

Create an API layer for external integration.

---

## Manufacturing Integration

Potential integration with:

* ERP systems
* MES systems
* Production monitoring platforms
* Quality management systems

---

## Predictive Quality Intelligence

Future analytics could predict:

* High-risk defect types
* Recurring quality issues
* Production trends

---

# 23. Conclusion

TexInspect AI is an end-to-end AI-powered textile quality inspection prototype that combines Computer Vision, quality intelligence, database persistence, and interactive analytics.

The platform uses a custom-trained YOLO11n model to detect known textile defects and transforms raw AI detections into meaningful inspection information.

The complete workflow includes:

```text
IMAGE
  │
  ▼
AI DETECTION
  │
  ▼
DEFECT ANALYSIS
  │
  ▼
SEVERITY CLASSIFICATION
  │
  ▼
QUALITY DECISION
  │
  ▼
DATABASE
  │
  ▼
HISTORY + ANALYTICS
```

The project demonstrates that textile inspection can move beyond simple object detection by combining AI predictions with structured analysis and explainable quality decision support.

TexInspect AI provides a foundation for future development toward real-world industrial inspection systems involving industrial cameras, real-time processing, anomaly detection, cloud infrastructure, and manufacturing integration.

---

# 👩‍💻 Author

**Ayesha Imran**

AI Engineer | AI Application Developer

Areas of Interest:

* Artificial Intelligence
* Machine Learning
* Deep Learning
* Computer Vision
* YOLO
* Intelligent Applications
* Enterprise AI Systems

---

# 📌 Project Status

```text
AI Detection Engine          READY

Defect Analysis Engine      READY

Severity Engine             READY

Decision Engine             READY

Database Persistence        READY

Image Storage               READY

Inspection History          READY

Quality Analytics           READY

Quality Rules               READY

Model Information           READY

Documentation               READY

Cloud Deployment            PLANNED
```

---

<div align="center">

## 🧵 TexInspect AI

### Intelligent Computer Vision for Textile Quality Inspection

</div>
