# 📚 COMPLETE PROJECT GUIDE

## 🎯 Project Overview

**Lung Oncology AI** is a production-ready web application for lung cancer risk assessment using:
- **CNN**: Deep learning image feature extraction
- **Radiomics**: Quantitative medical imaging analysis
- **Ensemble Learning**: Hybrid ML prediction model

Users upload a tumor CT image and radiomics features to get instant risk classification.

---

## 📂 Project Structure

```
LUNG_ONCOLOGY_AI/
│
├── 📄 README.md                          # Project overview
├── 📄 QUICKSTART.md                      # 5-minute setup guide
├── 📄 DEPLOYMENT_GUIDE.md               # Full deployment options
├── 📄 DEPLOYMENT_CHECKLIST.md           # Pre-deployment verification
├── 📄 PROJECT_STRUCTURE.md              # This file
│
├── 📋 requirements.txt                   # Python dependencies
├── 📋 runtime.txt                        # Python version
├── 🐳 Dockerfile                         # Docker image definition
├── 🐳 docker-compose.yml                 # Docker compose setup
│
├── 🔧 setup.sh                           # Automated setup script
│
├── 📂 app/                               # Main application
│   ├── 🎨 streamlit_app.py              # Web UI (main entry point)
│   ├── 🔮 predict.py                    # Prediction pipeline
│   ├── 🖼️ preprocessing.py              # Image preprocessing
│   ├── 🛠️ utils.py                      # Utility functions
│   └── ⚙️ config.json                   # Configuration
│
├── 📂 models/                            # ML Models directory
│   ├── 📘 README.md                      # Model documentation
│   ├── 🤖 final_ensemble_model.pkl      # Ensemble predictor
│   ├── 🧠 cnn_embedding_model.h5        # CNN feature extractor
│   ├── 📊 radiomics_scaler.pkl          # Feature normalization
│   ├── 🏷️ label_encoder.pkl             # Label encoding
│   ├── ✨ fused_feature_selector.pkl   # Feature selection
│   └── 🎯 cnn_feature_selector.pkl     # CNN feature selection
│
├── 📂 uploads/                           # User uploaded files
├── 📂 outputs/                           # Generated predictions
└── 📂 sample_inputs/                     # Example files
    └── sample_radiomics.csv              # Sample CSV template
```

---

## 🚀 Quick Start (Choose One)

### Option 1: Local Python (Fastest)
```bash
cd LUNG_ONCOLOGY_AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app && streamlit run streamlit_app.py
```

### Option 2: Docker (No Python needed)
```bash
cd LUNG_ONCOLOGY_AI
docker build -t lung-ai .
docker run -p 8501:8501 lung-ai
```

### Option 3: Docker Compose (Easiest)
```bash
cd LUNG_ONCOLOGY_AI
docker-compose up
```

👉 **Access**: http://localhost:8501

---

## 📋 What Each File Does

### Root Level Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python packages needed |
| `runtime.txt` | Python version for cloud deployment |
| `Dockerfile` | Docker image builder |
| `docker-compose.yml` | Multi-container orchestration |
| `setup.sh` | Automated environment setup |

### Application Files (`app/` folder)

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Web interface - **START HERE** |
| `predict.py` | Prediction logic & model loading |
| `preprocessing.py` | Image preprocessing & normalization |
| `utils.py` | Helper functions & config loading |
| `config.json` | Application settings |

### Model Files (`models/` folder)

| File | Type | Purpose |
|------|------|---------|
| `final_ensemble_model.pkl` | Scikit-learn | Main predictor |
| `cnn_embedding_model.h5` | TensorFlow | Extract CNN features |
| `radiomics_scaler.pkl` | Scikit-learn | Normalize radiomics |
| `label_encoder.pkl` | Scikit-learn | Encode class labels |
| `fused_feature_selector.pkl` | Scikit-learn | Select top features |
| `cnn_feature_selector.pkl` | Scikit-learn | Reduce CNN dims |

---

## 🧠 How It Works

### Data Flow

```
User Upload
    ↓
[Image] ──→ OpenCV ──→ Resize to 224×224 ──→ Normalize ──→ CNN Model ──→ Extract Features
[CSV]   ──→ Pandas ──→ Read Features ────────→ Scale ────→ Feature Selector
    ↓
Concatenate Features → Fusion Processing → Final Selection
    ↓
Ensemble Model (XGBoost/LightGBM/CatBoost)
    ↓
Risk Prediction + Confidence + Class Probabilities
    ↓
Display Results in Web UI
```

