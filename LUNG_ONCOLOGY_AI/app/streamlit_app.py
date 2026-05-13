import os
import json
import streamlit as st
import logging
from pathlib import Path

from predict import predict_lung_cancer
from utils import ensure_directories, load_config

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Lung Oncology AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .title-text {
        text-align: center;
        color: #1f77b4;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# INITIALIZE
# ============================================================

ensure_directories()
config = load_config()

# ============================================================
# TITLE & DESCRIPTION
# ============================================================

st.markdown(
    "<h1 class='title-text'>🫁 Lung Oncology AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='result-box'>
    <b>Hybrid CNN + Radiomics Cancer Risk Prediction System</b>
    
    Upload a tumor CT image and radiomics features to get a cancer risk assessment.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("📋 Information")
    st.info("### Project Overview\n"
            "This system combines:\n"
            "- **CNN**: Deep learning image analysis\n"
            "- **Radiomics**: Quantitative feature extraction\n"
            "- **Ensemble**: Hybrid prediction model\n\n"
            "**Risk Classes:**\n"
            f"- {config['classes'][0]}\n"
            f"- {config['classes'][1]}\n"
            f"- {config['classes'][2]}")

# ============================================================
# FILE UPLOADS
# ============================================================

st.header("📤 Upload Files")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Tumor Image")
    image_file = st.file_uploader(
        "Upload Tumor CT Scan (PNG/JPG)",
        type=["png", "jpg", "jpeg"],
        key="image_upload"
    )

with col2:
    st.subheader("2️⃣ Radiomics Features")
    csv_file = st.file_uploader(
        "Upload Radiomics CSV",
        type=["csv"],
        key="csv_upload"
    )

# ============================================================
# PREVIEW UPLOADED FILES
# ============================================================

if image_file and csv_file:
    st.divider()
    st.header("📊 Preview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tumor Image")
        st.image(image_file, use_column_width=True)
    
    with col2:
        st.subheader("Radiomics Data")
        import pandas as pd
        csv_df = pd.read_csv(csv_file)
        st.dataframe(csv_df, use_container_width=True)
        st.write(f"**Shape:** {csv_df.shape[0]} rows × {csv_df.shape[1]} columns")

# ============================================================
# PREDICTION
# ============================================================

if image_file and csv_file:
    st.divider()
    
    if st.button("🚀 Make Prediction", use_container_width=True):
        try:
            # Create upload directory
            upload_dir = os.path.join(
                os.path.dirname(__file__),
                "../uploads"
            )
            os.makedirs(upload_dir, exist_ok=True)

            # Save files
            image_path = os.path.join(upload_dir, image_file.name)
            csv_path = os.path.join(upload_dir, csv_file.name)

            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

            with open(csv_path, "wb") as f:
                f.write(csv_file.getbuffer())

            logger.info(f"Files saved: {image_path}, {csv_path}")

            # Make prediction
            with st.spinner("🔄 Processing... Analyzing tumor and extracting features..."):
                result = predict_lung_cancer(image_path, csv_path)

            # Display results
            st.header("🎯 Results")
            
            # Main prediction
            risk_level = result['prediction']
            confidence = result['confidence']
            
            # Color code based on risk
            if "High" in risk_level:
                color = "🔴"
            elif "Medium" in risk_level:
                color = "🟡"
            else:
                color = "🟢"
            
            st.success(f"{color} **Prediction:** {risk_level}")
            
            # Confidence
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence Score", f"{confidence:.4f}", "")
            
            # Class probabilities
            st.subheader("📈 Class Probabilities")
            probs_df = pd.DataFrame(
                list(result['probabilities'].items()),
                columns=['Risk Class', 'Probability']
            )
            probs_df['Probability'] = probs_df['Probability'].round(4)
            st.bar_chart(probs_df.set_index('Risk Class'))
            
            st.table(probs_df)
            
            # Detailed results JSON
            with st.expander("📋 Detailed Results (JSON)"):
                st.json(result)

        except Exception as e:
            st.error(f"❌ Error during prediction: {str(e)}")
            logger.error(f"Prediction error: {e}")

else:
    if not image_file or not csv_file:
        st.info("👆 Please upload both the tumor image and radiomics CSV file to proceed")

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
    <p>Lung Oncology AI v1.0 | Hybrid CNN + Radiomics Model</p>
    <p>For medical use only - consult healthcare professionals for clinical decisions</p>
    </div>
    """,
    unsafe_allow_html=True
)
