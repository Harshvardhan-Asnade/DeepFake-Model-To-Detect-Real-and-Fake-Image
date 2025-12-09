# Project Structure

This document outlines the file organization of the Deepfake Detection System.

```
Deepfake-System/
├── README.md                   # Main project documentation
├── QUICK_START.md              # Quick start guide
├── STRUCTURE.md                # This file
├── requirements.txt            # Project dependencies
│
├── frontend/                   # Web Interface
│   ├── static/
│   │   ├── style.css           # Styling for the web app
│   │   ├── script.js           # Frontend logic and API handling
│   │   └── uploads/            # Temporary storage for uploaded images
│   ├── templates/
│   │   ├── index.html          # Main analysis page
│   │   ├── dashboard.html      # Dashboard view
│   │   ├── history.html        # Analysis history
│   │   └── results.html        # Results display page
│   └── WEB_APP_README.md       # Frontend specific documentation
│
├── backend/                    # Flask Server
│   ├── app.py                  # Main application server (Port 5001)
│   └── start_webapp.bat        # Windows startup script
│
├── model/                      # Deep Learning Model
│   ├── main.py                 # Main training pipeline
│   ├── model.py                # EfficientNetB0 architecture definition
│   ├── data_preparation.py     # Data loading and preprocessing (EfficientNet standards)
│   ├── train.py                # Training loops and callbacks
│   ├── evaluate.py             # Evaluation metrics
│   ├── resume_finetune.py      # Script for fine-tuning resumption
│   ├── model_training_guide.md # Guide for training strategies
│   ├── logs/                   # Training logs
│   └── checkpoints/            # Saved model weights
│       ├── final_model.keras       # Baseline Model (MobileNetV2)
│       ├── final_model_pro.keras   # High-Accuracy Model (EfficientNetB0, ~91.6%)
│       └── final_model_m4.keras    # M4 Optimized Model
│
└── venv/                       # Python Virtual Environment
```

## Key Components

### 1. Model Core (`model/`)
- **Architecture**: EfficientNetB0 (Pre-trained on ImageNet)
- **Top Layer**: Custom Dense Head (512 units -> Dropout -> Sigmoid)
- **Performance**: ~91.6% Accuracy
- **Training Strategy**: 
  - Phase 1: Train Head (frozen base)
  - Phase 2: Fine-tune deep layers (unfrozen last 30 layers)

### 2. Backend API (`backend/`)
- **Framework**: Flask
- **Port**: 5001
- **Endpoints**:
  - `/api/predict`: Handles image uploads and inference
  - `/api/model-status`: Checks model loading status

### 3. Frontend UI (`frontend/`)
- **Tech**: HTML5, CSS3, Vanilla JS
- **Features**: Drag & Drop, Real-time Analysis, Responsive Design
