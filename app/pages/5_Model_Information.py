import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Model Information | TexInspect AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """<style>
.stApp {
    background-color: #F8FAFC;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] > div {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.sidebar-brand {
    padding: 10px 5px 20px 5px;
}

.sidebar-brand-title {
    font-size: 24px;
    font-weight: 750;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.sidebar-brand-subtitle {
    font-size: 13px;
    color: #94A3B8;
    letter-spacing: 0.3px;
}

.sidebar-divider {
    border: none;
    border-top: 1px solid #334155;
    margin: 15px 0 20px 0;
}

.sidebar-status-title {
    font-size: 11px;
    font-weight: 700;
    color: #94A3B8;
    letter-spacing: 1.2px;
    margin-bottom: 12px;
}

.sidebar-status {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 9px 0;
    font-size: 13px;
    color: #CBD5E1;
}

.status-dot-green {
    width: 8px;
    height: 8px;
    background-color: #22C55E;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.status-dot-yellow {
    width: 8px;
    height: 8px;
    background-color: #F59E0B;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.4);
}

/* HERO */
.model-header {
    background: linear-gradient(135deg, #0F172A 0%, #162A46 55%, #1E3A5F 100%);
    padding: 34px 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.12);
    position: relative;
    overflow: hidden;
}

.model-header::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    right: -80px;
    top: -110px;
    background: rgba(37, 99, 235, 0.14);
}

.model-badge {
    display: inline-block;
    background: rgba(6, 182, 212, 0.14);
    border: 1px solid rgba(6, 182, 212, 0.30);
    color: #67E8F9;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 14px;
}

.model-header h1 {
    font-size: 36px;
    line-height: 1.15;
    margin: 0;
    font-weight: 750;
    color: #FFFFFF;
}

.model-header p {
    font-size: 15px;
    line-height: 1.6;
    margin-top: 11px;
    margin-bottom: 0;
    color: #CBD5E1;
    max-width: 800px;
}

/* SECTION TITLES */
.section-title {
    font-size: 21px;
    font-weight: 750;
    color: #0F172A;
    margin-top: 26px;
    margin-bottom: 7px;
}

.section-subtitle {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 18px;
}

/* INFORMATION CARDS */
.info-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 23px 25px;
    min-height: 145px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.info-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 9px;
}

.info-card-text {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
}

/* MODEL KPI CARDS */
.model-kpi {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    min-height: 110px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.05);
}

.model-kpi-label {
    font-size: 10px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
}

.model-kpi-value {
    font-size: 25px;
    color: #0F172A;
    font-weight: 750;
    margin-top: 9px;
}

.model-kpi-description {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 5px;
}

/* CLASS CARDS */
.class-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    min-height: 130px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.05);
}

.class-number {
    display: inline-block;
    width: 30px;
    height: 30px;
    line-height: 30px;
    text-align: center;
    border-radius: 9px;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 12px;
    font-weight: 750;
    margin-bottom: 10px;
}

.class-name {
    font-size: 15px;
    font-weight: 700;
    color: #0F172A;
}

.class-description {
    font-size: 12px;
    line-height: 1.5;
    color: #64748B;
    margin-top: 6px;
}

/* PIPELINE */
.pipeline-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 22px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.05);
}

.pipeline-step {
    padding: 13px 15px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    margin-bottom: 9px;
    font-size: 13px;
    color: #475569;
    font-weight: 600;
}

.pipeline-step:last-child {
    margin-bottom: 0;
}

.pipeline-arrow {
    text-align: center;
    color: #2563EB;
    font-size: 16px;
    margin: 2px 0;
}

/* BADGES */
.badge-blue {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 12px;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.badge-green {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 12px;
    background: #F0FDF4;
    color: #15803D;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.badge-orange {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 12px;
    background: #FFF7ED;
    color: #C2410C;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* FOOTER */
.tex-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #E2E8F0;
    text-align: center;
    color: #94A3B8;
    font-size: 11px;
}
</style>""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """<div class="sidebar-brand">
    <div class="sidebar-brand-title">🔷 TexInspect AI</div>
    <div class="sidebar-brand-subtitle">Textile Quality Intelligence</div>
</div>
<div class="sidebar-divider"></div>
<div class="sidebar-status-title">SYSTEM STATUS</div>
<div class="sidebar-status"><span class="status-dot-green"></span>AI Engine Online</div>
<div class="sidebar-status"><span class="status-dot-green"></span>Detector Available</div>
<div class="sidebar-status"><span class="status-dot-yellow"></span>Prototype Mode</div>
<div class="sidebar-divider"></div>""",
        unsafe_allow_html=True
    )

    st.caption("TexInspect AI Platform")
    st.caption("Computer Vision • Textile QC")


# ============================================================
# HERO
# ============================================================

st.markdown(
    """<div class="model-header">
    <div class="model-badge">COMPUTER VISION MODEL</div>
    <h1>TexInspect Detector V1</h1>
    <p>YOLO11n-based textile defect detection model used by TexInspect AI to identify and localize known fabric quality defects.</p>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# MODEL OVERVIEW
# ============================================================

