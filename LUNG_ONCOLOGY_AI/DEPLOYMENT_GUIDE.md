# 🚀 DEPLOYMENT GUIDE

## Local Development

### Prerequisites
- Python 3.10+
- pip or conda
- Git

### Setup

1. **Clone and navigate to project**
```bash
cd LUNG_ONCOLOGY_AI
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Prepare models**
   - Place all `.pkl` and `.h5` files in `models/` directory
   - Required files:
     - `final_ensemble_model.pkl`
     - `cnn_embedding_model.h5`
     - `radiomics_scaler.pkl`
     - `label_encoder.pkl`
     - `fused_feature_selector.pkl`
     - `cnn_feature_selector.pkl`

5. **Run application**
```bash
cd app
streamlit run streamlit_app.py
```

Application opens at `http://localhost:8501`

---

## Docker Deployment

### Build Docker Image

```bash
docker build -t lung-ai:latest .
```

### Run Docker Container

```bash
docker run -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/uploads:/app/uploads \
  lung-ai:latest
```

Access at `http://localhost:8501`

### Run with Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  lung-ai:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./models:/app/models
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## Streamlit Cloud Deployment

### Step 1: Prepare GitHub Repository

Structure your repo:
```
my-lung-ai-repo/
├── LUNG_ONCOLOGY_AI/
│   ├── app/
│   ├── models/
│   ├── requirements.txt
│   ├── runtime.txt
│   └── Dockerfile
```

### Step 2: Upload Models to GitHub LFS

**Install Git LFS:**
```bash
git lfs install
```

**Track model files:**
```bash
git lfs track "*.h5"
git lfs track "*.pkl"
```

### Step 3: Push to GitHub

```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

### Step 4: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your GitHub repo
4. Enter these settings:
   - **Repository**: `username/repo`
   - **Branch**: `main`
   - **Main file path**: `LUNG_ONCOLOGY_AI/app/streamlit_app.py`

5. Click "Deploy"

**Note**: Streamlit Cloud has 1GB memory limit. Optimize models if needed.

---

## AWS Deployment

### Using EC2

1. **Launch EC2 instance** (Ubuntu 20.04+, t3.medium+)

2. **SSH into instance**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

3. **Install dependencies**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10 python3-pip git -y
```

4. **Clone and setup**
```bash
git clone https://github.com/yourusername/lung-ai.git
cd lung-ai/LUNG_ONCOLOGY_AI
pip install -r requirements.txt
```

5. **Run with systemd**

Create `/etc/systemd/system/lung-ai.service`:

```ini
[Unit]
Description=Lung Oncology AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/lung-ai/LUNG_ONCOLOGY_AI
ExecStart=/usr/bin/python3 -m streamlit run app/streamlit_app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable lung-ai
sudo systemctl start lung-ai
```

### Using AWS AppRunner (Easier)

1. Create Docker image and push to ECR
2. In AppRunner: New service → ECR image → Configure
3. Port: 8501
4. Deploy

---

## Google Cloud Run Deployment

1. **Build image**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/lung-ai
```

2. **Deploy**
```bash
gcloud run deploy lung-ai \
  --image gcr.io/PROJECT-ID/lung-ai \
  --platform managed \
  --Memory 2Gi \
  --port 8501
```

---

## Heroku Deployment

1. **Create Heroku app**
```bash
heroku login
heroku create your-app-name
```

2. **Create Procfile**
```
web: cd LUNG_ONCOLOGY_AI && streamlit run app/streamlit_app.py --server.port=$PORT
```

3. **Push to Heroku**
```bash
git push heroku main
```

**Note**: Heroku free tier may be insufficient for this app's size.

---

## Azure Container Instances

1. **Build and push image**
```bash
az acr build --registry myregistry --image lung-ai:latest .
```

2. **Deploy container**
```bash
az container create \
  --resource-group mygroup \
  --name lung-ai \
  --image myregistry.azurecr.io/lung-ai:latest \
  --ports 8501 \
  --memory 2 \
  --cpu 1
```

---

## Performance Optimization

### Model Optimization
```python
# Use TensorFlow Lite for faster inference
import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_saved_model("model_directory")
tflite_model = converter.convert()
```

### Caching with Streamlit
```python
@st.cache_resource
def load_models():
    # Models loaded once per session
    return models
```

### Environment Variables
Create `.env`:
```
MODEL_PATH=/app/models
UPLOAD_PATH=/app/uploads
MAX_UPLOAD_SIZE=100MB
```

---

## Monitoring & Logging

### Docker Logs
```bash
docker logs -f lung-ai
```

### Streamlit Logging
Logs appear in terminal where Streamlit runs.

### Production Logging (with Sentry)
```python
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

---

## Security Considerations

1. **Disable Streamlit UI**
```python
# In config
client.showErrorDetails = false
logger.level = "warning"
```

2. **Use HTTPS** (behind nginx/proxy)

3. **Restrict file uploads**
```python
if file_uploader.size > MAX_SIZE:
    st.error("File too large")
```

4. **Validate inputs** before model prediction

5. **Use environment variables** for sensitive data

---

## Troubleshooting

### Models not loading
```bash
ls -la models/  # Check if files exist
file models/*.pkl  # Verify file types
```

### Out of memory
- Reduce image size in config.json
- Use smaller batch sizes
- Upgrade server resources

### Slow predictions
- Pre-warm models
- Use GPU if available
- Optimize model size

### Connection timeout
- Check firewall rules
- Verify port 8501 is open
- Check proxy/load balancer config

---

## Health Check

Test deployment:
```bash
curl http://localhost:8501
```

Should return HTML (Streamlit page)

---

**Last Updated**: 2026-05-13
