# Model Files Location Reference

## Required Model Files

All model files should be placed in the `models/` directory:

### 1. **Ensemble Model**
- **File**: `final_ensemble_model.pkl`
- **Type**: Scikit-learn XGBoost/LightGBM/CatBoost ensemble
- **Purpose**: Main predictor for risk classification
- **Input**: Fused radiomics + CNN features

### 2. **CNN Embedding Model**
- **File**: `cnn_embedding_model.h5`
- **Type**: TensorFlow/Keras model
- **Purpose**: Extract CNN features from tumor images
- **Input**: 224x224 RGB image
- **Output**: Deep feature vector

### 3. **Radiomics Scaler**
- **File**: `radiomics_scaler.pkl`
- **Type**: Scikit-learn StandardScaler/MinMaxScaler
- **Purpose**: Normalize radiomics features
- **Input Shape**: (n_samples, n_radiomics_features)

### 4. **Label Encoder**
- **File**: `label_encoder.pkl`
- **Type**: Scikit-learn LabelEncoder
- **Purpose**: Encode/decode class labels
- **Classes**: ["High Risk", "Medium Risk", "Low Risk"]

### 5. **Fused Feature Selector**
- **File**: `fused_feature_selector.pkl`
- **Type**: Scikit-learn SelectKBest or similar
- **Purpose**: Select important fused features
- **Input**: Concatenated radiomics + CNN features

### 6. **CNN Feature Selector**
- **File**: `cnn_feature_selector.pkl`
- **Type**: Scikit-learn feature selector
- **Purpose**: Reduce CNN feature dimensionality
- **Input Shape**: (n_samples, 2048) or similar from CNN

## File Structure

```
LUNG_ONCOLOGY_AI/
└── models/
    ├── final_ensemble_model.pkl          (Required)
    ├── cnn_embedding_model.h5            (Required)
    ├── radiomics_scaler.pkl              (Required)
    ├── label_encoder.pkl                 (Required)
    ├── fused_feature_selector.pkl        (Required)
    ├── cnn_feature_selector.pkl          (Required)
    ├── hybrid_radiomics_cnn_model.h5     (Optional backup)
    └── README.md                         (This file)
```

## Model Training Pipeline

```
Raw Input
    ↓
[Image] → CNN Embedding Model → CNN Features → CNN Feature Selector → Selected CNN Features
    ↓
[CSV] → Radiomics Scaler → Scaled Radiomics Features → Feature Fusion
              ↓
         Fused Features → Fused Feature Selector → Selected Fused Features
                ↓
          Final Ensemble Model → Prediction
```

## How to Generate Model Files

### 1. CNN Embedding Model
```python
from tensorflow.keras import Sequential, layers

model = Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D(),
    # ... more layers ...
])
model.save("cnn_embedding_model.h5")
```

### 2. Ensemble Model
```python
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier

ensemble = VotingClassifier([
    ('xgb', XGBClassifier()),
    ('lgb', LGBMClassifier()),
])
ensemble.fit(X_train, y_train)

import joblib
joblib.dump(ensemble, "final_ensemble_model.pkl")
```

### 3. Scalers and Encoders
```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

scaler = StandardScaler()
scaler.fit(radiomics_features)
joblib.dump(scaler, "radiomics_scaler.pkl")

encoder = LabelEncoder()
encoder.fit(["High Risk", "Medium Risk", "Low Risk"])
joblib.dump(encoder, "label_encoder.pkl")
```

## Verification

Check if models are correctly formatted:

```bash
# List model files
ls -lh models/

# Verify pickle files
python -c "
import joblib
models = ['final_ensemble_model.pkl', 'radiomics_scaler.pkl', 
          'label_encoder.pkl', 'fused_feature_selector.pkl', 
          'cnn_feature_selector.pkl']
for m in models:
    try:
        joblib.load(f'models/{m}')
        print(f'✓ {m}')
    except Exception as e:
        print(f'✗ {m}: {e}')
"

# Verify H5 files
python -c "
from tensorflow.keras.models import load_model
try:
    model = load_model('models/cnn_embedding_model.h5')
    print(f'✓ cnn_embedding_model.h5')
    print(f'  Input shape: {model.input_shape}')
    print(f'  Output shape: {model.output_shape}')
except Exception as e:
    print(f'✗ cnn_embedding_model.h5: {e}')
"
```

## Troubleshooting

**Models not loading?**
- Check file paths are correct
- Verify TensorFlow version matches training version
- Ensure pickle files were created with same Python version

**Feature dimension mismatch?**
- Verify radiomics features match training count
- Check CNN output size matches selector input

**Out of memory?**
- Reduce model complexity
- Use GPU if available
- Batch process predictions

---

**Last Updated**: 2026-05-13