### Prediction Result

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

## 📦 What You Need to Add

### 1. Model Files (Required)

Copy your trained models to `models/` directory:

```bash
models/
├── final_ensemble_model.pkl
├── cnn_embedding_model.h5
├── radiomics_scaler.pkl
├── label_encoder.pkl
├── fused_feature_selector.pkl
└── cnn_feature_selector.pkl
```

**Size estimates:**
- Ensemble: 1-10 MB
- CNN Model: 50-500 MB
- Scalers/Encoders: < 1 MB each

See [models/README.md](models/README.md) for generation details.

### 2. Training Data Format

**Tumor Image:**
- Format: PNG or JPEG
- Size: Any (auto-resized to 224×224)
- Color: RGB or grayscale

**Radiomics CSV:**
- Format: CSV with headers
- Example:
  ```csv
  feature_1,feature_2,feature_3,...
  0.123,0.456,0.789,...
  ```

---

## ⚙️ Configuration

Edit `app/config.json`:

```json
{
    "image_size": 224,
    "classes": [
        "High Risk",
        "Low Risk", 
        "Medium Risk"
    ],
    "num_classes": 3
}
```

---

## 🚢 Deployment Options

### 1. **Streamlit Cloud** (Easiest)
✅ Free tier available  
✅ Auto-scaling  
❌ Cold starts (30-60s)

[See DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### 2. **Docker + AWS/GCP/Azure**
✅ Production-ready  
✅ Full control  
❌ More setup required

[See DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### 3. **Local Server**
✅ Simplest  
✅ No cloud costs  
❌ Always-on requirement

[See QUICKSTART.md](QUICKSTART.md)

---

##🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Model not found"
```bash
ls -la models/  # Check files exist
file models/*.pkl  # Verify formats
```

### "Image error"
- Ensure image is PNG/JPG
- Try a different image
- Check file not corrupted

### "CSV error"
- Verify CSV has headers
- Check feature count matches training
- See `sample_inputs/sample_radiomics.csv`

### "Out of memory"
- Close other apps
- Reduce batch size
- Use smaller images

### "Slow predictions"
- Check CPU/GPU usage
- Verify model files loaded
- Try GPU acceleration

---

## 📊 Performance Targets

| Metric | Target |
|--------|--------|
| Startup time | < 30s |
| Prediction latency | < 10s |
| Memory usage | < 2GB |
| CPU usage | < 80% |
| Concurrent users | 5+ |

---

## 🔒 Security Best Practices

1. **File Validation**
   - Check file types before processing
   - Limit upload size
   - Validate CSV format

2. **Model Security**
   - Don't expose model files
   - Use `.gitignore` properly
   - Version control with Git LFS

3. **Deployment**
   - Use HTTPS in production
   - Enable authentication
   - Set resource limits
   - Monitor logs

---

## 📝 Important Notes

⚠️ **Medical Disclaimer**
- System is for research/clinical support
- Always consult healthcare professionals
- Not a replacement for medical diagnosis

⚠️ **Data Privacy**
- Configure upload/storage properly
- Follow HIPAA/GDPR if applicable
- Implement access controls

⚠️ **Model Updates**
- Track model versions
- Test before deploying
- Keep backup of previous versions

---

## 🎓 Next Steps

1. **Get Started**: [QUICKSTART.md](QUICKSTART.md)
2. **Full Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. **Model Info**: [models/README.md](models/README.md)
4. **Pre-Deployment**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 📞 Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **TensorFlow Docs**: https://www.tensorflow.org/
- **Scikit-learn Docs**: https://scikit-learn.org/
- **Docker Docs**: https://docs.docker.com/

---

## 📈 Project Statistics

- **Lines of Code**: ~800
- **Configuration Files**: 3
- **Docker Setup**: 1 image + compose
- **Supported Platforms**: 5+ (Local, Docker, Streamlit Cloud, AWS, GCP, Azure)
- **Python Version**: 3.10+
- **ML Frameworks**: TensorFlow, Scikit-learn, XGBoost, LightGBM, CatBoost

---

## 🎯 Success Criteria

✅ Application starts without errors  
✅ Files upload successfully  
✅ Predictions complete < 10 seconds  
✅ Results display correctly  
✅ Docker deployment works  
✅ Cloud deployment accessible  

---

**Version**: 1.0  
**Status**: Production Ready  
**Last Updated**: 2026-05-13

For questions or issues, refer to the comprehensive guides linked above.
