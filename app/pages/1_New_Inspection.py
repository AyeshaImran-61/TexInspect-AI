import sys
import html
from pathlib import Path

from PIL import Image
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT TEXINSPECT AI ENGINES
# ============================================================

from app.core.detector import TexInspectDetector

from app.core.defect_analysis import (
    analyze_all_detections
)

from app.core.severity_engine import (
    apply_severity_to_defects
)

from app.core.decision_engine import (
    make_quality_decision
)

from app.database.inspection_service import (
    save_inspection
)

from app.database.image_service import (
    save_inspection_images
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="New Inspection | TexInspect AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "last_inspection" not in st.session_state:
    st.session_state["last_inspection"] = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def get_defect_class_name(defect):
    """
    Extract defect class name safely.
    """

    return str(
        defect.get(
            "class_name",
            defect.get(
                "name",
                defect.get(
                    "class",
                    "Unknown Defect"
                )
            )
        )
    )


def get_defect_confidence(defect):
    """
    Extract confidence safely.
    """

    return safe_float(
        defect.get(
            "confidence",
            defect.get(
                "conf",
                0
            )
        )
    )


def get_location_text(defect):
    """
    Convert defect location to readable text.
    """

    location = defect.get(
        "location",
        "Not available"
    )

    if isinstance(location, dict):

        return ", ".join(
            f"{key}: {value}"
            for key, value
            in location.items()
        )

    return str(location)


def get_relative_area(defect):
    """
    Extract relative area safely.
    """

    relative_area = defect.get(
        "relative_area_percent",
        defect.get(
            "relative_area",
            None
        )
    )

    if relative_area is None:
        return None

    return safe_float(
        relative_area,
        default=None
    )


def get_severity_class(severity):
    """
    Return CSS class based on severity.
    """

    severity = str(severity).upper()

    if severity == "CRITICAL":
        return "severity-critical"

    elif severity == "MAJOR":
        return "severity-major"

    elif severity == "MODERATE":
        return "severity-moderate"

    return "severity-minor"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background-color: #F8FAFC;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] > div {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0;
}


/* =========================================================
   SIDEBAR BRAND
========================================================= */

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


/* =========================================================
   PAGE HERO
========================================================= */

.inspection-header {

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

    box-shadow:
        0px 12px 30px rgba(15, 23, 42, 0.12);

    position: relative;

    overflow: hidden;
}

.inspection-header::after {

    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    border-radius: 50%;

    right: -70px;
    top: -100px;

    background:
        rgba(6, 182, 212, 0.10);
}

.inspection-badge {

    display: inline-block;

    background:
        rgba(6, 182, 212, 0.14);

    border:
        1px solid rgba(6, 182, 212, 0.30);

    color: #67E8F9;

    padding: 6px 12px;

    border-radius: 20px;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 13px;
}

.inspection-header h1 {

    font-size: 34px;

    line-height: 1.15;

    margin: 0;

    font-weight: 750;

    color: #FFFFFF;
}

.inspection-header p {

    font-size: 15px;

    line-height: 1.6;

    margin-top: 10px;

    margin-bottom: 0;

    color: #CBD5E1;

    max-width: 750px;
}


/* =========================================================
   SECTION TITLES
========================================================= */

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


/* =========================================================
   UPLOAD CARD
========================================================= */

.upload-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 24px;

    box-shadow:
        0px 4px 12px rgba(15, 23, 42, 0.055);
}

.upload-title {

    font-size: 17px;

    font-weight: 700;

    color: #0F172A;

    margin-bottom: 6px;
}

.upload-description {

    font-size: 13px;

    color: #64748B;

    line-height: 1.5;

    margin-bottom: 18px;
}


/* =========================================================
   CONTROL CARD
========================================================= */

.control-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 24px;

    box-shadow:
        0px 4px 12px rgba(15, 23, 42, 0.055);
}

.control-title {

    font-size: 17px;

    font-weight: 700;

    color: #0F172A;

    margin-bottom: 15px;
}


/* =========================================================
   BUTTON
========================================================= */

.stButton > button {

    border-radius: 12px;

    min-height: 48px;

    font-weight: 700;

    font-size: 15px;
}


