import streamlit as st

st.set_page_config(page_title="HTML Test", layout="wide")

st.markdown(
    """
    <style>
    .test-card {
        background: #0F172A;
        color: white;
        padding: 30px;
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="test-card">
        <h1>TexInspect AI</h1>
        <p>HTML rendering test successful.</p>
    </div>
    """,
    unsafe_allow_html=True
)