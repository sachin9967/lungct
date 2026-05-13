import os
import json
import logging

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "config.json"
)

def load_config():
    """Load configuration from config.json"""
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config

def ensure_directories():
    """Ensure required directories exist."""
    dirs = [
        "../uploads",
        "../outputs"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        logger.info(f"Directory ensured: {d}")

def get_file_path(directory, filename):
    """Get safely joined file path."""
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, directory, filename)
    return full_path

def format_confidence(confidence):
    """Format confidence score."""
    return f"{confidence:.4f}"

def format_result(prediction, confidence, probabilities):
    """Format prediction result."""
    return {
        "prediction": prediction,
        "confidence": float(confidence),
        "probabilities": {
            cls: float(prob)
            for cls, prob in probabilities.items()
        }
    }
