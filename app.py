import streamlit as st
import time
from datetime import datetime

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="DeepGuard | Deepfake Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CUSTOM CSS — this is what makes the app look professional instead of
# "default Streamlit". Replace colors in :root if you want a different theme.
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-primary: #0b0e14;
        --bg-secondary: #10141d;
        --bg-card: #141924;
        --border-color: #232a38;
        --accent: #5b8cff;
        --accent-soft: rgba(91, 140, 255, 0.12);
        --text-primary: #e9edf5;
        --text-secondary: #8b94a7;
        --danger: #ff5c72;
        --danger-soft: rgba(255, 92, 114, 0.12);
        --success: #33d6a6;
        --success-soft: rgba(51, 214, 166, 0.12);
        --warning: #ffb454;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    /* Hide default Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---------- Top navbar / hero ---------- */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.1rem 1.75rem;
        background: linear-gradient(180deg, var(--bg-secondary) 0%, rgba(16,20,29,0.4) 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        margin-bottom: 1.75rem;
    }
    .app-header .brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .app-header .brand-icon {
        width: 42px; height: 42px;
        border-radius: 11px;
        background: linear-gradient(135deg, var(--accent), #8c6bff);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
    }
    .app-header .brand-text h1 {
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.01em;
        color: var(--text-primary);
    }
    .app-header .brand-text p {
        font-size: 0.78rem;
        color: var(--text-secondary);
        margin: 0;
    }
    .status-pill {
        display: flex; align-items: center; gap: 0.4rem;
        padding: 0.35rem 0.8rem;
        background: var(--success-soft);
        border: 1px solid rgba(51, 214, 166, 0.3);
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--success);
    }
    .status-pill .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: var(--success);
    }

    /* ---------- Section titles ---------- */
    .section-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.15rem;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .section-subtitle {
        font-size: 0.82rem;
        color: var(--text-secondary);
        margin-bottom: 1.1rem;
    }

    /* ---------- Upload card ---------- */
    .upload-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
    }

    [data-testid="stFileUploader"] {
        background: var(--bg-secondary);
        border: 1.5px dashed var(--border-color);
        border-radius: 12px;
        padding: 0.5rem;
    }
    [data-testid="stFileUploader"] section {
        background: transparent;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: transparent !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stDownloadButton > button {
        background: var(--accent);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.3rem;
        font-weight: 600;
        font-size: 0.88rem;
        transition: all 0.15s ease;
        width: 100%;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #4a78e8;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(91, 140, 255, 0.35);
    }

    /* ---------- Result cards ---------- */
    .result-card {
        border-radius: 16px;
        padding: 1.6rem;
        border: 1px solid var(--border-color);
        background: var(--bg-card);
        margin-top: 1rem;
    }
    .result-card.fake { border-color: rgba(255,92,114,0.4); background: linear-gradient(180deg, var(--danger-soft), var(--bg-card)); }
    .result-card.real { border-color: rgba(51,214,166,0.4); background: linear-gradient(180deg, var(--success-soft), var(--bg-card)); }

    .result-label {
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin-bottom: 0.2rem;
    }
    .result-label.fake { color: var(--danger); }
    .result-label.real { color: var(--success); }

    .result-sub { color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1rem; }

    /* ---------- Metric chips ---------- */
    .metric-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-top: 0.8rem; }
    .metric-chip {
        flex: 1; min-width: 140px;
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 0.85rem 1rem;
    }
    .metric-chip .val { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
    .metric-chip .lbl { font-size: 0.72rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px; }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

    .sidebar-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.9rem;
    }
    .sidebar-card h4 { font-size: 0.8rem; color: var(--text-primary); margin: 0 0 0.4rem 0; }
    .sidebar-card p { font-size: 0.78rem; color: var(--text-secondary); margin: 0; line-height: 1.5; }

    /* ---------- Progress bar ---------- */
    .stProgress > div > div { background: var(--accent) !important; }

    /* ---------- Footer ---------- */
    .app-footer {
        text-align: center;
        color: var(--text-secondary);
        font-size: 0.75rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid var(--border-color);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-text">
            <h1>DeepGuard</h1>
            <p>AI-Powered Deepfake Detection System</p>
        </div>
    </div>
    <div class="status-pill"><span class="dot"></span> Model Online</div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Detection Settings")

    media_type = st.selectbox("Media type", ["Image", "Video"])
    sensitivity = st.slider("Detection sensitivity", 0, 100, 75)
    show_heatmap = st.checkbox("Show manipulation heatmap", value=True)

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-card">
        <h4>📊 How it works</h4>
        <p>DeepGuard analyzes facial landmarks, texture artifacts, and temporal
        inconsistencies using a trained CNN model to flag manipulated media.</p>
    </div>
    <div class="sidebar-card">
        <h4>🔒 Privacy</h4>
        <p>Uploaded files are processed in-memory and are not stored on any server.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption(f"Session started · {datetime.now().strftime('%d %b %Y, %H:%M')}")

# ----------------------------------------------------------------------------
# MAIN LAYOUT
# ----------------------------------------------------------------------------
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-title">📤 Upload Media</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Supported formats: JPG, PNG, MP4, MOV · Max size 200MB</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=["jpg", "jpeg", "png", "mp4", "mov"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, use_container_width=True)
        else:
            st.video(uploaded_file)

    analyze_clicked = st.button("🔍  Run Detection", disabled=uploaded_file is None)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-title">🧠 Analysis Result</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Results will appear here after analysis</div>',
        unsafe_allow_html=True,
    )

    if uploaded_file is None:
        st.markdown("""
        <div class="result-card">
            <p style="color: var(--text-secondary); text-align:center; padding: 2rem 0; margin:0;">
                Upload an image or video to begin analysis
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif analyze_clicked:
        progress_text = st.empty()
        bar = st.progress(0)
        stages = ["Extracting frames...", "Detecting facial landmarks...",
                  "Running CNN inference...", "Computing confidence score..."]
        for i, stage in enumerate(stages):
            progress_text.markdown(f"<p style='color:var(--text-secondary); font-size:0.82rem;'>{stage}</p>", unsafe_allow_html=True)
            bar.progress(int((i + 1) / len(stages) * 100))
            time.sleep(0.4)
        progress_text.empty()
        bar.empty()

        # ------------------------------------------------------------------
        # PLACEHOLDER PREDICTION — replace this block with your real model
        # inference call, e.g.:
        #   prediction, confidence = your_model.predict(uploaded_file)
        # ------------------------------------------------------------------
        import random
        is_fake = random.choice([True, False])
        confidence = round(random.uniform(78, 98), 1)
        inference_time = round(random.uniform(0.8, 2.4), 2)

        label = "Fake" if is_fake else "Authentic"
        css_class = "fake" if is_fake else "real"
        icon = "⚠️" if is_fake else "✅"

        st.markdown(f"""
        <div class="result-card {css_class}">
            <div class="result-label {css_class}">{icon} {label} Content Detected</div>
            <div class="result-sub">Analysis completed using DeepGuard CNN v2.1</div>
            <div class="metric-row">
                <div class="metric-chip">
                    <div class="val">{confidence}%</div>
                    <div class="lbl">Confidence</div>
                </div>
                <div class="metric-chip">
                    <div class="val">{inference_time}s</div>
                    <div class="lbl">Inference Time</div>
                </div>
                <div class="metric-chip">
                    <div class="val">{sensitivity}</div>
                    <div class="lbl">Sensitivity</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if show_heatmap:
            st.markdown('<div class="section-title" style="margin-top:1.2rem;">🗺️ Manipulation Heatmap</div>', unsafe_allow_html=True)
            st.caption("Highlighted regions indicate areas with the highest manipulation probability.")
            if uploaded_file.type.startswith("image"):
                st.image(uploaded_file, use_container_width=True, caption="Heatmap overlay placeholder — wire up your actual heatmap output here")

    else:
        st.markdown("""
        <div class="result-card">
            <p style="color: var(--text-secondary); text-align:center; padding: 2rem 0; margin:0;">
                Click <b>Run Detection</b> to analyze the uploaded file
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------
st.markdown("""
<div class="app-footer">
    DeepGuard © 2026 · Built with Streamlit · For research &amp; educational purposes only
</div>
""", unsafe_allow_html=True)
