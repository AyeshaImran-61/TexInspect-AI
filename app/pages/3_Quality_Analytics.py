# ============================================================
# TexInspect AI - Quality Analytics
# Database-Driven Quality Intelligence Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

from app.database.inspection_service import (
    get_all_inspections,
    get_inspection_statistics
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Quality Analytics | TexInspect AI",
    page_icon="📊",
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
ORANGE = "#F97316"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #F8FAFC;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

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

.analytics-header {
    background: linear-gradient(135deg, #0F172A 0%, #162A46 55%, #1E3A5F 100%);
    padding: 32px 38px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.12);
    position: relative;
    overflow: hidden;
}

.analytics-header::after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    right: -70px;
    top: -100px;
    background: rgba(6, 182, 212, 0.10);
}

.analytics-badge {
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

.analytics-header h1 {
    font-size: 34px;
    line-height: 1.15;
    margin: 0;
    font-weight: 750;
    color: #FFFFFF;
}

.analytics-header p {
    font-size: 15px;
    line-height: 1.6;
    margin-top: 10px;
    margin-bottom: 0;
    color: #CBD5E1;
    max-width: 820px;
}

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

.analytics-kpi {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px;
    min-height: 118px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.05);
    position: relative;
    overflow: hidden;
}

.analytics-kpi::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background: #2563EB;
}

.kpi-green::before { background: #16A34A; }
.kpi-yellow::before { background: #F59E0B; }
.kpi-red::before { background: #DC2626; }
.kpi-cyan::before { background: #06B6D4; }

.analytics-kpi-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.9px;
    color: #64748B;
    text-transform: uppercase;
}

.analytics-kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 8px;
}

.analytics-kpi-description {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 4px;
}

.chart-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.045);
    margin-bottom: 20px;
}

.chart-title {
    font-size: 16px;
    font-weight: 750;
    color: #0F172A;
    margin-bottom: 3px;
}

.chart-description {
    font-size: 12px;
    color: #64748B;
    margin-bottom: 12px;
}

.insight-card {
    background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
    border: 1px solid #BFDBFE;
    border-left: 5px solid #2563EB;
    border-radius: 16px;
    padding: 21px;
    margin-bottom: 20px;
}

.insight-title {
    font-size: 15px;
    font-weight: 750;
    color: #1E3A8A;
    margin-bottom: 8px;
}

.insight-text {
    font-size: 13px;
    color: #475569;
    line-height: 1.6;
}

.defect-stat {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 15px 18px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.defect-stat-name {
    font-size: 13px;
    font-weight: 700;
    color: #1E293B;
}

.defect-stat-count {
    font-size: 18px;
    font-weight: 800;
    color: #2563EB;
}

.database-status {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #166534;
}

.database-status strong {
    color: #15803D;
}

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
    max-width: 650px;
    margin: auto;
    line-height: 1.6;
}

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

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">🔷 TexInspect AI</div>
            <div class="sidebar-brand-subtitle">Textile Quality Intelligence</div>
        </div>
        <div class="sidebar-divider"></div>
        <div class="sidebar-status-title">SYSTEM STATUS</div>
        <div class="sidebar-status"><span class="status-dot-green"></span> AI Engine Online</div>
        <div class="sidebar-status"><span class="status-dot-green"></span> Detector Available</div>
        <div class="sidebar-status"><span class="status-dot-green"></span> Database Connected</div>
        <div class="sidebar-status"><span class="status-dot-yellow"></span> Prototype Mode</div>
        <div class="sidebar-divider"></div>
        """,
        unsafe_allow_html=True
    )
    st.caption("TexInspect AI Platform")
    st.caption("Computer Vision • Textile QC")


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="analytics-header">
        <div class="analytics-badge">QUALITY INTELLIGENCE</div>
        <h1>Quality Analytics</h1>
        <p>
            Transform inspection results into actionable quality intelligence.
            Monitor pass rates, defect patterns, inspection performance
            and overall fabric quality trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATABASE DATA
# ============================================================

try:
    statistics = get_inspection_statistics()
    inspections = get_all_inspections()
    database_available = True
except Exception as e:
    statistics = {
        "total_inspections": 0,
        "passed": 0,
        "warning": 0,
        "failed": 0,
        "total_defects": 0,
        "pass_rate": 0
    }
    inspections = []
    database_available = False
    st.error(f"Unable to load inspection analytics from database: {str(e)}")


# ============================================================
# DATABASE STATUS
# ============================================================

if database_available:
    st.markdown(
        """
        <div class="database-status">
            <strong>● Database Connected</strong> &nbsp; Analytics are generated from the TexInspect AI inspection database.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EMPTY STATE OR DASHBOARD
# ============================================================

