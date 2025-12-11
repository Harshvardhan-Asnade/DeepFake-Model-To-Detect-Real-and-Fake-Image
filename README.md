# Deepfake Detection System (Pro)

A high-performance deep learning system to detect deepfake images, featuring a **91.6% accuracy** EfficientNetB0 model and a modern web interface.

## 🚀 Features

- **Pro-Grade Accuracy**: ~91.6% validation accuracy using Fine-Tuned EfficientNetB0.
- **Modern Web Interface**:
  - Drag & Drop file uploads.
  - Real-time analysis with confidence scores.
  - Modern, responsive Dark Mode design.
- **Advanced Architecture**:
  - **Base**: EfficientNetB0 (Transfer Learning).
  - **Head**: Custom Dense Layers with Dropout for robustness.
  - **Preprocessing**: EfficientNet-specific standard.
- **Dual Infrastructure**:
  - **Training Pipeline**: Comprehensive scripts for Data Prep, Training, and Evaluation.
  - **Inference Engine**: Fast Flask-based API running on Port 5001.

## � Documentation

- [**Structure**](STRUCTURE.md): Detailed breakdown of files and folders.
- [**Technologies**](TECHNOLOGIES.md): Explanation of the tech stack and AI terms used.

## �📂 Project Structure

See [STRUCTURE.md](STRUCTURE.md) for a detailed breakdown.

```
Deepfake-System/
├── frontend/           # Web Interface (HTML/CSS/JS)
├── backend/            # Flask Server (app.py)
├── model/              # Training Pipeline & Checkpoints
└── README.md           # This file
```

## 🛠️ Installation

1. **Clone & Setup Environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Dataset Setup**:
   Ensure you have the "Deepfake and Real Images" dataset in `Dataset/` or the default cache location.

## 🚦 Usage

### 1. Launch the Web App (Recommended)
This starts the backend server and serves the frontend.

```bash
cd backend
python app.py
```
> Open your browser at **[http://localhost:5001](http://localhost:5001)**

### 2. Train the Model
To re-train or fine-tune the model yourself:

```bash
cd model
# Standard Training (Phase 1)
python main.py --epochs 10 --batch-size 32

# Pro Training (Phase 1 + Fine-Tuning)
python main.py --epochs 10 --fine-tune --fine-tune-epochs 10
```

## 🧠 Model Performance

| Model Version | Architecture | Accuracy | Status |
| :--- | :--- | :--- | :--- |
| **Final Pro** | **EfficientNetB0 (Fine-Tuned)** | **91.56%** | ✅ **Active** |
| Baseline | EfficientNetB0 (Frozen) | ~78.0% | ⚠️ Deprecated |
| Legacy | MobileNetV2 | ~75.9% | ⚠️ Legacy |

## 📜 License

Created for educational and research purposes.