# ⚙️ TexInspect AI — Installation Guide

This guide explains how to install and run TexInspect AI locally.

---

# System Requirements

Recommended environment:

| Requirement      | Recommended    |
| ---------------- | -------------- |
| Operating System | Windows 10/11  |
| Python           | Python 3.11    |
| RAM              | 8 GB or higher |
| Storage          | 5 GB free      |
| Processor        | Modern CPU     |
| GPU              | Optional       |

> **Recommended Python Version: Python 3.11**

---

# 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TexInspect-AI.git
```

Navigate to the project:

```bash
cd TexInspect-AI
```

---

# 2. Create a Virtual Environment

```bash
python -m venv .venv
```

---

# 3. Activate the Virtual Environment

## Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## Windows Command Prompt

```cmd
.venv\Scripts\activate
```

## Linux / macOS

```bash
source .venv/bin/activate
```

---

# 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 6. Verify Installation

Run:

```bash
python -c "import streamlit, ultralytics, torch, sqlalchemy; print('TexInspect AI dependencies installed successfully')"
```

Expected output:

```text
TexInspect AI dependencies installed successfully
```

---

# 7. Verify Model

Ensure the trained model exists:

```text
models/
└── detector/
    └── texinspect_detector_v1/
        └── best.pt
```

The application requires `best.pt` to perform AI defect detection.

---

# 8. Run the Application

From the project root:

```bash
streamlit run app/Home.py
```

Streamlit will start the application and display a local URL.

Typical URL:

```text
http://localhost:8501
```

---

# 9. Application Pages

After starting TexInspect AI, the application provides:

```text
🏠 Home

🔍 New Inspection

📁 Inspection History

📊 Quality Analytics

⚙️ Quality Rules

🧠 Model Information
```

---

# Database Setup

The application uses SQLite.

Database location:

```text
data/database/texinspect.db
```

The database is managed through SQLAlchemy.

The application stores:

* Inspections
* Detected defects
* Quality decisions
* Inspection metadata

---

# Inspection Image Storage

Inspection images are stored in:

```text
data/external/inspections/
```

Example:

```text
TXI-20260909-0BA53E/
├── original.jpg
└── annotated.jpg
```

---

# Troubleshooting

## Python Version Issue

Check Python:

```bash
python --version
```

Recommended:

```text
Python 3.11.x
```

---

## Virtual Environment Not Active

Make sure the terminal displays:

```text
(.venv)
```

before running installation commands.

---

## Model Not Found

Verify:

```text
models/detector/texinspect_detector_v1/best.pt
```

exists.

---

## Streamlit Command Not Found

Install Streamlit:

```bash
pip install streamlit
```

Then run:

```bash
python -m streamlit run app/Home.py
```

---

## Database Issues

For development testing, you can remove the local database:

```text
data/database/texinspect.db
```

Then restart the application if the database initialization logic supports automatic recreation.

> Warning: This removes all existing local inspection records.

---

# Deployment Notes

For deployment:

```text
GitHub
    │
    ▼
Streamlit Community Cloud
```

Before deployment ensure:

* `requirements.txt` is present
* `best.pt` is available to the application
* All paths are relative
* No local Windows paths are hardcoded
* Secrets are not committed
* `.venv` is excluded
* Test database files are excluded if appropriate

---

# Recommended Project Command

From the project root:

```bash
streamlit run app/Home.py
```

---

# Installation Complete

If the application opens successfully in your browser, TexInspect AI has been installed successfully.

Next, continue with:

📖 `USAGE_GUIDE.md`