if not inspections:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📊</div>
            <div class="empty-title">Analytics Awaiting Inspection Data</div>
            <div class="empty-text">
                Run fabric inspections from the New Inspection page to populate this quality intelligence dashboard.
                Once inspection records are available, this page will display quality KPIs, decision trends, defect patterns and operational insights.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # ========================================================
    # BASIC STATISTICS
    # ========================================================
    total_inspections = statistics["total_inspections"]
    pass_count = statistics["passed"]
    warning_count = statistics["warning"]
    fail_count = statistics["failed"]
    total_defects = statistics["total_defects"]
    pass_rate = statistics["pass_rate"]
    avg_defects = total_defects / total_inspections if total_inspections else 0

    defect_counter = Counter()
    severity_counter = Counter()
    defect_rows = []
    inspection_rows = []

    # ========================================================
    # PROCESS INSPECTIONS WITH SAFE RELATIONSHIP ACCESS
    # ========================================================
    for inspection in inspections:
        inspection_rows.append({
            "Inspection ID": inspection.inspection_id,
            "Timestamp": inspection.inspected_at,
            "Decision": inspection.decision,
            "Defects": inspection.defect_count or 0,
            "Confidence": inspection.confidence
        })

        # SAFELY ATTEMPT ACCESS TO DEFECTS RELATIONSHIP TO PREVENT DETACHED INSTANCE ERRORS
        try:
            defects_list = inspection.defects or []
        except Exception:
            defects_list = []

        for defect in defects_list:
            defect_name = defect.defect_type or "Unknown Defect"
            severity_name = str(defect.severity or "Unknown").upper()

            defect_counter[defect_name] += 1
            severity_counter[severity_name] += 1

            defect_rows.append({
                "Inspection ID": inspection.inspection_id,
                "Defect": defect_name,
                "Confidence": defect.confidence,
                "Severity": severity_name,
                "Relative Area": defect.relative_area,
                "Location": defect.location
            })

    # ========================================================
    # QUALITY PERFORMANCE
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Quality Performance</div>
        <div class="section-subtitle">Current inspection performance across the recorded database dataset.</div>
        """,
        unsafe_allow_html=True
    )

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

    with kpi1:
        st.markdown(
            f"""
            <div class="analytics-kpi">
                <div class="analytics-kpi-label">Inspections</div>
                <div class="analytics-kpi-value">{total_inspections}</div>
                <div class="analytics-kpi-description">Total quality checks</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="analytics-kpi kpi-green">
                <div class="analytics-kpi-label">Pass Rate</div>
                <div class="analytics-kpi-value">{pass_rate:.1f}%</div>
                <div class="analytics-kpi-description">Accepted inspections</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="analytics-kpi kpi-yellow">
                <div class="analytics-kpi-label">Warnings</div>
                <div class="analytics-kpi-value">{warning_count}</div>
                <div class="analytics-kpi-description">Require review</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="analytics-kpi kpi-red">
                <div class="analytics-kpi-label">Failed</div>
                <div class="analytics-kpi-value">{fail_count}</div>
                <div class="analytics-kpi-description">Quality rejection</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi5:
        st.markdown(
            f"""
            <div class="analytics-kpi kpi-cyan">
                <div class="analytics-kpi-label">Total Defects</div>
                <div class="analytics-kpi-value">{total_defects}</div>
                <div class="analytics-kpi-description">AI detections</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi6:
        st.markdown(
            f"""
            <div class="analytics-kpi">
                <div class="analytics-kpi-label">Avg Defects</div>
                <div class="analytics-kpi-value">{avg_defects:.1f}</div>
                <div class="analytics-kpi-description">Per inspection</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # QUALITY DECISION ANALYSIS
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Quality Decision Analysis</div>
        <div class="section-subtitle">Distribution of PASS, WARNING and FAIL inspection decisions recorded in the database.</div>
        """,
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown(
            """
            <div class="chart-card">
                <div class="chart-title">Decision Distribution</div>
                <div class="chart-description">Overall quality outcome of recorded inspections.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        decision_df = pd.DataFrame({
            "Decision": ["PASS", "WARNING", "FAIL"],
            "Count": [pass_count, warning_count, fail_count]
        })

        fig_decision = px.pie(
            decision_df,
            names="Decision",
            values="Count",
            hole=0.58,
            color="Decision",
            color_discrete_map={"PASS": GREEN, "WARNING": YELLOW, "FAIL": RED}
        )
        fig_decision.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(orientation="h", y=-0.05)
        )
        st.plotly_chart(fig_decision, use_container_width=True)

    with chart_col2:
        st.markdown(
            """
            <div class="chart-card">
                <div class="chart-title">Defects per Inspection</div>
                <div class="chart-description">Number of detected defects across individual inspections.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        defect_distribution = Counter(int(inspection.defect_count or 0) for inspection in inspections)
        distribution_df = pd.DataFrame({
            "Defects": list(defect_distribution.keys()),
            "Inspections": list(defect_distribution.values())
        }).sort_values("Defects")

        fig_distribution = px.bar(
            distribution_df,
            x="Defects",
            y="Inspections",
            text="Inspections",
            color_discrete_sequence=[BLUE]
        )
        fig_distribution.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Detected Defects",
            yaxis_title="Number of Inspections"
        )
        fig_distribution.update_traces(textposition="outside")
        st.plotly_chart(fig_distribution, use_container_width=True)

    # ========================================================
    # DEFECT INTELLIGENCE
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Defect Intelligence</div>
        <div class="section-subtitle">Identify which defect categories are appearing most frequently across all stored inspections.</div>
        """,
        unsafe_allow_html=True
    )

    defect_col1, defect_col2 = st.columns([1, 1.5])

    with defect_col1:
        if defect_counter:
            sorted_defects = sorted(defect_counter.items(), key=lambda x: x[1], reverse=True)
            for name, count in sorted_defects:
                st.markdown(
                    f"""
                    <div class="defect-stat">
                        <div class="defect-stat-name">{name}</div>
                        <div class="defect-stat-count">{count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No defect detections are currently available.")

    with defect_col2:
        if defect_counter:
            defect_df = pd.DataFrame({
                "Defect": list(defect_counter.keys()),
                "Detections": list(defect_counter.values())
            }).sort_values("Detections", ascending=True)

            fig_defects = px.bar(
                defect_df,
                x="Detections",
                y="Defect",
                orientation="h",
                text="Detections",
                color_discrete_sequence=[CYAN]
            )
            fig_defects.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title="Number of Detections",
                yaxis_title=""
            )
            fig_defects.update_traces(textposition="outside")
            st.plotly_chart(fig_defects, use_container_width=True)
        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">🔍</div>
                    <div class="empty-title">No Defect Categories Yet</div>
                    <div class="empty-text">Run inspections containing detected defects to populate defect intelligence analytics.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # SEVERITY INTELLIGENCE
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Severity Intelligence</div>
        <div class="section-subtitle">Distribution of defect severity levels calculated by the TexInspect AI severity engine.</div>
        """,
        unsafe_allow_html=True
    )

    severity_col1, severity_col2 = st.columns(2)

    with severity_col1:
        st.markdown(
            """
            <div class="chart-card">
                <div class="chart-title">Severity Distribution</div>
                <div class="chart-description">Distribution of MINOR, MODERATE, MAJOR and CRITICAL detected defects.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        severity_order = ["MINOR", "MODERATE", "MAJOR", "CRITICAL"]
        severity_data = [{"Severity": s, "Count": severity_counter.get(s, 0)} for s in severity_order]
        severity_df = pd.DataFrame(severity_data)

        fig_severity = px.bar(
            severity_df,
            x="Severity",
            y="Count",
            text="Count",
            color="Severity",
            color_discrete_map={"MINOR": BLUE, "MODERATE": YELLOW, "MAJOR": ORANGE, "CRITICAL": RED}
        )
        fig_severity.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Severity Level",
            yaxis_title="Detected Defects",
            showlegend=False
        )
        fig_severity.update_traces(textposition="outside")
        st.plotly_chart(fig_severity, use_container_width=True)

    with severity_col2:
        severity_display = [
            ("CRITICAL", severity_counter.get("CRITICAL", 0)),
            ("MAJOR", severity_counter.get("MAJOR", 0)),
            ("MODERATE", severity_counter.get("MODERATE", 0)),
            ("MINOR", severity_counter.get("MINOR", 0))
        ]

        for severity, count in severity_display:
            accent = RED if severity == "CRITICAL" else ORANGE if severity == "MAJOR" else YELLOW if severity == "MODERATE" else BLUE
            st.markdown(
                f"""
                <div class="defect-stat">
                    <div class="defect-stat-name" style="border-left: 4px solid {accent}; padding-left: 10px;">{severity}</div>
                    <div class="defect-stat-count" style="color: {accent};">{count}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # INSPECTION TREND
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Inspection Trend</div>
        <div class="section-subtitle">Inspection volume and detected defect activity across recorded inspection sessions.</div>
        """,
        unsafe_allow_html=True
    )

    trend_rows = []
    sorted_inspections = sorted(inspections, key=lambda x: x.inspected_at if x.inspected_at else 0)

    for index, inspection in enumerate(sorted_inspections, start=1):
        trend_rows.append({
            "Inspection": index,
            "Defects": int(inspection.defect_count or 0),
            "Decision": str(inspection.decision or "WARNING").upper()
        })

    trend_df = pd.DataFrame(trend_rows)
    fig_trend = px.line(
        trend_df,
        x="Inspection",
        y="Defects",
        markers=True,
        color_discrete_sequence=[BLUE]
    )
    fig_trend.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Inspection Sequence",
        yaxis_title="Detected Defects"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ========================================================
    # QUALITY INTELLIGENCE
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Quality Intelligence</div>
        <div class="section-subtitle">Automated interpretation of the current database inspection dataset.</div>
        """,
        unsafe_allow_html=True
    )

    if defect_counter:
        most_common_defect = defect_counter.most_common(1)[0]
        common_defect_name, common_defect_count = most_common_defect[0], most_common_defect[1]
    else:
        common_defect_name, common_defect_count = "No defect category identified", 0

    severity_priority = ["CRITICAL", "MAJOR", "MODERATE", "MINOR"]
    highest_severity = "NONE"
    for s in severity_priority:
        if severity_counter.get(s, 0) > 0:
            highest_severity = s
            break

    if pass_rate >= 80:
        quality_message = "Current inspection results indicate a strong overall quality acceptance rate."
    elif pass_rate >= 50:
        quality_message = "Inspection results show a mixed quality profile. Additional monitoring and defect review are recommended."
    else:
        quality_message = "The current dataset shows a low acceptance rate. Quality review and investigation of recurring defects are recommended."

    critical_count = severity_counter.get("CRITICAL", 0)
    major_count = severity_counter.get("MAJOR", 0)

    if critical_count > 0:
        severity_message = f"{critical_count} critical defect(s) require immediate quality attention."
    elif major_count > 0:
        severity_message = f"{major_count} major defect(s) require quality review."
    else:
        severity_message = "No critical or major defects are currently recorded in the database."

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🤖 TexInspect AI Quality Insight</div>
            <div class="insight-text">
                <strong>Overall Assessment:</strong> {quality_message}<br><br>
                <strong>Inspection Volume:</strong> {total_inspections} inspection(s) have been analyzed.<br><br>
                <strong>Defect Activity:</strong> {total_defects} total defect(s) detected, averaging {avg_defects:.1f} defect(s) per inspection.<br><br>
                <strong>Most Frequent Defect:</strong> {common_defect_name} ({common_defect_count} detection(s)).<br><br>
                <strong>Highest Severity Present:</strong> {highest_severity}.<br><br>
                <strong>Severity Assessment:</strong> {severity_message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # ANALYTICS DATASET
    # ========================================================
    st.markdown(
        """
        <div class="section-title">Analytics Dataset</div>
        <div class="section-subtitle">Inspection-level data retrieved directly from the TexInspect AI database.</div>
        """,
        unsafe_allow_html=True
    )

    table_rows = []
    for inspection in inspections:
        try:
            conf_val = float(inspection.confidence)
            conf_str = f"{conf_val * 100:.1f}%" if conf_val <= 1.0 else f"{conf_val:.1f}%"
        except (ValueError, TypeError):
            conf_str = "N/A"

        timestamp = inspection.inspected_at.strftime("%Y-%m-%d %H:%M:%S") if inspection.inspected_at else "N/A"

        table_rows.append({
            "Inspection ID": inspection.inspection_id,
            "Timestamp": timestamp,
            "Decision": str(inspection.decision or "WARNING").upper(),
            "Defects": int(inspection.defect_count or 0),
            "Confidence": conf_str
        })

    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    if defect_rows:
        st.markdown(
            """
            <div class="section-title">Defect Analytics Dataset</div>
            <div class="section-subtitle">Detailed defect-level records used to calculate defect and severity analytics.</div>
            """,
            unsafe_allow_html=True
        )

        defect_df_display = pd.DataFrame(defect_rows)
        if not defect_df_display.empty:
            defect_df_display["Confidence"] = defect_df_display["Confidence"].apply(
                lambda x: f"{float(x) * 100:.1f}%" if x is not None and str(x).replace('.', '', 1).isdigit() and float(x) <= 1.0 else (f"{float(x):.1f}%" if x is not None and str(x).replace('.', '', 1).isdigit() else "N/A")
            )
            defect_df_display["Relative Area"] = defect_df_display["Relative Area"].apply(
                lambda x: f"{float(x):.2f}%" if x is not None and str(x).replace('.', '', 1).isdigit() else "N/A"
            )

        st.dataframe(defect_df_display, use_container_width=True, hide_index=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="tex-footer">
        TexInspect AI &nbsp;•&nbsp; Intelligent Textile Quality Inspection Platform &nbsp;•&nbsp; Quality Intelligence & Analytics
    </div>
    """,
    unsafe_allow_html=True
)