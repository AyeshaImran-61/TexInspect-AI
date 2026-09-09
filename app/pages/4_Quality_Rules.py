import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Quality Rules | TexInspect AI",
    page_icon="⚙️",
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
.rules-header {
    background: linear-gradient(135deg, #0F172A 0%, #162A46 55%, #1E3A5F 100%);
    padding: 34px 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.12);
    position: relative;
    overflow: hidden;
}

.rules-header::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    right: -80px;
    top: -110px;
    background: rgba(6, 182, 212, 0.10);
}

.rules-badge {
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

.rules-header h1 {
    font-size: 36px;
    line-height: 1.15;
    margin: 0;
    font-weight: 750;
    color: #FFFFFF;
}

.rules-header p {
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

/* RULE CARDS */
.rule-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 22px 24px;
    min-height: 135px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.rule-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 8px;
}

.rule-card-text {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
}

.rule-threshold {
    font-size: 21px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 10px;
}

/* SEVERITY BADGES */
.severity-badge {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 0.6px;
    margin-bottom: 8px;
}

.minor {
    color: #1D4ED8;
    background: #EFF6FF;
}

.moderate {
    color: #B45309;
    background: #FFFBEB;
}

.major {
    color: #C2410C;
    background: #FFF7ED;
}

.critical {
    color: #B91C1C;
    background: #FEF2F2;
}

/* DECISION CARDS */
.decision-card {
    background: #FFFFFF;
    border-radius: 17px;
    padding: 22px 24px;
    min-height: 155px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.decision-card-pass {
    border: 1px solid #BBF7D0;
    border-left: 5px solid #16A34A;
}

.decision-card-warning {
    border: 1px solid #FDE68A;
    border-left: 5px solid #F59E0B;
}

.decision-card-fail {
    border: 1px solid #FECACA;
    border-left: 5px solid #DC2626;
}

.decision-card-title {
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 9px;
}

.pass-color {
    color: #15803D;
}

.warning-color {
    color: #D97706;
}

.fail-color {
    color: #B91C1C;
}

.decision-card-text {
    font-size: 13px;
    color: #64748B;
    line-height: 1.6;
}

/* FLOW */
.flow-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 23px;
    box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.055);
}

.flow-step {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    padding: 13px 16px;
    border-radius: 11px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #475569;
}

