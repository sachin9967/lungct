# 🫁 Lung Oncology AI

**Hybrid CNN + Radiomics Lung Cancer Risk Prediction System**

A machine learning application that combines deep learning (CNN) and radiomics analysis for accurate lung cancer risk classification.

## 📋 Features

- **Radiomics Analysis**: Quantitative feature extraction from medical images
- **CNN Embeddings**: Deep learning-based image feature extraction
- **Ensemble Learning**: Hybrid prediction combining multiple models
- **Risk Classification**: High/Medium/Low risk assessment
- **Streamlit UI**: Interactive web-based interface
- **Docker Support**: Easy containerization and deployment

## 🎯 Risk Classes

- 🔴 **High Risk**: Elevated cancer risk
- 🟡 **Medium Risk**: Moderate cancer risk
- 🟢 **Low Risk**: Lower cancer risk

## 📁 Project Structure

```
LUNG_ONCOLOGY_AI/
├── app/
│   ├── streamlit_app.py       # Main Streamlit application
│   ├── predict.py              # Prediction pipeline
│   ├── preprocessing.py         # Image preprocessing
│   ├── utils.py               # Utility functions
│   └── config.json            # Configuration
├── models/
│   ├── final_ensemble_model.pkl
│   ├── hybrid_radiomics_cnn_model.h5
│   ├── cnn_embedding_model.h5
│   ├── radiomics_scaler.pkl
│   ├── label_encoder.pkl
│   ├── fused_feature_selector.pkl
│   └── cnn_feature_selector.pkl
├── uploads/                    # User uploaded files
├── outputs/                    # Generated predictions
├── sample_inputs/              # Example files
├── requirements.txt
├── Dockerfile
├── runtime.txt
└── README.md
```

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
cd app
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t lung-ai .
```

### Run Container

```bash
docker run -p 8501:8501 lung-ai
```

Access at `http://localhost:8501`

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Click "New app"
4. Connect your GitHub repo
5. Set main file path to `app/streamlit_app.py`
6. Deploy

## 📊 How to Use

1. **Upload Tumor Image**: PNG or JPG of CT scan
2. **Upload Radiomics CSV**: CSV file with radiomics features
3. **Click "Make Prediction"**: System processes both inputs
4. **Get Results**: 
   - Risk classification
   - Confidence score
   - Class probabilities

## 🔧 Configuration

Edit `app/config.json`:

```json
{
    "image_size": 224,
    "classes": ["High Risk", "Low Risk", "Medium Risk"],
    "num_classes": 3
}
```

## 📦 Models

Place trained models in the `models/` directory:

| Model | Purpose |
|-------|---------|
| `final_ensemble_model.pkl` | Final ensemble predictor |
| `cnn_embedding_model.h5` | CNN feature extractor |
| `hybrid_radiomics_cnn_model.h5` | Hybrid architecture (optional) |
| `radiomics_scaler.pkl` | Radiomics feature scaler |
| `label_encoder.pkl` | Class label encoder |
| `fused_feature_selector.pkl` | Fused feature selector |
| `cnn_feature_selector.pkl` | CNN feature selector |

## 🔗 API Integration

For custom integration, use the `predict.py` module:

```python
from app.predict import predict_lung_cancer

result = predict_lung_cancer(
    image_path="path/to/image.png",
    radiomics_csv_path="path/to/radiomics.csv"
)

print(result)
# {
#     "prediction": "High Risk",
#     "confidence": 0.9234,
#     "probabilities": {
#         "High Risk": 0.9234,
#         "Medium Risk": 0.0512,
#         "Low Risk": 0.0254
#     }
# }
```

## ⚠️ Important Notes

- This system is for research/clinical support only
- Always consult healthcare professionals for medical decisions
- Ensure radiomics CSV has all required features
- Image size should be 224x224 pixels (auto-resized)
- Models must be placed in `models/` directory before running

## 📋 Requirements

- Python 3.10+
- TensorFlow 2.19.0
- scikit-learn
- OpenCV
- pandas
- numpy

See `requirements.txt` for full list.

## 🐛 Troubleshooting

**Model not found**: Ensure all `.pkl` and `.h5` files are in `models/` directory

**Image error**: Verify image is PNG/JPG and readable by OpenCV

**CSV error**: Check radiomics CSV format matches training data

**Memory issues**: Reduce batch size or use smaller images

## 📞 Support

For issues or questions, please refer to the project documentation.

## 📄 License

This project is for educational and research purposes.

---

**Last Updated**: 2026-05-13
**Version**: 1.0