/* =========================================================
   IMAGE CARDS
========================================================= */

.image-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 20px;

    box-shadow:
        0px 4px 12px rgba(15, 23, 42, 0.055);

    margin-bottom: 12px;
}

.image-card-title {

    font-size: 16px;

    font-weight: 700;

    color: #0F172A;
}

.image-card-badge {

    display: inline-block;

    padding: 4px 9px;

    border-radius: 12px;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 0.5px;

    margin-left: 7px;
}

.badge-original {

    color: #475569;

    background: #F1F5F9;
}

.badge-ai {

    color: #1D4ED8;

    background: #EFF6FF;
}


/* =========================================================
   RESULT CARDS
========================================================= */

.result-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 22px;

    box-shadow:
        0px 4px 12px rgba(15, 23, 42, 0.055);
}


/* =========================================================
   DECISION CARDS
========================================================= */

.decision-pass {

    background: #F0FDF4;

    border: 1px solid #BBF7D0;

    border-left: 5px solid #16A34A;

    border-radius: 16px;

    padding: 22px;
}

.decision-warning {

    background: #FFFBEB;

    border: 1px solid #FDE68A;

    border-left: 5px solid #F59E0B;

    border-radius: 16px;

    padding: 22px;
}

.decision-fail {

    background: #FEF2F2;

    border: 1px solid #FECACA;

    border-left: 5px solid #DC2626;

    border-radius: 16px;

    padding: 22px;
}

.decision-label {

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;

    color: #64748B;

    margin-bottom: 5px;
}

.decision-value {

    font-size: 30px;

    font-weight: 800;

    margin-bottom: 7px;
}

.pass-text {
    color: #15803D;
}

.warning-text {
    color: #D97706;
}

.fail-text {
    color: #B91C1C;
}

.decision-description {

    font-size: 13px;

    color: #475569;

    line-height: 1.5;
}


/* =========================================================
   DETECTION KPI
========================================================= */

.detection-kpi {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 15px;

    padding: 18px;

    text-align: center;

    min-height: 105px;

    box-shadow:
        0px 4px 12px rgba(15, 23, 42, 0.045);
}

.detection-kpi-label {

    font-size: 10px;

    color: #64748B;

    text-transform: uppercase;

    letter-spacing: 0.9px;

    font-weight: 700;
}

.detection-kpi-value {

    font-size: 26px;

    font-weight: 750;

    color: #0F172A;

    margin-top: 8px;
}


/* =========================================================
   DEFECT CARD
========================================================= */

.defect-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    padding: 18px 20px;

    margin-bottom: 12px;

    box-shadow:
        0px 3px 10px rgba(15, 23, 42, 0.045);
}

.defect-name {

    font-size: 15px;

    font-weight: 700;

    color: #0F172A;
}

.defect-detail {

    font-size: 12px;

    color: #64748B;

    margin-top: 5px;

    line-height: 1.6;
}

.severity-minor {

    color: #1D4ED8;

    background: #EFF6FF;

    padding: 4px 9px;

    border-radius: 12px;

    font-size: 10px;

    font-weight: 700;
}

.severity-moderate {

    color: #B45309;

    background: #FFFBEB;

    padding: 4px 9px;

    border-radius: 12px;

    font-size: 10px;

    font-weight: 700;
}

.severity-major {

    color: #C2410C;

    background: #FFF7ED;

    padding: 4px 9px;

    border-radius: 12px;

    font-size: 10px;

    font-weight: 700;
}

.severity-critical {

    color: #B91C1C;

    background: #FEF2F2;

    padding: 4px 9px;

    border-radius: 12px;

    font-size: 10px;

    font-weight: 700;
}


/* =========================================================
   INSPECTION RECORD
========================================================= */

.inspection-record {

    background: #EFF6FF;

    border: 1px solid #BFDBFE;

    border-left: 4px solid #2563EB;

    border-radius: 12px;

    padding: 12px 16px;

    margin-bottom: 20px;
}

.inspection-record-label {

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 1px;

    color: #64748B;
}

.inspection-record-id {

    font-size: 17px;

    font-weight: 750;

    color: #1D4ED8;

    margin-top: 4px;
}

