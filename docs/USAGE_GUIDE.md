# 🧵 TexInspect AI — User Guide

## Intelligent Textile Quality Inspection & Defect Intelligence Platform

This guide explains how to use TexInspect AI to perform AI-powered fabric inspections, review detected defects, understand quality decisions, and analyze historical inspection data.

---

# 1. Launching the Application

Start the application from the project root:

```bash
streamlit run app/Home.py
```

Once Streamlit starts, open the displayed local URL in a web browser.

Typical address:

```text
http://localhost:8501
```

---

# 2. Application Navigation

TexInspect AI provides the following pages:

```text
🏠 Home

🔍 New Inspection

📁 Inspection History

📊 Quality Analytics

⚙️ Quality Rules

🧠 Model Information
```

Each page serves a specific part of the textile inspection workflow.

---

# 3. Home — Textile Quality Command Center

The Home page provides an overview of the inspection platform.

It provides access to:

* Inspection KPIs
* Quick actions
* Quality monitoring
* System intelligence
* AI model information

### Dashboard KPIs

The dashboard can display:

```text
Total Inspections
Pass Rate
Defects Detected
AI Model
```

These values represent the inspection activity stored by the application.

### Quick Actions

Use the available actions to access:

```text
New Inspection
Inspection History
Quality Analytics
```

---

# 4. New Inspection

The **New Inspection** page is the primary AI inspection workspace.

---

## Step 1 — Upload a Fabric Image

Upload a fabric image using the image uploader.

Supported formats:

```text
JPG
JPEG
PNG
```

For best results, use an image where:

* Fabric is clearly visible.
* Lighting is reasonably consistent.
* The image is not excessively blurred.
* Defect regions are visible.
* The fabric occupies most of the image.

---

## Step 2 — Configure Confidence

The confidence threshold controls how confident the YOLO model must be before a detection is accepted.

The available range is approximately:

```text
0.05 – 0.95
```

Default:

```text
0.25
```

### Lower Confidence

A lower threshold may produce more detections but can also increase false positives.

### Higher Confidence

A higher threshold produces more selective detections but may miss weaker defect predictions.

For normal prototype inspection:

```text
0.25
```

is a reasonable starting point.

---

# 5. Run AI Inspection

After uploading the image and selecting the confidence threshold, run the AI inspection.

The system executes:

```text
Image
  ↓
YOLO11n
  ↓
Defect Detection
  ↓
Defect Analysis
  ↓
Severity Classification
  ↓
Quality Decision
  ↓
Database Persistence
```

The inspection produces an AI-generated result.

---

# 6. Understanding AI Detection Results

The annotated inspection image displays detected defects using bounding boxes.

Each detection contains information such as:

```text
Defect Type
Confidence
Bounding Box
Location
```

Example:

```text
Thread Defect
Confidence: 0.86
Location: Center
```

---

# 7. Understanding Defect Analysis

For every detected defect, TexInspect AI calculates additional information.

### Bounding Box

Defines the detected defect region.

```text
x1
y1
x2
y2
```

### Width and Height

Represents the dimensions of the detected region.

### Area

Represents the bounding-box area.

### Relative Area

Estimates how much of the overall image is affected by the detected defect.

### Location

The system determines the approximate position of the defect within the image.

---

# 8. Understanding Severity

Every detected defect is assigned a severity level.

The available severity levels are:

| Severity | Interpretation             |
| -------- | -------------------------- |
| MINOR    | Low-impact quality issue   |
| MODERATE | Noticeable quality concern |
| MAJOR    | Significant defect         |
| CRITICAL | Severe quality issue       |

Severity is evaluated using configured quality rules and defect characteristics.

---

# 9. Understanding Quality Decisions

After evaluating detected defects, the Quality Decision Engine generates a final inspection result.

## 🟢 PASS

The inspection satisfies the configured quality conditions.

---

## 🟡 WARNING

Potential quality concerns were identified and may require review.

---

## 🔴 FAIL

Significant quality issues were detected according to the configured rules.

---

## Decision Reason

