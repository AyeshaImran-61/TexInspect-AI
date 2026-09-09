# ------------------------------------------------------------
# TexInspect AI - Inspection History
# Database-Driven Quality Records
# ------------------------------------------------------------

import streamlit as st
import pandas as pd

from app.database.inspection_service import (
    get_all_inspections,
    get_inspection_statistics,
    get_inspection_by_id
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Inspection History | TexInspect AI",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COLOR SYSTEM
# ============================================================

PRIMARY_NAVY = "#0F172A"
SECONDARY_BLUE = "#162A46"
DARK_BLUE = "#1E3A5F"

BLUE = "#2563EB"
CYAN = "#06B6D4"
CYAN_LIGHT = "#67E8F9"

BACKGROUND = "#F8FAFC"
WHITE = "#FFFFFF"

TEXT = "#1E293B"
SECONDARY_TEXT = "#64748B"
MUTED = "#94A3B8"

BORDER = "#E2E8F0"

GREEN = "#16A34A"
GREEN_LIGHT = "#F0FDF4"

YELLOW = "#F59E0B"
YELLOW_LIGHT = "#FFFBEB"

RED = "#DC2626"
RED_LIGHT = "#FEF2F2"

BLUE_LIGHT = "#EFF6FF"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """<style>
    /* GLOBAL */
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
    .history-header {
        background: linear-gradient(
            135deg,
            #0F172A 0%,
            #162A46 55%,
            #1E3A5F 100%
        );
        padding: 32px 38px;
        border-radius: 20px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.12);
        position: relative;
        overflow: hidden;
    }

    .history-header::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        right: -70px;
        top: -100px;
        background: rgba(6, 182, 212, 0.10);
    }

    .history-badge {
        display: inline-block;
        background: rgba(6, 182, 212, 0.14);
        border: 1px solid rgba(6, 182, 212, 0.30);
        color: #67E8F9;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 13px;
    }

    .history-header h1 {
        font-size: 34px;
        line-height: 1.15;
        margin: 0;
        font-weight: 750;
        color: #FFFFFF;
    }

    .history-header p {
        font-size: 15px;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 0;
        color: #CBD5E1;
        max-width: 800px;
    }

    /* SECTION TITLES */
    .section-title {
        font-size: 21px;
        font-weight: 750;
        color: #0F172A;
        margin-top: 25px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 18px;
    }

    /* KPI CARDS */
    .history-kpi {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        min-height: 115px;
        box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.05);
        position: relative;
        overflow: hidden;
    }

    .history-kpi::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        width: 4px;
        height: 100%;
        background: #2563EB;
    }

    .history-kpi-green::before {
        background: #16A34A;
    }

    .history-kpi-yellow::before {
        background: #F59E0B;
    }

    .history-kpi-red::before {
        background: #DC2626;
    }

    .history-kpi-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.9px;
        color: #64748B;
        text-transform: uppercase;
    }

    .history-kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 8px;
    }

    /* RECORD CARD */
    .inspection-record {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.04);
        transition: 0.2s ease;
    }

    .inspection-record:hover {
        border-color: #CBD5E1;
        box-shadow: 0px 7px 18px rgba(15, 23, 42, 0.07);
    }

    .record-id {
        font-size: 14px;
        font-weight: 750;
        color: #0F172A;
    }

    .record-meta {
        font-size: 12px;
        color: #64748B;
        margin-top: 5px;
    }

    .record-number {
        font-size: 21px;
        font-weight: 800;
        color: #0F172A;
        text-align: center;
    }

    .record-label {
        font-size: 9px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        text-align: center;
    }

    /* STATUS BADGES */
    .status-pass {
        display: inline-block;
        background: #F0FDF4;
        color: #15803D;
        border: 1px solid #BBF7D0;
        padding: 5px 11px;
        border-radius: 14px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 0.5px;
    }

    .status-warning {
        display: inline-block;
        background: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
        padding: 5px 11px;
        border-radius: 14px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 0.5px;
    }

    .status-fail {
        display: inline-block;
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
        padding: 5px 11px;
        border-radius: 14px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: 0.5px;
    }

    /* DETAIL CARDS */
    .detail-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .detail-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
        margin-bottom: 5px;
    }

    .detail-value {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
    }

    /* EMPTY STATE */
    .empty-state {
        background: #FFFFFF;
        border: 1px dashed #CBD5E1;
        border-radius: 18px;
        padding: 55px 25px;
        text-align: center;
        margin-top: 15px;
    }

    .empty-icon {
        font-size: 44px;
        margin-bottom: 12px;
    }

    .empty-title {
        font-size: 19px;
        font-weight: 750;
        color: #0F172A;
        margin-bottom: 7px;
    }

    .empty-text {
        font-size: 13px;
        color: #64748B;
        max-width: 600px;
        margin: auto;
        line-height: 1.6;
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

    #MainMenu, footer {
        visibility: hidden;
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
        <div class="sidebar-status"><span class="status-dot-green"></span>Inspection Database Online</div>
        <div class="sidebar-status"><span class="status-dot-yellow"></span>Prototype Mode</div>
        <div class="sidebar-divider"></div>""",
        unsafe_allow_html=True
    )

    st.caption("TexInspect AI Platform")
    st.caption("Computer Vision • Textile QC")


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """<div class="history-header">
        <div class="history-badge">QUALITY RECORDS</div>
        <h1>Inspection History</h1>
        <p>
            Review previous fabric inspections, quality decisions,
            detected defects and inspection performance from the
            TexInspect AI quality control platform.
        </p>
    </div>""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATABASE
# ============================================================

try:
    statistics = get_inspection_statistics()
    inspections = get_all_inspections()
    database_available = True
except Exception as e:
    database_available = False
    statistics = {
        "total_inspections": 0,
        "passed": 0,
        "warning": 0,
        "failed": 0,
        "total_defects": 0,
        "pass_rate": 0
    }
    inspections = []
    st.error(f"Inspection database could not be loaded: {e}")


# ============================================================
# KPI VALUES
# ============================================================

total_inspections = statistics.get("total_inspections", 0)
pass_count = statistics.get("passed", 0)
warning_count = statistics.get("warning", 0)
fail_count = statistics.get("failed", 0)
total_defects = statistics.get("total_defects", 0)
pass_rate = statistics.get("pass_rate", 0)


# ============================================================
# QUALITY OVERVIEW
# ============================================================

st.markdown(
    """<div class="section-title">Quality Overview</div>
    <div class="section-subtitle">
        Live inspection performance retrieved directly from the TexInspect AI database.
    </div>""",
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(
        f"""<div class="history-kpi">
            <div class="history-kpi-label">Total Inspections</div>
            <div class="history-kpi-value">{total_inspections}</div>
        </div>""",
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""<div class="history-kpi history-kpi-green">
            <div class="history-kpi-label">Passed</div>
            <div class="history-kpi-value">{pass_count}</div>
        </div>""",
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""<div class="history-kpi history-kpi-yellow">
            <div class="history-kpi-label">Warning</div>
            <div class="history-kpi-value">{warning_count}</div>
        </div>""",
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""<div class="history-kpi history-kpi-red">
            <div class="history-kpi-label">Failed</div>
            <div class="history-kpi-value">{fail_count}</div>
        </div>""",
        unsafe_allow_html=True
    )