.inspection-record-text {

    font-size: 12px;

    color: #64748B;

    margin-top: 3px;
}


/* =========================================================
   EMPTY STATE
========================================================= */

.empty-state {

    background: #FFFFFF;

    border: 1px dashed #CBD5E1;

    border-radius: 18px;

    padding: 45px 25px;

    text-align: center;

    margin-top: 10px;
}

.empty-icon {

    font-size: 42px;

    margin-bottom: 12px;
}

.empty-title {

    font-size: 18px;

    font-weight: 700;

    color: #0F172A;

    margin-bottom: 7px;
}

.empty-text {

    font-size: 13px;

    color: #64748B;
}


/* =========================================================
   FOOTER
========================================================= */

.tex-footer {

    margin-top: 40px;

    padding-top: 20px;

    border-top: 1px solid #E2E8F0;

    text-align: center;

    color: #94A3B8;

    font-size: 11px;
}


/* =========================================================
   STREAMLIT CLEANUP
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""<div class="sidebar-brand"><div class="sidebar-brand-title">🔷 TexInspect AI</div><div class="sidebar-brand-subtitle">Textile Quality Intelligence</div></div><div class="sidebar-divider"></div><div class="sidebar-status-title">SYSTEM STATUS</div><div class="sidebar-status"><span class="status-dot-green"></span>AI Engine Online</div><div class="sidebar-status"><span class="status-dot-green"></span>Detector Available</div><div class="sidebar-status"><span class="status-dot-yellow"></span>Prototype Mode</div><div class="sidebar-divider"></div>""", unsafe_allow_html=True)

    st.caption("TexInspect AI Platform")
    st.caption("Computer Vision • Textile QC")


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown("""<div class="inspection-header"><div class="inspection-badge">AI INSPECTION WORKSPACE</div><h1>New Fabric Inspection</h1><p>Upload a fabric image and let TexInspect AI detect, analyze and classify visible textile defects using the trained Computer Vision inspection pipeline.</p></div>""", unsafe_allow_html=True)


# ============================================================
# INSPECTION INPUT SECTION
# ============================================================

st.markdown("""<div class="section-title">Inspection Input</div><div class="section-subtitle">Provide the fabric image and configure the AI inspection.</div>""", unsafe_allow_html=True)


input_col1, input_col2 = st.columns(
    [1.45, 0.75]
)


# ============================================================
# UPLOAD
# ============================================================

with input_col1:

    st.markdown("""<div class="upload-card"><div class="upload-title">📤 Fabric Image</div><div class="upload-description">Upload a clear fabric image for defect detection. Supported formats include JPG, JPEG and PNG.</div></div>""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload fabric image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )


# ============================================================
# CONTROLS
# ============================================================

with input_col2:

    st.markdown("""<div class="control-card"><div class="control-title">⚙️ Inspection Controls</div></div>""", unsafe_allow_html=True)

    confidence = st.slider(
        "Detection Confidence",
        min_value=0.05,
        max_value=0.95,
        value=0.25,
        step=0.05,
        help="Minimum confidence required for a detection."
    )

    st.caption(
        "Lower values detect more possible defects; "
        "higher values produce stricter detections."
    )


# ============================================================
# RUN INSPECTION BUTTON
# ============================================================

run_inspection = st.button(
    "🔍 Run AI Inspection",
    type="primary",
    use_container_width=True
)


# ============================================================
# INSPECTION PIPELINE
# ============================================================

if run_inspection:

    if uploaded_file is None:

        st.warning(
            "Please upload a fabric image before "
            "starting the inspection."
        )

    else:

        try:

            # ------------------------------------------------
            # LOAD IMAGE
            # ------------------------------------------------

            image = Image.open(
                uploaded_file
            ).convert("RGB")


            # ------------------------------------------------
            # LOAD DETECTOR
            # ------------------------------------------------

            with st.spinner(
                "Loading TexInspect AI inspection engine..."
            ):

                detector = TexInspectDetector()


            # ------------------------------------------------
            # RUN DETECTION
            # ------------------------------------------------

            with st.spinner(
                "Analyzing fabric image..."
            ):

                inspection_result = detector.inspect(
                    image,
                    confidence=confidence
                )


            # ------------------------------------------------
            # VALIDATE RESULT
            # ------------------------------------------------

            if not isinstance(
                inspection_result,
                dict
            ):

                raise ValueError(
                    "Detector returned an invalid inspection result."
                )


            # ------------------------------------------------
            # EXTRACT RESULTS
            # ------------------------------------------------

            detections = inspection_result.get(
                "detections",
                []
            )

            if detections is None:
                detections = []

            annotated_image = inspection_result.get(
                "annotated_image"
            )

            image_width = inspection_result.get(
                "image_width",
                image.width
            )

            image_height = inspection_result.get(
                "image_height",
                image.height
            )


            # ------------------------------------------------
            # DEFECT ANALYSIS
            # ------------------------------------------------

            analyzed_defects = analyze_all_detections(

                detections=detections,

                image_width=image_width,

                image_height=image_height
            )

            if analyzed_defects is None:
                analyzed_defects = []


            # ------------------------------------------------
            # SEVERITY ENGINE
            # ------------------------------------------------

            severity_defects = apply_severity_to_defects(
                analyzed_defects
            )

            if severity_defects is None:
                severity_defects = []


            # ------------------------------------------------
            # QUALITY DECISION
            # ------------------------------------------------

            decision = make_quality_decision(
                severity_defects
            )


            # ------------------------------------------------
            # SAVE TO DATABASE
            # ------------------------------------------------

            try:

                database_result = save_inspection(

                    image_name=uploaded_file.name,

                    image_width=image_width,

                    image_height=image_height,

                    confidence=confidence,

                    defects=severity_defects,

                    decision=decision
                )

                # ------------------------------------------------
                # SAVE INSPECTION IMAGES
                # ------------------------------------------------

                image_storage_result = None

                if database_result.get("success"):

                    image_bytes = uploaded_file.getvalue()

                    image_storage_result = save_inspection_images(

                        inspection_id=database_result[
                            "inspection_id"
                        ],

                        image_bytes=image_bytes,

                        original_filename=uploaded_file.name,

                        annotated_image=annotated_image
                    )

            except Exception as database_error:

                database_result = {

                    "success": False,

                    "message": str(
                        database_error
                    )
                }

                image_storage_result = None


            # ------------------------------------------------
            # INSPECTION ID
            # ------------------------------------------------

            inspection_id = None

            if isinstance(
                database_result,
                dict
            ):

                if database_result.get(
                    "success"
                ):

                    inspection_id = database_result.get(
                        "inspection_id"
                    )


            # ------------------------------------------------
            # SAVE RESULTS TO SESSION STATE
            # ------------------------------------------------

            st.session_state[
                "last_inspection"
            ] = {

                "original_image":
                    image,

                "annotated_image":
                    annotated_image,

                "detections":
                    detections,

                "defects":
                    severity_defects,

                "decision":
                    decision,

                "confidence":
                    confidence,

                "image_name":
                    uploaded_file.name,

                "image_width":
                    image_width,

                "image_height":
                    image_height,

                "inspection_id":
                    inspection_id,

                "database_result":
                    database_result
            }


            # ------------------------------------------------
            # DATABASE STATUS
            # ------------------------------------------------

            if database_result.get("success"):

                inspection_id = (
                    database_result["inspection_id"]
                )

                if (
                    image_storage_result
                    and image_storage_result.get("success")
                ):

                    st.success(
                        "AI inspection completed successfully. "
                        f"Inspection ID: {inspection_id}"
                    )

                else:

                    st.warning(
                        "AI inspection completed and database "
                        "record was created, but inspection images "
                        "could not be stored."
                    )

            else:

                st.warning(
                    "AI inspection completed, but the "
                    "inspection could not be saved to "
                    f"the database: "
                    f"{database_result.get('message', 'Unknown error')}"
                )


        except Exception as e:

            st.session_state[
                "last_inspection"
            ] = None

            st.error(
                f"Inspection could not be completed: {str(e)}"
            )


# ============================================================
# DISPLAY RESULTS
# ============================================================

result = st.session_state.get(
    "last_inspection"
)


if result:

    original_image = result.get(
        "original_image"
    )

    annotated_image = result.get(
        "annotated_image"
    )

    defects = result.get(
        "defects",
        []
    )

    decision_result = result.get(
        "decision"
    )

    inspection_id = result.get(
        "inspection_id"
    )


    # ========================================================
    # INSPECTION RESULTS TITLE
    # ========================================================

    st.markdown("""<div class="section-title">Inspection Results</div><div class="section-subtitle">AI-generated visual inspection and quality assessment.</div>""", unsafe_allow_html=True)


    # ========================================================
    # INSPECTION RECORD
    # ========================================================

    if inspection_id:

        st.markdown(
            f"""<div class="inspection-record"><div class="inspection-record-label">INSPECTION RECORD</div><div class="inspection-record-id">{html.escape(str(inspection_id))}</div><div class="inspection-record-text">Inspection successfully stored in the TexInspect AI database.</div></div>""",
            unsafe_allow_html=True
        )


    # ========================================================
    # IMAGE COMPARISON
    # ========================================================

    image_col1, image_col2 = st.columns(2)


    with image_col1:

        st.markdown("""<div class="image-card"><div class="image-card-title">Original Fabric <span class="image-card-badge badge-original">INPUT</span></div></div>""", unsafe_allow_html=True)

        st.image(
            original_image,
            use_container_width=True
        )


    with image_col2:

        st.markdown("""<div class="image-card"><div class="image-card-title">AI Inspection <span class="image-card-badge badge-ai">DETECTED</span></div></div>""", unsafe_allow_html=True)

        if annotated_image is not None:

            st.image(
                annotated_image,
                use_container_width=True
            )

        else:

            st.image(
                original_image,
                use_container_width=True
            )


    # ========================================================
    # DETECTION SUMMARY
    # ========================================================

    st.markdown("""<div class="section-title">Detection Summary</div><div class="section-subtitle">Key measurements produced by the inspection engine.</div>""", unsafe_allow_html=True)


    total_defects = len(
        defects
    )


    unique_classes = len(

        set(

            get_defect_class_name(
                defect
            )

            for defect in defects
        )
    )


    confidence_values = [

        get_defect_confidence(
            defect
        )

        for defect in defects
    ]


    if confidence_values:

        average_confidence = (

            sum(confidence_values)
            /
            len(confidence_values)
        )

    else:

        average_confidence = 0


    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


    with kpi1:

        st.markdown(
            f"""<div class="detection-kpi"><div class="detection-kpi-label">Total Defects</div><div class="detection-kpi-value">{total_defects}</div></div>""",
            unsafe_allow_html=True
        )


    with kpi2:

        st.markdown(
            f"""<div class="detection-kpi"><div class="detection-kpi-label">Defect Classes</div><div class="detection-kpi-value">{unique_classes}</div></div>""",
            unsafe_allow_html=True
        )


    with kpi3:

        confidence_display = (

            f"{average_confidence * 100:.1f}%"

            if total_defects > 0

            else "—"
        )

        st.markdown(
            f"""<div class="detection-kpi"><div class="detection-kpi-label">Avg Confidence</div><div class="detection-kpi-value">{confidence_display}</div></div>""",
            unsafe_allow_html=True
        )


    with kpi4:

        image_size = (

            f"{original_image.width}"
            f" × "
            f"{original_image.height}"
        )

        st.markdown(
            f"""<div class="detection-kpi"><div class="detection-kpi-label">Image Size</div><div class="detection-kpi-value">{image_size}</div></div>""",
            unsafe_allow_html=True
        )


    # ========================================================
    # QUALITY DECISION
    # ========================================================

    st.markdown("""<div class="section-title">Quality Decision</div><div class="section-subtitle">Explainable decision generated from detected defect severity.</div>""", unsafe_allow_html=True)


    if isinstance(
        decision_result,
        dict
    ):

        decision = (

            decision_result.get("decision")

            or decision_result.get("status")

            or decision_result.get("result")

            or "WARNING"
        )

        decision_reason = (

            decision_result.get("reason")

            or decision_result.get("message")

            or decision_result.get("explanation")

            or (
                "Decision generated from the "
                "configured quality rules."
            )
        )

    else:

        decision = str(
            decision_result
        )

        decision_reason = (
            "Decision generated from the "
            "configured quality rules."
        )


    decision = str(
        decision
    ).upper()


    if "PASS" in decision:

        decision_class = "decision-pass"

        decision_text_class = "pass-text"

        decision_icon = "✓"

        decision_label = "QUALITY ACCEPTED"

        display_decision = "PASS"


    elif "FAIL" in decision:

        decision_class = "decision-fail"

        decision_text_class = "fail-text"

        decision_icon = "✕"

        decision_label = "QUALITY REJECTED"

        display_decision = "FAIL"


    else:

        decision_class = "decision-warning"

        decision_text_class = "warning-text"

        decision_icon = "!"

        decision_label = "REVIEW REQUIRED"

        display_decision = "WARNING"


    safe_reason = html.escape(
        str(decision_reason)
    )


    st.markdown(
        f"""<div class="{decision_class}"><div class="decision-label">{decision_label}</div><div class="decision-value {decision_text_class}">{decision_icon} {display_decision}</div><div class="decision-description">{safe_reason}</div></div>""",
        unsafe_allow_html=True
    )


    # ========================================================
    # DEFECT ANALYSIS
    # ========================================================

    st.markdown("""<div class="section-title">Defect Analysis</div><div class="section-subtitle">Detailed characteristics of every detected defect.</div>""", unsafe_allow_html=True)


    if not defects:

        st.markdown("""<div class="empty-state"><div class="empty-icon">✓</div><div class="empty-title">No Defects Detected</div><div class="empty-text">The AI inspection did not identify any defect above the selected confidence threshold.</div></div>""", unsafe_allow_html=True)


    else:

        for index, defect in enumerate(
            defects,
            start=1
        ):

            class_name = get_defect_class_name(
                defect
            )

            confidence_value = get_defect_confidence(
                defect
            )

            confidence_text = (
                f"{confidence_value * 100:.1f}%"
            )

            severity = str(

                defect.get(
                    "severity",
                    "MINOR"
                )

            ).upper()

            location_text = get_location_text(
                defect
            )

            relative_area = get_relative_area(
                defect
            )


            if relative_area is not None:

                area_text = (
                    f"{relative_area:.3f}%"
                )

            else:

                area_text = "—"


            severity_class = get_severity_class(
                severity
            )


            safe_class_name = html.escape(
                class_name
            )

            safe_location = html.escape(
                location_text
            )


            st.markdown(
                f"""<div class="defect-card"><div style="display:flex; justify-space-between; align-items:center; gap:15px;"><div><div class="defect-name">#{index} &nbsp; {safe_class_name}</div><div class="defect-detail">Location: {safe_location} &nbsp; • &nbsp; Confidence: {confidence_text} &nbsp; • &nbsp; Relative Area: {area_text}</div></div><div><span class="{severity_class}">{severity}</span></div></div></div>""",
                unsafe_allow_html=True
            )


    # ========================================================
    # INSPECTION INFORMATION
    # ========================================================

    st.markdown("""<div class="section-title">Inspection Information</div>""", unsafe_allow_html=True)


    meta1, meta2, meta3 = st.columns(3)


    with meta1:

        st.info(
            "**Model:** TexInspect Detector V1\n\n"
            "**Architecture:** YOLO11n"
        )


    with meta2:

        st.info(
            f"**Confidence Threshold:** "
            f"{result['confidence']:.2f}\n\n"
            "**Processing:** CPU"
        )


    with meta3:

        st.info(
            "**Defect Classes:**\n\n"
            "Foreign Body • Hole • Stain • Thread"
        )


# ============================================================
# INITIAL EMPTY STATE
# ============================================================

else:

    st.markdown("""<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-title">Ready for Fabric Inspection</div><div class="empty-text">Upload a fabric image above and click <strong>Run AI Inspection</strong> to begin.</div></div>""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""<div class="tex-footer">TexInspect AI &nbsp;•&nbsp; Intelligent Textile Quality Inspection Platform &nbsp;•&nbsp; AI Inspection Workspace</div>""", unsafe_allow_html=True)