TexInspect AI also provides a decision explanation.

This allows users to understand **why** the inspection received its final result rather than relying only on a status label.

---

# 10. Inspection Information

The results page provides inspection metadata such as:

```text
Inspection ID
Model
Model Architecture
Confidence Threshold
Processing Device
Image Dimensions
Defect Classes
Inspection Timestamp
```

Example inspection ID:

```text
TXI-20260909-0BA53E
```

---

# 11. Database Persistence

After an inspection is completed, TexInspect AI stores the inspection information.

The database contains:

```text
Inspection Record
        │
        ├── Inspection Metadata
        ├── Quality Decision
        └── Defect Count
                │
                ▼
          Defect Records
```

Each detected defect is stored separately.

---

# 12. Inspection History

Open:

```text
Inspection History
```

to review previously completed inspections.

The history page can display:

```text
Inspection ID
Timestamp
Image Name
Defect Count
Confidence
Quality Decision
```

---

# 13. Searching and Filtering History

Use the available controls to locate inspections.

You can search using inspection-related information and filter records based on quality decisions.

Possible decisions:

```text
PASS
WARNING
FAIL
```

This makes it easier to investigate previous quality issues.

---

# 14. Inspection Details

Selecting an inspection provides additional information.

Details can include:

```text
Inspection ID
Image Name
Image Size
Confidence Threshold
Quality Decision
Decision Reason
Database Record ID
Total Defects
Inspection Timestamp
```

---

# 15. Reviewing Detected Defects

Inspection details provide defect-level information.

Each defect may include:

```text
Defect Type
Confidence
Location
Relative Area
Severity
Bounding Box Information
```

This allows users to understand not only the final decision but also the defects that contributed to it.

---

# 16. Inspection Images

For inspections with stored image evidence, the system can provide:

```text
Original Fabric Image
        │
        ▼
AI Annotated Inspection Image
```

The original image represents the uploaded fabric.

The annotated image represents the Computer Vision output.

---

# 17. Quality Analytics

Open:

```text
Quality Analytics
```

to analyze accumulated inspection data.

The analytics dashboard can provide:

### Inspection KPIs

```text
Total Inspections
Pass Rate
Total Defects
Average Defects per Inspection
```

---

## Decision Distribution

Shows the number of:

```text
PASS
WARNING
FAIL
```

inspections.

---

## Defect Distribution

Shows the frequency of detected defect types:

```text
Foreign Body
Hole
Stain
Thread
```

---

## Severity Distribution

Shows the number of defects categorized as:

```text
MINOR
MODERATE
MAJOR
CRITICAL
```

---

## Inspection Trends

Historical inspection activity can be visualized over time.

This can help identify changes in:

* Inspection volume
* Defect frequency
* Quality decisions

---

# 18. Quality Rules

The **Quality Rules** page provides visibility into the rules used by the quality intelligence system.

Rules help determine:

```text
Defect Severity
        ↓
Quality Decision
```

The rule-based layer provides a transparent bridge between Computer Vision predictions and business-oriented quality decisions.

---

# 19. Model Information

The **Model Information** page provides technical information about the AI model.

Current model:

```text
TexInspect Detector V1
```

Architecture:

```text
YOLO11n
```

Task:

```text
Object Detection
```

Known classes:

```text
Foreign-Body-Defect
Hole-Defect
Stain-Defect
Thread-Defect
```

---

# 20. Recommended Inspection Workflow

For consistent prototype testing, follow this sequence:

```text
1. Open Home

2. Select New Inspection

3. Upload Fabric Image

4. Set Confidence Threshold

5. Run AI Inspection

6. Review Annotated Image

7. Review Detected Defects

8. Review Severity

9. Review PASS/WARNING/FAIL

10. Confirm Inspection Saved

11. Open Inspection History

12. Review Stored Record

13. Open Quality Analytics
```

---

# 21. Interpreting AI Results Correctly

TexInspect AI is an AI-assisted inspection system.

A detection represents the model's prediction based on learned visual patterns.

Therefore:

> AI predictions should be interpreted within the context of the training dataset and configured quality rules.

A high-confidence detection does not automatically mean that a production-quality decision is universally correct.

For industrial deployment, the model should be validated against customer-specific textile materials and quality standards.

---

# 22. Best Practices

For better prototype results:

### Use Clear Images

Avoid heavily blurred or extremely dark images.

### Maintain Consistent Imaging

Use similar image conditions when comparing inspections.

### Review Confidence

If too many false detections appear, consider increasing the threshold.

If obvious defects are missed, consider evaluating a lower threshold.

### Review the Annotated Image

Always inspect the bounding boxes before interpreting the final quality decision.

### Review Severity

Check whether the assigned severity corresponds to the configured quality rules.

### Use History

Use historical inspections to identify recurring defect patterns.

---

# 23. Example Inspection Workflow

Example:

```text
Fabric Image
     │
     ▼
YOLO11n detects:
Thread Defect
Confidence: 0.86
     │
     ▼
Defect Analysis:
Relative Area calculated
Location identified
     │
     ▼
Severity:
MAJOR
     │
     ▼
Decision:
FAIL
     │
     ▼
Reason:
Significant defect detected
     │
     ▼
Inspection Saved
```

The inspection can then be reviewed from:

```text
Inspection History
```

and included in:

```text
Quality Analytics
```

---

# 24. Troubleshooting

## No Defects Detected

Possible reasons:

* Image does not contain a trained defect.
* Confidence threshold is too high.
* Image differs significantly from training data.
* Defect is visually difficult to identify.

Try evaluating the image using a lower confidence threshold.

---

## Too Many Detections

Possible reasons:

* Confidence threshold is too low.
* Fabric texture resembles a learned defect pattern.
* Image characteristics differ from the training dataset.

Try increasing the confidence threshold and review the annotated output.

---

## Application Does Not Start

Verify the virtual environment:

```bash
.venv\Scripts\activate
```

Then run:

```bash
streamlit run app/Home.py
```

---

## Model Loading Error

Verify that:

```text
models/detector/texinspect_detector_v1/best.pt
```

exists.

---

# 25. Application Screenshots

Place application screenshots inside:

```text
docs/screenshots/
```

Recommended screenshots:

```text
home_dashboard.png
new_inspection.png
inspection_results.png
inspection_history.png
quality_analytics.png
quality_rules.png
model_information.png
```

These screenshots can also be referenced from the main `README.md`.

---

# 26. Prototype Scope

TexInspect AI is currently a Computer Vision prototype.

The prototype demonstrates:

```text
AI Detection
+
Defect Intelligence
+
Severity Classification
+
Quality Decisions
+
Database Persistence
+
Inspection Analytics
```

It is not intended to replace certified industrial quality-control procedures without additional validation.

---

# 27. Production Deployment Considerations

Before using TexInspect AI in an industrial production environment, the system should be validated using:

* Customer-specific fabric types
* Production images
* Customer defect taxonomy
* Industrial imaging hardware
* Controlled lighting
* Production conveyor conditions
* Quality-control standards
* Domain expert validation

Potential production architecture:

```text
Industrial Camera
       ↓
Real-Time Inspection
       ↓
YOLO + Anomaly Detection
       ↓
Quality Intelligence
       ↓
Cloud / Enterprise Database
       ↓
Manufacturing Systems
```

---

# 28. Summary

TexInspect AI provides a complete prototype workflow for AI-assisted textile quality inspection.

The user can:

```text
Upload Fabric
      ↓
Detect Defects
      ↓
Analyze Defects
      ↓
Classify Severity
      ↓
Generate Quality Decision
      ↓
Save Inspection
      ↓
Review History
      ↓
Analyze Quality Trends
```

The platform demonstrates how Computer Vision can be integrated with explainable business logic and structured quality-management workflows.

---

## 🧵 TexInspect AI

**Intelligent Computer Vision for Textile Quality Inspection**

**Author:** Ayesha Imran
**Technology:** Python • YOLO11n • PyTorch • Streamlit • SQLAlchemy • SQLite
