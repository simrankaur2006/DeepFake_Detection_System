import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DeepGuard | Deepfake Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ---------- Global ---------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.15), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(168, 85, 247, 0.12), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(59, 130, 246, 0.10), transparent 35%),
            #080b14;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Hide Streamlit default ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- Hero ---------- */

    .hero {
        text-align: center;
        padding: 35px 20px 25px 20px;
    }

    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 30px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.35);
        color: #a5b4fc;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 58px;
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0;
        background: linear-gradient(
            90deg,
            #ffffff,
            #a5b4fc,
            #c084fc
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #94a3b8;
        font-size: 18px;
        max-width: 700px;
        margin: 15px auto 0 auto;
        line-height: 1.7;
    }

    /* ---------- Cards ---------- */

    .glass-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 22px;
        padding: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(16px);
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ---------- Upload ---------- */

    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.45);
        border: 1.5px dashed rgba(129, 140, 248, 0.45);
        border-radius: 18px;
        padding: 15px;
        transition: 0.3s;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #818cf8;
        background: rgba(99, 102, 241, 0.08);
    }

    /* ---------- Result ---------- */

    .result-real {
        background: linear-gradient(
            135deg,
            rgba(16, 185, 129, 0.15),
            rgba(6, 78, 59, 0.15)
        );
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
    }

    .result-fake {
        background: linear-gradient(
            135deg,
            rgba(239, 68, 68, 0.15),
            rgba(127, 29, 29, 0.15)
        );
        border: 1px solid rgba(248, 113, 113, 0.35);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
    }

    .result-icon {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .result-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .confidence {
        font-size: 38px;
        font-weight: 800;
        margin: 12px 0;
    }

    .confidence-label {
        color: #94a3b8;
        font-size: 13px;
    }

    /* ---------- Metrics ---------- */

    .metric-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
    }

    .metric-icon {
        font-size: 25px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 750;
        margin-top: 8px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
    }

    /* ---------- How it works ---------- */

    .step-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 18px;
        padding: 22px;
        height: 170px;
    }

    .step-number {
        display: inline-flex;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        align-items: center;
        justify-content: center;
        background: rgba(99, 102, 241, 0.18);
        color: #a5b4fc;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .step-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .step-text {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.5;
    }

    /* ---------- Footer ---------- */

    .custom-footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding-top: 30px;
    }

    .tech {
        color: #a5b4fc;
        font-weight: 600;
    }

    /* ---------- Image ---------- */

    [data-testid="stImage"] {
        border-radius: 18px;
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("deepfake_detector.keras")


try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error("⚠️ Model could not be loaded.")
    st.code(str(e))


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

    <div class="badge">
        🛡️ AI-POWERED MEDIA FORENSICS
    </div>

    <h1>DeepGuard</h1>

    <p>
        An intelligent deepfake detection system that analyzes facial
        images using deep learning to identify potential synthetic media.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN DETECTOR
# ============================================================

st.markdown("""
<div class="glass-card">

<div class="section-title">
    🔎 Analyze an Image
</div>

<div class="section-subtitle">
    Upload a JPG, JPEG, or PNG image containing a face.
</div>

</div>
""", unsafe_allow_html=True)

st.write("")


uploaded_file = st.file_uploader(
    "Upload your image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# ============================================================
# IMAGE ANALYSIS
# ============================================================

if uploaded_file is not None and model_loaded:

    image = Image.open(uploaded_file).convert("RGB")

    st.write("")

    col1, col2 = st.columns([1.05, 0.95], gap="large")

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    with col1:

        st.markdown("""
        <div class="glass-card">
        <div class="section-title">📷 Uploaded Image</div>
        <div class="section-subtitle">
            Image provided for forensic analysis
        </div>
        """, unsafe_allow_html=True)

        st.image(
            image,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    img = image.resize((224, 224))

    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = float(model.predict(img_array, verbose=0)[0][0])

    # Your model classes:
    # 0 = fake
    # 1 = real

    if prediction >= 0.5:

        confidence = prediction * 100

        result_html = f"""
        <div class="result-real">

            <div class="result-icon">🟢</div>

            <div class="result-title">
                REAL IMAGE
            </div>

            <div class="confidence">
                {confidence:.1f}%
            </div>

            <div class="confidence-label">
                Model confidence
            </div>

        </div>
        """

    else:

        confidence = (1 - prediction) * 100

        result_html = f"""
        <div class="result-fake">

            <div class="result-icon">🔴</div>

            <div class="result-title">
                POTENTIAL DEEPFAKE
            </div>

            <div class="confidence">
                {confidence:.1f}%
            </div>

            <div class="confidence-label">
                Model confidence
            </div>

        </div>
        """

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with col2:

        st.markdown("""
        <div class="glass-card">
        <div class="section-title">🧠 Detection Result</div>
        <div class="section-subtitle">
            Deep learning classification output
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )

        st.write("")

        # Probability
        st.markdown(
            f"**Real probability:** `{prediction * 100:.1f}%`"
        )

        st.progress(prediction)

        st.markdown(
            f"**Deepfake probability:** `{(1 - prediction) * 100:.1f}%`"
        )

        st.write("")

        st.info(
            "💡 This result is a model prediction and should not be "
            "treated as definitive proof of image authenticity."
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# MODEL INFORMATION
# ============================================================

st.write("")
st.divider()
st.write("")

st.markdown("""
<div style="text-align:center">

<h2>⚙️ Detection Pipeline</h2>

<p style="color:#94a3b8">
From image upload to deepfake classification
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="step-card">

        <div class="step-number">01</div>

        <div class="step-title">
            Image Upload
        </div>

        <div class="step-text">
            User provides a facial image for analysis.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:
    st.markdown("""
    <div class="step-card">

        <div class="step-number">02</div>

        <div class="step-title">
            Preprocessing
        </div>

        <div class="step-text">
            The image is resized to 224 × 224 pixels before inference.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:
    st.markdown("""
    <div class="step-card">

        <div class="step-number">03</div>

        <div class="step-title">
            Feature Extraction
        </div>

        <div class="step-text">
            MobileNetV2 extracts visual features from the input image.
        </div>

    </div>
    """, unsafe_allow_html=True)


with c4:
    st.markdown("""
    <div class="step-card">

        <div class="step-number">04</div>

        <div class="step-title">
            Classification
        </div>

        <div class="step-text">
            The model estimates whether the image belongs to the real or fake class.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TECHNOLOGY SECTION
# ============================================================

st.write("")
st.write("")
st.divider()
st.write("")

st.markdown("""
<div style="text-align:center">

<h2>🧩 Technology Stack</h2>

<p style="color:#94a3b8">
Technologies used to build the detection system
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🧠</div>
        <div class="metric-value">MobileNetV2</div>
        <div class="metric-label">Deep Learning Model</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🐍</div>
        <div class="metric-value">TensorFlow</div>
        <div class="metric-label">Model Framework</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">⚡</div>
        <div class="metric-value">Streamlit</div>
        <div class="metric-label">Web Interface</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">🖼️</div>
        <div class="metric-value">224×224</div>
        <div class="metric-label">Input Resolution</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# DISCLAIMER
# ============================================================

st.write("")
st.write("")

st.markdown("""
<div class="glass-card">

### ⚠️ Important Note

DeepGuard provides an automated prediction based on patterns
learned from its training dataset. Detection accuracy can vary
depending on image quality, manipulation techniques, compression,
and whether the image resembles the data used during training.

The system should therefore be used as an **assistive screening
tool rather than definitive proof of authenticity**.

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="custom-footer">

DeepGuard • Deepfake Detection System

<br><br>

Built with
<span class="tech">TensorFlow</span> •
<span class="tech">MobileNetV2</span> •
<span class="tech">Python</span> •
<span class="tech">Streamlit</span>

</div>
""", unsafe_allow_html=True)