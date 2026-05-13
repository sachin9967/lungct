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
    try:
        ensemble = joblib.load(ENSEMBLE_PATH)
        logger.info("Ensemble model loaded")
        
        embedding_model = load_model(EMBEDDING_MODEL_PATH)
        logger.info("CNN embedding model loaded")
        
        scaler = joblib.load(SCALER_PATH)
        logger.info("Radiomics scaler loaded")
        
        encoder = joblib.load(ENCODER_PATH)
        logger.info("Label encoder loaded")
        
        fusion_selector = joblib.load(FUSION_SELECTOR_PATH)
        logger.info("Fusion feature selector loaded")
        
        cnn_selector = joblib.load(CNN_SELECTOR_PATH)
        logger.info("CNN feature selector loaded")
        
        return {
            "ensemble": ensemble,
            "embedding_model": embedding_model,
            "scaler": scaler,
            "encoder": encoder,
            "fusion_selector": fusion_selector,
            "cnn_selector": cnn_selector
        }
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        raise

# Load models on startup
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
