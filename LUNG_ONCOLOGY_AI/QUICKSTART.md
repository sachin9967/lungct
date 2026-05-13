# 🚀 Quick Start Guide

## ⚡ 5-Minute Local Setup

### 1. **Prerequisites**
- Python 3.10+
- pip
- Git (for cloning)
- 4GB+ RAM
- 2GB+ disk space

### 2. **Clone/Navigate to Project**
```bash
cd LUNG_ONCOLOGY_AI
```

### 3. **Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 5. **Add Models**
Copy your trained models to `models/` directory:
- `final_ensemble_model.pkl`
- `cnn_embedding_model.h5`
- `radiomics_scaler.pkl`
- `label_encoder.pkl`
- `fused_feature_selector.pkl`
- `cnn_feature_selector.pkl`

### 6. **Run Application**
```bash
cd app
streamlit run streamlit_app.py
```

**✅ App runs at**: http://localhost:8501

---

## 🐳 Docker Quick Start (No Python Install Needed)

### Prerequisites
- Docker installed
- Docker running

### Steps

```bash
# Build image
docker build -t lung-ai .

# Run container
docker run -p 8501:8501 lung-ai
```

**✅ App runs at**: http://localhost:8501

---

## 🚀 Using Docker Compose

**Simplest method:**

```bash
docker-compose up
```

**✅ App runs at**: http://localhost:8501

To stop:
```bash
docker-compose down
```

---

## 📝 File Formats Expected

### Tumor Image (PNG/JPG)
- Format: PNG or JPEG
- Size: Any (auto-resized to 224x224)
- Color: RGB or Grayscale
- Example: `tumor_scan.png`

### Radiomics Features (CSV)
- Format: CSV with headers
- Columns: Feature names (any count)
- Row: One row of feature values
- Recommended: 20+ features

Example `radiomics.csv`:
```csv
feature_1,feature_2,feature_3,...
0.123,0.456,0.789,...
```

See `sample_inputs/sample_radiomics.csv` for reference.

---

## 🎯 Using the App

1. **Upload Image**: Choose your tumor CT scan (PNG/JPG)
2. **Upload CSV**: Choose radiomics features CSV
3. **Click "Make Prediction"**: Wait for processing
4. **View Results**:
   - Risk level (High/Medium/Low)
   - Confidence score (0-1)
   - Probability for each class

---

## 🔧 Configuration

Edit `app/config.json` to customize:

```json
{
    "image_size": 224,           # Image dimensions
    "classes": [                 # Risk classes
        "High Risk",
        "Low Risk",
        "Medium Risk"
    ],
    "num_classes": 3
}
```

---

## 📊 Expected Output

```json
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

## ⚠️ Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### "Model not found" Error
- Check `models/` directory has all files
- Verify file names match exactly:
  - `final_ensemble_model.pkl`
  - `cnn_embedding_model.h5`
  - etc.

### App crashes when predicting
- Check image format (must be PNG/JPG)
- Verify CSV has correct number of features
- Check system RAM (needs 4GB+)

### Port 8501 already in use
```bash
# Use different port
streamlit run app/streamlit_app.py --server.port 8502
```

### Image too small/large
- Images are auto-resized to 224x224
- Any input size works

---

## 🎓 Next Steps

After successful local run:

1. **Deploy to Cloud**:
   - Streamlit Cloud (easiest)
   - Docker + AWS/GCP/Azure
   - See `DEPLOYMENT_GUIDE.md`

2. **Optimize Models**:
   - Reduce model size
   - Use GPU acceleration
   - Implement caching

3. **Add Features**:
   - Export predictions
   - Add batch processing
   - Integrate with hospital systems

---

## 📚 Documentation

- **Full Deployment**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Model Info**: See [models/README.md](models/README.md)
- **Project Info**: See [README.md](README.md)

---

## 🆘 Need Help?

1. Check app logs:
   ```bash
   docker logs lung-ai  # For Docker
   # Or terminal output for local run
   ```

2. Verify models:
   ```bash
   ls -la models/
   ```

3. Test prediction:
   ```python
   from app.predict import predict_lung_cancer
   result = predict_lung_cancer("path/to/image.png", "path/to/radiomics.csv")
   print(result)
   ```

---

**Version**: 1.0  
**Last Updated**: 2026-05-13