.flow-arrow {
    text-align: center;
    color: #2563EB;
    font-weight: 700;
    margin: 2px 0;
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
    """<div class="rules-header">
    <div class="rules-badge">QUALITY DECISION INTELLIGENCE</div>
    <h1>Quality Rules</h1>
    <p>Transparent and explainable rules used by TexInspect AI to convert detected defect characteristics into severity levels and final quality decisions.</p>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# SEVERITY ENGINE
# ============================================================

st.markdown(
    """<div class="section-title">Defect Severity Rules</div>
<div class="section-subtitle">Severity is calculated from the relative area occupied by a detected defect.</div>""",
    unsafe_allow_html=True
)

s1, s2 = st.columns(2)

with s1:
    st.markdown(
        """<div class="rule-card">
    <span class="severity-badge minor">MINOR</span>
    <div class="rule-card-text">Small detected defect occupying less than 0.5% of the inspected image area.</div>
    <div class="rule-threshold">Relative Area &lt; 0.5%</div>
</div>""",
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        """<div class="rule-card">
    <span class="severity-badge moderate">MODERATE</span>
    <div class="rule-card-text">Defect occupies at least 0.5% but remains below the major-defect threshold.</div>
    <div class="rule-threshold">0.5% ≤ Area &lt; 2%</div>
</div>""",
        unsafe_allow_html=True
    )

s3, s4 = st.columns(2)

with s3:
    st.markdown(
        """<div class="rule-card">
    <span class="severity-badge major">MAJOR</span>
    <div class="rule-card-text">Significant defect occupying at least 2% of the inspected image area.</div>
    <div class="rule-threshold">2% ≤ Area &lt; 5%</div>
</div>""",
        unsafe_allow_html=True
    )

with s4:
    st.markdown(
        """<div class="rule-card">
    <span class="severity-badge critical">CRITICAL</span>
    <div class="rule-card-text">Very large defect occupying at least 5% of the inspected image area.</div>
    <div class="rule-threshold">Relative Area ≥ 5%</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# DECISION ENGINE
# ============================================================

st.markdown(
    """<div class="section-title">Quality Decision Rules</div>
<div class="section-subtitle">The final quality decision is generated from the severity and number of detected defects.</div>""",
    unsafe_allow_html=True
)

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown(
        """<div class="decision-card decision-card-pass">
    <div class="decision-card-title pass-color">✓ PASS</div>
    <div class="decision-card-text">Assigned when no known textile defects are detected by the inspection model.</div>
</div>""",
        unsafe_allow_html=True
    )

with d2:
    st.markdown(
        """<div class="decision-card decision-card-warning">
    <div class="decision-card-title warning-color">! WARNING</div>
    <div class="decision-card-text">Assigned when moderate or minor defects require quality review but do not trigger the defined failure conditions.</div>
</div>""",
        unsafe_allow_html=True
    )

with d3:
    st.markdown(
        """<div class="decision-card decision-card-fail">
    <div class="decision-card-title fail-color">✕ FAIL</div>
    <div class="decision-card-text">Assigned when critical, major, or multiple defects meet the defined rejection conditions.</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# FAIL CONDITIONS
# ============================================================

st.markdown(
    """<div class="section-title">FAIL Conditions</div>
<div class="section-subtitle">Any one of the following conditions causes the inspection to fail.</div>""",
    unsafe_allow_html=True
)

fail1, fail2 = st.columns(2)

with fail1:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Critical Defect</div>
    <div class="rule-card-text">If at least one detected defect has <strong>CRITICAL</strong> severity, the fabric is rejected.</div>
</div>""",
        unsafe_allow_html=True
    )

with fail2:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Major Defect</div>
    <div class="rule-card-text">A single <strong>MAJOR</strong> defect is sufficient to produce a FAIL decision.</div>
</div>""",
        unsafe_allow_html=True
    )

fail3, fail4 = st.columns(2)

with fail3:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Multiple Major Defects</div>
    <div class="rule-card-text">Two or more MAJOR defects automatically produce a FAIL decision.</div>
</div>""",
        unsafe_allow_html=True
    )

with fail4:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Multiple Defects</div>
    <div class="rule-card-text">Three or more detected defects produce a FAIL decision under the current rules.</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# WARNING CONDITIONS
# ============================================================

st.markdown(
    """<div class="section-title">WARNING Conditions</div>
<div class="section-subtitle">Conditions that require review without triggering the current FAIL rules.</div>""",
    unsafe_allow_html=True
)

w1, w2 = st.columns(2)

with w1:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Moderate Defect</div>
    <div class="rule-card-text">A MODERATE defect produces a WARNING when no higher-priority FAIL condition applies.</div>
</div>""",
        unsafe_allow_html=True
    )

with w2:
    st.markdown(
        """<div class="rule-card">
    <div class="rule-card-title">Minor Defect</div>
    <div class="rule-card-text">A MINOR defect produces a WARNING and indicates that quality review may be required.</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# DECISION PRIORITY
# ============================================================

st.markdown(
    """<div class="section-title">Decision Priority</div>
<div class="section-subtitle">The engine evaluates conditions in a defined order to produce one final decision.</div>""",
    unsafe_allow_html=True
)

st.markdown(
    """<div class="flow-card">
    <div class="flow-step">01 &nbsp; No defects → PASS</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">02 &nbsp; Critical defect → FAIL</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">03 &nbsp; Two or more major defects → FAIL</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">04 &nbsp; One major defect → FAIL</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">05 &nbsp; Three or more total defects → FAIL</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">06 &nbsp; Moderate defect → WARNING</div>
    <div class="flow-arrow">↓</div>
    <div class="flow-step">07 &nbsp; Minor defect → WARNING</div>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# ENGINE PRINCIPLE
# ============================================================

st.markdown(
    """<div class="section-title">Explainable Quality Intelligence</div>""",
    unsafe_allow_html=True
)

st.info(
    "TexInspect AI currently uses deterministic, rule-based quality decisions. "
    "The decision engine does not invent a quality result: it evaluates the "
    "detected defects and their calculated severity against the configured "
    "business rules shown on this page."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="tex-footer">
    TexInspect AI &nbsp;•&nbsp;
    Intelligent Textile Quality Inspection Platform
    &nbsp;•&nbsp;
    Explainable Quality Intelligence
</div>""",
    unsafe_allow_html=True
)