with kpi5:
    st.markdown(
        f"""<div class="history-kpi">
            <div class="history-kpi-label">Pass Rate</div>
            <div class="history-kpi-value">{pass_rate:.1f}%</div>
        </div>""",
        unsafe_allow_html=True
    )


# ============================================================
# DATABASE SUMMARY
# ============================================================

st.markdown(
    f"""<div style="margin-top:15px; padding:12px 16px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; color:#1E3A5F; font-size:13px;">
        <strong>Database Summary:</strong> {total_inspections} inspection record(s) • {total_defects} detected defect(s) • {fail_count} failed • {warning_count} warning • {pass_count} passed
    </div>""",
    unsafe_allow_html=True
)


# ============================================================
# FILTER SECTION
# ============================================================

st.markdown(
    """<div class="section-title">Inspection Records</div>
    <div class="section-subtitle">
        Search and filter inspection records stored in the TexInspect AI database.
    </div>""",
    unsafe_allow_html=True
)

with st.container(border=True):
    st.markdown("#### 🔎 History Filters")
    filter_col1, filter_col2, filter_col3 = st.columns([1.4, 0.8, 0.8])

    with filter_col1:
        search_text = st.text_input(
            "Search",
            placeholder="Search inspection ID or image name..."
        )

    with filter_col2:
        status_filter = st.selectbox(
            "Quality Decision",
            ["All", "PASS", "WARNING", "FAIL"]
        )

    with filter_col3:
        sort_order = st.selectbox(
            "Sort",
            ["Newest First", "Oldest First", "Most Defects"]
        )


