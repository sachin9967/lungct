# 🚀 DEPLOYMENT QUICK REFERENCE

## Commands at a Glance

### Local Deployment
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cd app && streamlit run streamlit_app.py
```

### Docker Deployment
```bash
docker build -t lung-ai .
docker run -p 8501:8501 lung-ai
# OR
docker-compose up
```

### Installation Check
```bash
python --version  # Should be 3.10+
pip list | grep -E "tensorflow|streamlit|pandas"
ls models/  # Should show all 6 model files
```

---

## Critical Checklist

- [ ] Models in `models/` directory
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Python 3.10+ installed
- [ ] Port 8501 available
- [ ] 4GB+ RAM available
- [ ] 2GB+ disk space available

---

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Module not found" | `pip install -r requirements.txt` |
| "Model not found" | `ls models/` - check all 6 files exist |
| "Port 8501 in use" | `streamlit run streamlit_app.py --server.port 8502` |
| "Out of memory" | Close other apps / upgrade server |
| "CSV error" | Check CSV headers and feature count |
| "Image error" | Verify image is PNG/JPG and not corrupted |

---

## URL References

| Component | URL |
|-----------|-----|
| Local App | http://localhost:8501 |
| Docker App | http://localhost:8501 |
| Streamlit Cloud | https://share.streamlit.io |
| AWS Console | https://console.aws.amazon.com |
| GCP Console | https://console.cloud.google.com |

---

## File Locations

### Configuration
- Image size: `app/config.json` → `image_size`
- Classes: `app/config.json` → `classes`

### Models
- Ensemble: `models/final_ensemble_model.pkl`
- CNN: `models/cnn_embedding_model.h5`
- Scaler: `models/radiomics_scaler.pkl`
- Encoder: `models/label_encoder.pkl`

### Uploads
- Images saved: `uploads/`
- Predictions: `outputs/`

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Image Input | 224×224 px |
| Classes | 3 (High/Medium/Low Risk) |
| Prediction Time | < 10 seconds |
| Memory Usage | < 2GB |
| Startup Time | < 30 seconds |
| Recommended RAM | 4GB+ |

---

## Environment Variables (Docker)

```dockerfile
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

---

## Docker Commands

```bash
# Build
docker build -t lung-ai .

# Run
docker run -p 8501:8501 lung-ai

# Run with volumes
docker run -p 8501:8501 -v $(pwd)/models:/app/models lung-ai

# Stop
docker stop <container-id>

# View logs
docker logs <container-id>

# Remove image
docker rmi lung-ai
```

---

## Model File Sizes (Approx)

- `final_ensemble_model.pkl`: 1-10 MB
- `cnn_embedding_model.h5`: 50-500 MB
- `radiomics_scaler.pkl`: < 1 MB
- `label_encoder.pkl`: < 1 MB
- `fused_feature_selector.pkl`: < 1 MB
- `cnn_feature_selector.pkl`: < 1 MB

**Total**: ~100 MB (depending on CNN model)

---

## CSV Format Example

```csv
feature_1,feature_2,feature_3,feature_4,feature_5
0.1234,0.5678,0.2341,0.4567,0.3456
```

Minimum: 1 row, 1+ columns  
Recommended: 20+ features

---

## Expected Output

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

## Performance Optimization Tips

1. Use GPU if available
2. Pre-warm models on startup
3. Implement result caching
4. Use smaller batch sizes
5. Monitor memory usage

---

## Deployment Comparison

| Platform | Setup | Cost | Speed | Support |
|----------|-------|------|-------|---------|
| Local | Easy | Free | Fast | Self |
| Docker | Medium | Free | Fast | Self |
| Streamlit | Easy | Free | Slow | Community |
| AWS | Hard | Paid | Fast | AWS |
| GCP | Hard | Paid | Fast | GCP |
| Azure | Hard | Paid | Fast | Azure |

---

## Documentation Files

- `README.md` - Project overview
- `QUICKSTART.md` - 5-minute setup
- `DEPLOYMENT_GUIDE.md` - Full deployment options
- `DEPLOYMENT_CHECKLIST.md` - Pre-production verification
- `PROJECT_STRUCTURE.md` - Complete guide
- `models/README.md` - Model specifications
- `REFERENCE.md` - This file

---

## Emergency Commands

```bash
# Reset everything
rm -rf venv uploads outputs __pycache__ *.pyc

# Fresh install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test models
python -c "
import joblib
models = ['final_ensemble_model.pkl', 'radiomics_scaler.pkl']
for m in models:
    print(f'Testing {m}...')
    joblib.load(f'models/{m}')
    print('✓ OK')
"
```

---

## Support Channels

- **Documentation**: See guides in root directory
- **Issues**: Check logs in terminal
- **Models**: See `models/README.md`
- **Deployment**: See `DEPLOYMENT_GUIDE.md`

---

**Keep this reference handy!**

Last Updated: 2026-05-13  
Project Version: 1.0
