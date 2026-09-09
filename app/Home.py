import sys
from pathlib import Path
import streamlit as st

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# DATABASE IMPORTS
# ============================================================

try:
    from app.database.inspection_service import get_dashboard_statistics
except ImportError:
    from app.database.inspection_service import (
        get_inspection_statistics as get_dashboard_statistics,
    )


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TexInspect AI",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
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

/* SIDEBAR BRAND */
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
.tex-header {
    background: linear-gradient(135deg, #0F172A 0%, #162A46 55%, #1E3A5F 100%);
    padding: 38px 42px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.12);
    position: relative;
    overflow: hidden;
}

.tex-header::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    right: -80px;
    top: -100px;
    background: rgba(37, 99, 235, 0.14);
}

.tex-header h1 {
    font-size: 38px;
    line-height: 1.15;
    margin: 0;
    font-weight: 750;
    color: #FFFFFF;
}

.tex-header p {
    font-size: 16px;
    line-height: 1.6;
    margin-top: 12px;
    margin-bottom: 0;
    color: #CBD5E1;
    max-width: 700px;
}

.hero-badge {
    display: inline-block;
    background: rgba(6, 182, 212, 0.14);
    border: 1px solid rgba(6, 182, 212, 0.30);
    color: #67E8F9;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

/* SECTION TITLES */
.section-title {
    font-size: 21px;
    font-weight: 750;
    color: #0F172A;
    margin-top: 28px;
    margin-bottom: 16px;
}

.section-subtitle {
    font-size: 13px;
    color: #64748B;
    margin-top: -8px;
    margin-bottom: 18px;
}

/* KPI CARDS */
.kpi-card {
    background: #FFFFFF;
    padding: 23px 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
    min-height: 125px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0px 8px 22px rgba(15, 23, 42, 0.09);
}

.kpi-title {
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    font-weight: 700;
}

.kpi-value {
    font-size: 31px;
    font-weight: 750;
    color: #0F172A;
    margin-top: 9px;
    line-height: 1.1;
}

.kpi-description {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 7px;
}

/* ACTION CARDS */
.action-card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    min-height: 145px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
    transform: translateY(-3px);
    border-color: #BFDBFE;
    box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.09);
}

.action-icon {
    font-size: 25px;
    margin-bottom: 10px;
}

.action-title {
    font-size: 17px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 7px;
}

.action-description {
    font-size: 13px;
    line-height: 1.55;
    color: #64748B;
}

/* SYSTEM CARDS */
.system-card {
    background: #FFFFFF;
    padding: 22px 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    min-height: 125px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.system-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 8px;
}

.system-card-text {
    font-size: 13px;
    line-height: 1.6;
    color: #64748B;
}

.system-badge {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-top: 10px;
}

.badge-blue {
    color: #1D4ED8;
    background: #EFF6FF;
}

.badge-green {
    color: #15803D;
    background: #F0FDF4;
}

/* STATUS PANEL */
.status-panel {
    background: #FFFFFF;
    padding: 20px 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.status-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #F1F5F9;
}

.status-row:last-child {
    border-bottom: none;
}

.status-name {
    font-size: 13px;
    color: #475569;
    font-weight: 600;
}

.status-value {
    font-size: 12px;
    font-weight: 700;
}

.online {
    color: #16A34A;
}

.prototype {
    color: #D97706;
}

/* ACTION BUTTONS */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    background: #FFFFFF;
    color: #334155;
    font-weight: 600;
    padding: 0.55rem 0.8rem;
    margin-top: 8px;
}

div.stButton > button:hover {
    border-color: #93C5FD;
    color: #1D4ED8;
    background: #F8FAFC;
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

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}
</style>""",
    unsafe_allow_html=True,
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
<div class="sidebar-status"><span class="status-dot-green"></span> AI Engine Online</div>
<div class="sidebar-status"><span class="status-dot-green"></span> Detector Available</div>
<div class="sidebar-status"><span class="status-dot-green"></span> Database Connected</div>
<div class="sidebar-divider"></div>""",
        unsafe_allow_html=True,
    )

    st.caption("TexInspect AI Platform")
    st.caption("Computer Vision • Textile QC")


# ============================================================
# LOAD DASHBOARD DATA
# ============================================================

try:
    dashboard_data = get_dashboard_statistics()
except Exception:
    dashboard_data = {"success": False}


if dashboard_data.get("success"):
    total_inspections = dashboard_data.get("total_inspections", 0)
    total_defects = dashboard_data.get("total_defects", 0)
    pass_rate = dashboard_data.get("pass_rate", 0)
else:
    total_inspections = 0
    total_defects = 0
    pass_rate = 0


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """<div class="tex-header">
    <div class="hero-badge">AI-POWERED TEXTILE QUALITY CONTROL</div>
    <h1>Textile Quality Command Center</h1>
    <p>AI-powered fabric inspection, defect intelligence and quality decision support for modern textile manufacturing.</p>
</div>""",
    unsafe_allow_html=True,
)


# ============================================================
# QUALITY OVERVIEW
# ============================================================

st.markdown(
    """<div class="section-title">Quality Overview</div>
<div class="section-subtitle">Current inspection and AI system status</div>""",
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4)


# ============================================================
# TOTAL INSPECTIONS
# ============================================================

