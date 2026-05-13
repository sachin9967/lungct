#!/bin/bash

# Lung Oncology AI - Setup Script
# This script sets up the deployment environment

echo "🫁 Lung Oncology AI - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check models directory
echo "✓ Verifying models directory..."
if [ ! -d "models" ]; then
    mkdir -p models
    echo "  Created models/ directory"
fi

# Check uploads directory
if [ ! -d "uploads" ]; then
    mkdir -p uploads
    echo "  Created uploads/ directory"
fi

# Check outputs directory
if [ ! -d "outputs" ]; then
    mkdir -p outputs
    echo "  Created outputs/ directory"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add model files to models/ directory:"
echo "   - final_ensemble_model.pkl"
echo "   - cnn_embedding_model.h5"
echo "   - radiomics_scaler.pkl"
echo "   - label_encoder.pkl"
echo "   - fused_feature_selector.pkl"
echo "   - cnn_feature_selector.pkl"
echo ""
echo "2. Run the application:"
echo "   cd app"
echo "   streamlit run streamlit_app.py"
echo ""
