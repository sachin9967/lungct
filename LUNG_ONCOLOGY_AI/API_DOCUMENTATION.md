# 🔌 API DOCUMENTATION

## Python Module API

### Import the Predictor

```python
from app.predict import predict_lung_cancer
```

### Function Signature

```python
def predict_lung_cancer(image_path: str, radiomics_csv_path: str) -> dict:
    """
    Predict lung cancer risk from image and radiomics features.
    
    Args:
        image_path (str): Path to tumor CT image (PNG/JPG)
        radiomics_csv_path (str): Path to radiomics features CSV
        
    Returns:
        dict: Prediction result with keys:
            - 'prediction' (str): Risk level
            - 'confidence' (float): Confidence score 0-1
            - 'probabilities' (dict): Class probabilities
            
    Raises:
        ValueError: If image is invalid
        FileNotFoundError: If files don't exist
        Exception: If models not loaded
    """
```

### Example Usage

```python
from app.predict import predict_lung_cancer

# Make prediction
result = predict_lung_cancer(
    image_path="path/to/tumor.png",
    radiomics_csv_path="path/to/radiomics.csv"
)

# Access results
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.4f}")
print(f"Probabilities: {result['probabilities']}")
```

### Return Value Example

```python
{
    "prediction": "High Risk",
    "confidence": 0.9234,
    "probabilities": {
        "High Risk": 0.9234,
        "Medium Risk": 0.0512,
        "Low Risk": 0.0254
    }
}
```

---

## Web API (Future)

### REST Endpoint (if Flask is enabled)

```http
POST /api/predict
Content-Type: multipart/form-data

{
    "image": <binary PNG/JPG file>,
    "radiomics_csv": <binary CSV file>
}
```

### Response

```json
{
    "status": "success",
    "prediction": "High Risk",
    "confidence": 0.9234,
    "probabilities": {
        "High Risk": 0.9234,
        "Medium Risk": 0.0512,
        "Low Risk": 0.0254
    },
    "timestamp": "2026-05-13T10:30:00Z",
    "processing_time_ms": 4532
}
```

### Error Response

```json
{
    "status": "error",
    "error": "Invalid image file",
    "details": "Image could not be read with OpenCV",
    "timestamp": "2026-05-13T10:30:00Z"
}
```

---

## Integration Examples

### 1. Batch Prediction

```python
import os
from app.predict import predict_lung_cancer

# Process all images in a directory
for image_file in os.listdir("images/"):
    image_path = os.path.join("images/", image_file)
    csv_path = os.path.join("data/", image_file.replace(".png", ".csv"))
    
    try:
        result = predict_lung_cancer(image_path, csv_path)
        print(f"{image_file}: {result['prediction']} ({result['confidence']:.4f})")
    except Exception as e:
        print(f"Error processing {image_file}: {e}")
```

### 2. Database Integration

```python
import sqlite3
from app.predict import predict_lung_cancer

conn = sqlite3.connect("predictions.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        image_file TEXT,
        prediction TEXT,
        confidence REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

# Make prediction and store
result = predict_lung_cancer("tumor.png", "features.csv")
cursor.execute(
    "INSERT INTO predictions (image_file, prediction, confidence) "
    "VALUES (?, ?, ?)",
    ("tumor.png", result['prediction'], result['confidence'])
)
conn.commit()
```

### 3. Web Framework Integration (Flask)

```python
from flask import Flask, request, jsonify
from app.predict import predict_lung_cancer
import os

app = Flask(__name__)

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files or 'csv' not in request.files:
        return jsonify({"error": "Missing files"}), 400
    
    image_file = request.files['image']
    csv_file = request.files['csv']
    
    # Save temporarily
    image_path = os.path.join("/tmp", image_file.filename)
    csv_path = os.path.join("/tmp", csv_file.filename)
    
    image_file.save(image_path)
    csv_file.save(csv_path)
    
    try:
        result = predict_lung_cancer(image_path, csv_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. Hospital Information System Integration

```python
# DICOM file to Prediction
import pydicom
import cv2
import numpy as np
from app.predict import predict_lung_cancer

def process_dicom(dicom_file):
    # Load DICOM
    dicom = pydicom.dcmread(dicom_file)
    
    # Convert to image
    image_array = dicom.pixel_array
    image_array = cv2.normalize(image_array, None, 0, 255, cv2.NORM_MINMAX)
    
    # Save as PNG
    png_path = "/tmp/tumor.png"
    cv2.imwrite(png_path, image_array)
    
    # Get radiomics (separate process)
    radiomics_csv = "/path/to/radiomics.csv"
    
    # Predict
    result = predict_lung_cancer(png_path, radiomics_csv)
    return result
```

---

## Configuration & Customization

### Load Configuration

```python
from app.utils import load_config

config = load_config()
print(config['image_size'])  # 224
print(config['classes'])     # ['High Risk', 'Low Risk', 'Medium Risk']
```

### Modify Configuration

Edit `app/config.json`:

```json
{
    "image_size": 224,
    "classes": ["High Risk", "Low Risk", "Medium Risk"],
    "num_classes": 3,
    "custom_setting": "value"
}
```

### Access in Code

```python
with open("app/config.json") as f:
    import json
    config = json.load(f)
    
# Use config
IMG_SIZE = config['image_size']
CLASSES = config['classes']
```

---

## Error Handling

### Common Exceptions

```python
from app.predict import predict_lung_cancer

try:
    result = predict_lung_cancer(image_path, csv_path)
    
except ValueError as e:
    print(f"Validation error: {e}")
    # Handle invalid image
    
except FileNotFoundError as e:
    print(f"File not found: {e}")
    # Handle missing models or input files
    
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle other errors
```

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting prediction")
result = predict_lung_cancer(image_path, csv_path)
logger.info(f"Prediction: {result['prediction']}")
```

---

## Performance Tuning

### Cache Models

```python
from app.predict import MODELS

# Models are already cached
# Re-use MODELS dict for faster subsequent calls
print(MODELS['ensemble'])  # Access loaded ensemble
```

### Batch Processing

```python
import time
from app.predict import predict_lung_cancer

images = [...]
batch_results = []

start = time.time()

for image in images:
    result = predict_lung_cancer(image, csv)
    batch_results.append(result)

elapsed = time.time() - start
print(f"Processed {len(images)} in {elapsed:.2f}s")
print(f"Average time per prediction: {elapsed/len(images):.2f}s")
```

---

## Advanced Usage

### Model Inspection

```python
from app.predict import MODELS

# Get model information
ensemble = MODELS['ensemble']
print(f"Model type: {type(ensemble)}")
print(f"Classes: {ensemble.classes_}")
print(f"Estimators: {len(ensemble.estimators_)}")

# Get feature importances
if hasattr(ensemble, 'feature_importances_'):
    importances = ensemble.feature_importances_
    print(f"Top features: {importances.argsort()[::-1][:10]}")
```

### Input Validation

```python
from app.preprocessing import preprocess_image
import cv2

def validate_inputs(image_path, csv_path):
    # Check image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Invalid image file")
    
    # Check CSV
    import pandas as pd
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            raise ValueError("CSV is empty")
    except Exception as e:
        raise ValueError(f"Invalid CSV: {e}")
    
    return True

# Use validation
validate_inputs("tumor.png", "features.csv")
result = predict_lung_cancer("tumor.png", "features.csv")
```

### Streaming Predictions

```python
# Process and stream results
import json

def stream_predictions(image_csv_pairs):
    for image_path, csv_path in image_csv_pairs:
        result = predict_lung_cancer(image_path, csv_path)
        
        # Stream as JSON lines
        print(json.dumps({
            "image": image_path,
            **result
        }))
```

---

## Testing the API

### Simple Test

```python
from app.predict import predict_lung_cancer

# Test with sample files
result = predict_lung_cancer(
    "sample_inputs/sample_image.png",
    "sample_inputs/sample_radiomics.csv"
)

assert "prediction" in result
assert "confidence" in result
assert "probabilities" in result
print("✅ API test passed")
```

### Unit Test Template

```python
import unittest
from app.predict import predict_lung_cancer

class TestPredictAPI(unittest.TestCase):
    
    def test_prediction_structure(self):
        result = predict_lung_cancer("image.png", "radiomics.csv")
        
        self.assertIn("prediction", result)
        self.assertIn("confidence", result)
        self.assertIn("probabilities", result)
    
    def test_confidence_range(self):
        result = predict_lung_cancer("image.png", "radiomics.csv")
        
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
    
    def test_valid_prediction_class(self):
        result = predict_lung_cancer("image.png", "radiomics.csv")
        
        valid_classes = ["High Risk", "Medium Risk", "Low Risk"]
        self.assertIn(result['prediction'], valid_classes)

if __name__ == '__main__':
    unittest.main()
```

---

## Versioning

### API Version

```python
# Add to app/predict.py
__version__ = "1.0.0"

# Check version
from app.predict import __version__
print(f"API Version: {__version__}")
```

### Model Version

```python
# Store in models/metadata.json
{
    "ensemble_version": "1.0",
    "cnn_version": "2.0",
    "training_date": "2026-05-01",
    "accuracy": 0.92
}
```

---

##Performance Metrics

### Profiling

```python
import cProfile
from app.predict import predict_lung_cancer

# Profile prediction
profiler = cProfile.Profile()
profiler.enable()

result = predict_lung_cancer("image.png", "radiomics.csv")

profiler.disable()
profiler.print_stats(sort='cumtime')
```

### Benchmarking

```python
import time
from app.predict import predict_lung_cancer

times = []
for _ in range(10):
    start = time.time()
    result = predict_lung_cancer("image.png", "radiomics.csv")
    times.append(time.time() - start)

print(f"Mean: {sum(times)/len(times):.3f}s")
print(f"Min: {min(times):.3f}s")
print(f"Max: {max(times):.3f}s")
```

---

## Support & Debugging

### Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("app.predict")

# Run prediction
result = predict_lung_cancer("image.png", "radiomics.csv")
# All debug logs will print
```

### Check Model Health

```python
from app.predict import MODELS

models_to_check = [
    'ensemble', 'embedding_model', 'scaler', 
    'encoder', 'fusion_selector', 'cnn_selector'
]

for model_name in models_to_check:
    model = MODELS.get(model_name)
    print(f"✓ {model_name}" if model else f"✗ {model_name} MISSING")
```

---

**API Version**: 1.0  
**Last Updated**: 2026-05-13