with col1:
    inspection_description = (
        "Inspection records stored in database"
        if total_inspections > 0
        else "No inspections recorded yet"
    )

    st.markdown(
        f"""<div class="kpi-card">
    <div class="kpi-title">Total Inspections</div>
    <div class="kpi-value">{total_inspections}</div>
    <div class="kpi-description">{inspection_description}</div>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# PASS RATE
# ============================================================

with col2:
    pass_rate_display = (
        f"{float(pass_rate):.1f}%" if total_inspections > 0 else "—"
    )

    pass_description = (
        "Passed quality inspections"
        if total_inspections > 0
        else "Available after inspections"
    )

    st.markdown(
        f"""<div class="kpi-card">
    <div class="kpi-title">Pass Rate</div>
    <div class="kpi-value">{pass_rate_display}</div>
    <div class="kpi-description">{pass_description}</div>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# DEFECTS DETECTED
# ============================================================

with col3:
    st.markdown(
        f"""<div class="kpi-card">
    <div class="kpi-title">Defects Detected</div>
    <div class="kpi-value">{total_defects}</div>
    <div class="kpi-description">Across recorded inspections</div>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# AI MODEL
# ============================================================

with col4:
    st.markdown(
        """<div class="kpi-card">
    <div class="kpi-title">AI Model</div>
    <div class="kpi-value">V1</div>
    <div class="kpi-description">YOLO11n defect detector</div>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# QUICK ACTIONS
# ============================================================

st.markdown(
    """<div class="section-title">Quick Actions</div>
<div class="section-subtitle">Core quality inspection workflows</div>""",
    unsafe_allow_html=True,
)


action1, action2, action3 = st.columns(3)


# ============================================================
# NEW INSPECTION
# ============================================================

with action1:
    st.markdown(
        """<div class="action-card">
    <div class="action-icon">🔍</div>
    <div class="action-title">New Inspection</div>
    <div class="action-description">Upload a fabric image and run AI-powered defect detection and quality analysis.</div>
</div>""",
        unsafe_allow_html=True,
    )

    if st.button(
        "Start New Inspection",
        key="new_inspection_action",
        use_container_width=True,
    ):
        try:
            st.switch_page("pages/New_Inspection.py")
        except Exception:
            st.info("Open New Inspection from the sidebar.")


# ============================================================
# INSPECTION HISTORY
# ============================================================

with action2:
    st.markdown(
        """<div class="action-card">
    <div class="action-icon">📁</div>
    <div class="action-title">Inspection History</div>
    <div class="action-description">Review previous inspections, detected defects and quality decisions.</div>
</div>""",
        unsafe_allow_html=True,
    )

    if st.button(
        "View Inspection History",
        key="inspection_history_action",
        use_container_width=True,
    ):
        try:
            st.switch_page("pages/Inspection_History.py")
        except Exception:
            st.info("Open Inspection History from the sidebar.")


# ============================================================
# QUALITY ANALYTICS
# ============================================================

with action3:
    st.markdown(
        """<div class="action-card">
    <div class="action-icon">📊</div>
    <div class="action-title">Quality Analytics</div>
    <div class="action-description">Explore defect trends, severity patterns and overall inspection performance.</div>
</div>""",
        unsafe_allow_html=True,
    )

    if st.button(
        "Open Quality Analytics",
        key="quality_analytics_action",
        use_container_width=True,
    ):
        try:
            st.switch_page("pages/Quality_Analytics.py")
        except Exception:
            st.info("Quality Analytics page is currently being configured.")


# ============================================================
# SYSTEM INTELLIGENCE
# ============================================================

st.markdown(
    """<div class="section-title">System Intelligence</div>
<div class="section-subtitle">AI components currently available in TexInspect</div>""",
    unsafe_allow_html=True,
)


info1, info2 = st.columns(2)


with info1:
    st.markdown(
        """<div class="system-card">
    <div class="system-card-title">🤖 TexInspect Detector V1</div>
    <div class="system-card-text">YOLO11n-based Computer Vision model trained to identify four known textile defect classes: Foreign Body, Hole, Stain and Thread.</div>
    <span class="system-badge badge-blue">COMPUTER VISION</span>
</div>""",
        unsafe_allow_html=True,
    )


with info2:
    st.markdown(
        """<div class="system-card">
    <div class="system-card-title">⚙️ Quality Decision Engine</div>
    <div class="system-card-text">Converts detected defect characteristics into explainable PASS, WARNING and FAIL quality decisions using defined severity and decision rules.</div>
    <span class="system-badge badge-green">RULE-BASED INTELLIGENCE</span>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# PLATFORM STATUS
# ============================================================

st.markdown(
    """<div class="section-title">Platform Status</div>
<div class="section-subtitle">TexInspect AI component availability</div>""",
    unsafe_allow_html=True,
)


status_col1, status_col2 = st.columns(2)


with status_col1:
    st.markdown(
        """<div class="status-panel">
    <div class="status-row">
        <span class="status-name">AI Detection Engine</span>
        <span class="status-value online">● READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Defect Analysis Engine</span>
        <span class="status-value online">● READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Severity Engine</span>
        <span class="status-value online">● READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Decision Engine</span>
        <span class="status-value online">● READY</span>
    </div>
</div>""",
        unsafe_allow_html=True,
    )


with status_col2:
    st.markdown(
        """<div class="status-panel">
    <div class="status-row">
        <span class="status-name">Inspection Database</span>
        <span class="status-value online">● READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Inspection History</span>
        <span class="status-value online">● READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Quality Analytics</span>
        <span class="status-value prototype">◐ READY</span>
    </div>
    <div class="status-row">
        <span class="status-name">Anomaly Detection</span>
        <span class="status-value prototype">◐ FUTURE ENHANCEMENT</span>
    </div>
</div>""",
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="tex-footer">
TexInspect AI &nbsp;•&nbsp; Intelligent Textile Quality Inspection Platform &nbsp;•&nbsp; Computer Vision Prototype
</div>""",
    unsafe_allow_html=True,
)