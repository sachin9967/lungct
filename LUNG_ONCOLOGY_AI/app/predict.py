import joblib
import numpy as np
import pandas as pd
import os
import logging

from tensorflow.keras.models import load_model
from preprocessing import preprocess_image

logger = logging.getLogger(__name__)

# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "../models")

ENSEMBLE_PATH = os.path.join(MODELS_DIR, "final_ensemble_model.pkl")
EMBEDDING_MODEL_PATH = os.path.join(MODELS_DIR, "cnn_embedding_model.h5")
SCALER_PATH = os.path.join(MODELS_DIR, "radiomics_scaler.pkl")
ENCODER_PATH = os.path.join(MODELS_DIR, "label_encoder.pkl")
FUSION_SELECTOR_PATH = os.path.join(MODELS_DIR, "fused_feature_selector.pkl")
CNN_SELECTOR_PATH = os.path.join(MODELS_DIR, "cnn_feature_selector.pkl")

# ============================================================
# LOAD MODELS
# ============================================================

def load_all_models():
    """Load all required models and scalers."""
    models = {}
    
    try:
        ensemble = joblib.load(ENSEMBLE_PATH)
        models["ensemble"] = ensemble
        logger.info("✅ Ensemble model loaded")
    except Exception as e:
        logger.warning(f"⚠️ Ensemble model not found: {e}")
        
    try:
        embedding_model = load_model(EMBEDDING_MODEL_PATH)
        models["embedding_model"] = embedding_model
        logger.info("✅ CNN embedding model loaded")
    except Exception as e:
        logger.warning(f"⚠️ CNN embedding model not found: {e}")
        logger.warning("⚠️ Please add cnn_embedding_model.h5 to /models/ directory")
        
    try:
        scaler = joblib.load(SCALER_PATH)
        models["scaler"] = scaler
        logger.info("✅ Radiomics scaler loaded")
    except Exception as e:
        logger.warning(f"⚠️ Radiomics scaler not found: {e}")
        
    try:
        encoder = joblib.load(ENCODER_PATH)
        models["encoder"] = encoder
        logger.info("✅ Label encoder loaded")
    except Exception as e:
        logger.warning(f"⚠️ Label encoder not found: {e}")
        
    try:
        fusion_selector = joblib.load(FUSION_SELECTOR_PATH)
        models["fusion_selector"] = fusion_selector
        logger.info("✅ Fusion feature selector loaded")
    except Exception as e:
        logger.warning(f"⚠️ Fusion feature selector not found: {e}")
        
    try:
        cnn_selector = joblib.load(CNN_SELECTOR_PATH)
        models["cnn_selector"] = cnn_selector
        logger.info("✅ CNN feature selector loaded")
    except Exception as e:
        logger.warning(f"⚠️ CNN feature selector not found: {e}")
    
    return models

# Load models on startup (non-blocking)
MODELS = load_all_models()

# ============================================================
# PREDICT FUNCTION
# ============================================================

def predict_lung_cancer(image_path, radiomics_csv_path):
    """
    Predict lung cancer risk from image and radiomics features.
    
    Args:
        image_path (str): Path to tumor image
        radiomics_csv_path (str): Path to radiomics CSV file
        
    Returns:
        dict: Prediction results with confidence and probabilities
    """
    # Validate all required models are loaded
    required_models = ["embedding_model", "cnn_selector", "scaler", "fusion_selector", "ensemble", "encoder"]
    missing_models = [m for m in required_models if m not in MODELS]
    
    if missing_models:
        error_msg = f"Missing models: {', '.join(missing_models)}. Please ensure all model files are in /models/ directory."
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        # --------------------------------------------------------
        # IMAGE PREPROCESSING
        # --------------------------------------------------------
        logger.info(f"Preprocessing image: {image_path}")
        image = preprocess_image(image_path)

        # --------------------------------------------------------
        # CNN EMBEDDINGS
        # --------------------------------------------------------
        logger.info("Extracting CNN features")
        cnn_features = MODELS["embedding_model"].predict(
            image,
            verbose=0
        )

        cnn_features = MODELS["cnn_selector"].transform(cnn_features)
        logger.info(f"CNN features shape: {cnn_features.shape}")

        # --------------------------------------------------------
        # RADIOMICS
        # --------------------------------------------------------
        logger.info(f"Loading radiomics features: {radiomics_csv_path}")
        radio_df = pd.read_csv(radiomics_csv_path)
        logger.info(f"Radiomics features shape: {radio_df.shape}")

        radio_scaled = MODELS["scaler"].transform(radio_df)

        # --------------------------------------------------------
        # FEATURE FUSION
        # --------------------------------------------------------
        logger.info("Fusing features")
        fused = np.concatenate(
            [radio_scaled, cnn_features],
            axis=1
        )
        logger.info(f"Fused features shape: {fused.shape}")

        fused = MODELS["fusion_selector"].transform(fused)
        logger.info(f"Selected fused features shape: {fused.shape}")

        # --------------------------------------------------------
        # PREDICTION
        # --------------------------------------------------------
        logger.info("Making prediction")
        pred = MODELS["ensemble"].predict(fused)[0]
        probs = MODELS["ensemble"].predict_proba(fused)[0]

        label = MODELS["encoder"].inverse_transform([pred])[0]
        confidence = float(np.max(probs))

        result = {
            "prediction": label,
            "confidence": confidence,
            "probabilities": {
                cls: float(prob)
                for cls, prob in zip(
                    MODELS["encoder"].classes_,
                    probs
                )
            }
        }
        
        logger.info(f"Prediction result: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise
