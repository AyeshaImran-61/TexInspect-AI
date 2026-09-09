# TexInspect AI — Official Dataset Profile

## 1. Dataset Overview

**Dataset Name:** Patterned Fabric TILDA Dataset  
**Version:** 2  
**Source:** Roboflow Universe  
**Project:** patterned-fabric-tilda  
**Workspace:** tilda-fabric-defect-detection-and-classification  

TexInspect AI uses the Patterned Fabric TILDA Dataset as the primary Computer Vision dataset for Version 1 of the project.

The dataset is designed for textile fabric defect detection and contains images of patterned fabrics with annotated defect regions.

---

# 2. Dataset Purpose

The dataset is used to train and evaluate the TexInspect AI defect detection system.

The primary objective is to enable an AI model to:

- Detect textile defects
- Identify defect types
- Localize defects
- Produce bounding boxes around detected defects
- Support automated fabric quality inspection

---

# 3. Dataset Classes

The dataset contains four official defect classes.

| Class ID | Defect Class |
|----------|--------------|
| 0 | Foreign-Body-Defect |
| 1 | Hole-Defect |
| 2 | Stain-Defect |
| 3 | Thread-Defect |

The official class names are preserved from the dataset metadata.

---

# 4. Dataset Size

The dataset contains a total of:

**500 images**

Dataset split:

| Split | Images |
|-------|-------:|
| Train | 400 |
| Validation | 50 |
| Test | 50 |
| **Total** | **500** |

---

# 5. Image Resolution

All dataset images have a consistent resolution:

```text
640 × 640 pixels