st.markdown(
    """<div class="section-title">Model Overview</div>
<div class="section-subtitle">Core technical configuration of the current TexInspect AI inspection model.</div>""",
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(
        """<div class="model-kpi">
    <div class="model-kpi-label">Architecture</div>
    <div class="model-kpi-value">YOLO11n</div>
    <div class="model-kpi-description">Ultralytics object detector</div>
</div>""",
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        """<div class="model-kpi">
    <div class="model-kpi-label">Model Version</div>
    <div class="model-kpi-value">V1</div>
    <div class="model-kpi-description">Current TexInspect detector</div>
</div>""",
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        """<div class="model-kpi">
    <div class="model-kpi-label">Input Size</div>
    <div class="model-kpi-value">640×640</div>
    <div class="model-kpi-description">Training image resolution</div>
</div>""",
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        """<div class="model-kpi">
    <div class="model-kpi-label">Processing</div>
    <div class="model-kpi-value">CPU</div>
    <div class="model-kpi-description">Local inference engine</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# TRAINING INFORMATION
# ============================================================

st.markdown(
    """<div class="section-title">Training Configuration</div>
<div class="section-subtitle">Dataset and training configuration used for TexInspect Detector V1.</div>""",
    unsafe_allow_html=True
)

train1, train2 = st.columns(2)

with train1:
    st.markdown(
        """<div class="info-card">
    <div class="info-card-title">Dataset</div>
    <div class="info-card-text">Patterned Fabric TILDA Dataset — Version 2. The dataset contains annotated fabric images representing four known textile defect categories.</div>
    <br>
    <span class="badge-blue">ROBOFLOW DATASET</span>
</div>""",
        unsafe_allow_html=True
    )

with train2:
    st.markdown(
        """<div class="info-card">
    <div class="info-card-title">Training Setup</div>
    <div class="info-card-text">Baseline training used YOLO11n with 50 epochs, 640×640 image size, batch size 4 and CPU-based training.</div>
    <br>
    <span class="badge-green">BASELINE MODEL</span>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# DATASET STATISTICS
# ============================================================

st.markdown(
    """<div class="section-title">Dataset Statistics</div>
<div class="section-subtitle">Current dataset composition used for model development.</div>""",
    unsafe_allow_html=True
)

d1, d2, d3, d4 = st.columns(4)

dataset_stats = [
    (d1, "500", "TOTAL IMAGES", "Train, validation and test"),
    (d2, "400", "TRAIN", "Training images"),
    (d3, "50", "VALIDATION", "Validation images"),
    (d4, "50", "TEST", "Held-out test images")
]

for column, value, label, description in dataset_stats:
    with column:
        st.markdown(
            f"""<div class="model-kpi">
    <div class="model-kpi-label">{label}</div>
    <div class="model-kpi-value">{value}</div>
    <div class="model-kpi-description">{description}</div>
</div>""",
            unsafe_allow_html=True
        )


# ============================================================
# DEFECT CLASSES
# ============================================================

st.markdown(
    """<div class="section-title">Detected Defect Classes</div>
<div class="section-subtitle">Four known textile defect categories currently supported by the model.</div>""",
    unsafe_allow_html=True
)

class1, class2 = st.columns(2)

with class1:
    st.markdown(
        """<div class="class-card">
    <div class="class-number">01</div>
    <div class="class-name">Foreign Body</div>
    <div class="class-description">Detects unwanted foreign material or objects appearing within the fabric surface.</div>
</div>""",
        unsafe_allow_html=True
    )

with class2:
    st.markdown(
        """<div class="class-card">
    <div class="class-number">02</div>
    <div class="class-name">Hole</div>
    <div class="class-description">Identifies visible openings or hole-type defects within the textile structure.</div>
</div>""",
        unsafe_allow_html=True
    )

class3, class4 = st.columns(2)

with class3:
    st.markdown(
        """<div class="class-card">
    <div class="class-number">03</div>
    <div class="class-name">Stain</div>
    <div class="class-description">Detects visible stain or discoloration regions affecting the fabric surface.</div>
</div>""",
        unsafe_allow_html=True
    )

with class4:
    st.markdown(
        """<div class="class-card">
    <div class="class-number">04</div>
    <div class="class-name">Thread</div>
    <div class="class-description">Detects thread-related defects and abnormal thread structures visible in the fabric.</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# INSPECTION PIPELINE
# ============================================================

st.markdown(
    """<div class="section-title">AI Inspection Pipeline</div>
<div class="section-subtitle">How a fabric image moves through the TexInspect AI system.</div>""",
    unsafe_allow_html=True
)

pipeline1, pipeline2 = st.columns(2)

with pipeline1:
    st.markdown(
        """<div class="pipeline-card">
    <div class="pipeline-step">01 &nbsp; Fabric Image Input</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">02 &nbsp; YOLO11n Detection</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">03 &nbsp; Bounding Box Localization</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">04 &nbsp; Defect Analysis</div>
</div>""",
        unsafe_allow_html=True
    )

with pipeline2:
    st.markdown(
        """<div class="pipeline-card">
    <div class="pipeline-step">05 &nbsp; Severity Calculation</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">06 &nbsp; Quality Decision</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">07 &nbsp; Inspection Result</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">08 &nbsp; Quality History</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# MODEL LIMITATION
# ============================================================

st.markdown(
    """<div class="section-title">Current Model Scope</div>
<div class="section-subtitle">Important distinction between the current implementation and future enhancements.</div>""",
    unsafe_allow_html=True
)

st.info(
    "TexInspect Detector V1 is a known-defect object detection model. "
    "It currently identifies the four trained defect categories only. "
    "Unknown-defect and anomaly detection are planned as future enhancements "
    "when suitable normal/reference data is available."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="tex-footer">
    TexInspect AI &nbsp;•&nbsp;
    Intelligent Textile Quality Inspection Platform
    &nbsp;•&nbsp;
    Model Intelligence
</div>""",
    unsafe_allow_html=True
)