# ============================================================
# FILTER DATABASE RECORDS
# ============================================================

filtered_inspections = inspections.copy()

if search_text:
    search_lower = search_text.lower()
    filtered_inspections = [
        inspection for inspection in filtered_inspections
        if (search_lower in str(inspection.inspection_id).lower())
        or (search_lower in str(inspection.image_name or "").lower())
    ]

if status_filter != "All":
    filtered_inspections = [
        inspection for inspection in filtered_inspections
        if str(inspection.decision).upper() == status_filter
    ]

if sort_order == "Oldest First":
    filtered_inspections = sorted(
        filtered_inspections,
        key=lambda x: (x.inspected_at or "")
    )
elif sort_order == "Most Defects":
    filtered_inspections = sorted(
        filtered_inspections,
        key=lambda x: (x.defect_count or 0),
        reverse=True
    )
else:
    filtered_inspections = sorted(
        filtered_inspections,
        key=lambda x: (x.inspected_at or ""),
        reverse=True
    )


# ============================================================
# RECORD COUNT
# ============================================================

st.caption(
    f"Showing {len(filtered_inspections)} of {len(inspections)} database record(s)."
)


# ============================================================
# EMPTY STATE
# ============================================================

if not filtered_inspections:
    st.markdown(
        """<div class="empty-state">
            <div class="empty-icon">📁</div>
            <div class="empty-title">No Inspection Records</div>
            <div class="empty-text">
                No inspection records match the current filters. Run a fabric inspection from
                the New Inspection page to create a quality record.
            </div>
        </div>""",
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY DATABASE RECORDS
# ============================================================

else:
    for inspection in filtered_inspections:
        inspection_id = inspection.inspection_id or "TXI-UNKNOWN"
        decision = str(inspection.decision or "WARNING").upper()
        defect_count = inspection.defect_count or 0
        confidence = inspection.confidence or 0
        image_name = inspection.image_name or "Unknown image"
        inspected_at = inspection.inspected_at

        if inspected_at:
            timestamp = inspected_at.strftime("%Y-%m-%d %H:%M")
        else:
            timestamp = "Unknown"

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------
        if decision == "PASS":
            status_html = '<span class="status-pass">✓ PASS</span>'
        elif decision == "FAIL":
            status_html = '<span class="status-fail">✕ FAIL</span>'
        else:
            status_html = '<span class="status-warning">! WARNING</span>'

        # ----------------------------------------------------
        # RECORD CARD (HTML INDENTATION FIXED)
        # ----------------------------------------------------
        st.markdown(
            f"""<div class="inspection-record">
                <div style="display:flex; align-items:center; gap:20px;">
                    <div style="flex:2;">
                        <div class="record-id">{inspection_id}</div>
                        <div class="record-meta">🕒 {timestamp} &nbsp; • &nbsp; 📄 {image_name}</div>
                    </div>
                    <div style="flex:1;">
                        <div class="record-label">Defects</div>
                        <div class="record-number">{defect_count}</div>
                    </div>
                    <div style="flex:1;">
                        <div class="record-label">Confidence</div>
                        <div class="record-number">{float(confidence) * 100:.1f}%</div>
                    </div>
                    <div style="flex:1; text-align:center;">
                        {status_html}
                    </div>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # DETAILS
        # ----------------------------------------------------
        with st.expander(f"View inspection details — {inspection_id}"):
            target_inspection = get_inspection_by_id(inspection.inspection_id) or inspection

            # Basic Info
            st.markdown(
                """<div class="section-title">Inspection Information</div>
                <div class="section-subtitle">Complete database record for this inspection.</div>""",
                unsafe_allow_html=True
            )

            info1, info2, info3, info4 = st.columns(4)

            with info1:
                st.markdown(
                    f"""<div class="detail-card">
                        <div class="detail-label">Inspection ID</div>
                        <div class="detail-value">{inspection_id}</div>
                    </div>""",
                    unsafe_allow_html=True
                )

            with info2:
                st.markdown(
                    f"""<div class="detail-card">
                        <div class="detail-label">Image</div>
                        <div class="detail-value">{image_name}</div>
                    </div>""",
                    unsafe_allow_html=True
                )

            with info3:
                st.markdown(
                    f"""<div class="detail-card">
                        <div class="detail-label">Image Size</div>
                        <div class="detail-value">{target_inspection.image_width or "—"} × {target_inspection.image_height or "—"}</div>
                    </div>""",
                    unsafe_allow_html=True
                )

            with info4:
                st.markdown(
                    f"""<div class="detail-card">
                        <div class="detail-label">Confidence Threshold</div>
                        <div class="detail-value">{float(confidence) * 100:.1f}%</div>
                    </div>""",
                    unsafe_allow_html=True
                )

            # Decision
            st.markdown(
                """<div class="section-title">Quality Decision</div>""",
                unsafe_allow_html=True
            )

            if decision == "PASS":
                st.success("✓ PASS — Quality inspection passed.")
            elif decision == "FAIL":
                st.error("✕ FAIL — Quality inspection rejected.")
            else:
                st.warning("! WARNING — Quality review required.")

            if target_inspection.decision_reason:
                st.info(target_inspection.decision_reason)

            # Defects
            st.markdown(
                """<div class="section-title">Detected Defects</div>
                <div class="section-subtitle">Defect-level information recorded during this inspection.</div>""",
                unsafe_allow_html=True
            )

            try:
                defects = getattr(target_inspection, "defects", []) or []
            except Exception:
                defects = []

            if not defects:
                st.success("No defects were stored for this inspection.")
            else:
                rows = []
                for index, defect in enumerate(defects, start=1):
                    confidence_value = defect.confidence if defect.confidence is not None else 0
                    relative_area = defect.relative_area if defect.relative_area is not None else 0

                    rows.append({
                        "#": index,
                        "Defect": defect.defect_type,
                        "Confidence": f"{float(confidence_value) * 100:.1f}%",
                        "Severity": str(defect.severity or "—").upper(),
                        "Location": defect.location or "—",
                        "Relative Area": f"{float(relative_area):.3f}%",
                        "Bounding Box": (
                            f"({defect.x1:.1f}, {defect.y1:.1f}) → ({defect.x2:.1f}, {defect.y2:.1f})"
                        ) if all(v is not None for v in [defect.x1, defect.y1, defect.x2, defect.y2]) else "—"
                    })

                defects_df = pd.DataFrame(rows)
                st.dataframe(defects_df, width="stretch", hide_index=True)

                # Severity Summary
                severity_counts = {}
                for defect in defects:
                    severity = str(defect.severity or "UNKNOWN").upper()
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1

                st.markdown(
                    """<div class="section-title">Severity Summary</div>""",
                    unsafe_allow_html=True
                )

                severity_columns = st.columns(max(1, len(severity_counts)))

                for column, (severity, count) in zip(severity_columns, severity_counts.items()):
                    with column:
                        if severity == "CRITICAL":
                            st.error(f"CRITICAL\n\n{count}")
                        elif severity == "MAJOR":
                            st.warning(f"MAJOR\n\n{count}")
                        elif severity == "MODERATE":
                            st.info(f"MODERATE\n\n{count}")
                        else:
                            st.success(f"{severity}\n\n{count}")

            # Database Metadata
            st.markdown(
                """<div class="section-title">Database Metadata</div>""",
                unsafe_allow_html=True
            )

            meta1, meta2, meta3 = st.columns(3)

            with meta1:
                st.metric("Database Record ID", target_inspection.id)

            with meta2:
                st.metric("Total Defects", target_inspection.defect_count or 0)

            with meta3:
                st.metric("Inspection Timestamp", timestamp)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="tex-footer">
        TexInspect AI &nbsp;•&nbsp; Intelligent Textile Quality Inspection Platform &nbsp;•&nbsp; Database-Driven Inspection History
    </div>""",
    unsafe_allow_html=True
) 