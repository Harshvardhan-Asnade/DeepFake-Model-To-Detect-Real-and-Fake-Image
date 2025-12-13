# Quick Start Guide 🚀

Get the Deepfake Detection System up and running in minutes.

## 📋 Prerequisites

- **Python 3.8+** (Required)
- **Git** (Recommended)
- **Mac Users**: Apple Silicon (M1/M2/M3) is supported via Metal.

## ⚡ Setup in 3 Steps

### 1. Setup Environment
First, create a virtual environment to keep your project clean. Choose your OS:

#### 🪟 Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 🍎 macOS / 🐧 Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install all required libraries.

```bash
pip install -r requirements.txt
```

### 3. Run the App
Launch the web interface.

#### 🪟 Windows
```cmd
cd backend
python app.py
```

#### 🍎 macOS / 🐧 Linux
```bash
cd backend
python app.py
```

> **Success!** Open your browser to: **[http://localhost:5001](http://localhost:5001)**

---

## 🛠 Troubleshooting

### "Model not loaded"
If you see this error, you need to train the model first.

```bash
cd model
python main.py --epochs 10
# Restart the backend after this
```

### "Address already in use"
If port 5001 is taken, open `backend/app.py` and change the line `port=5001` to `port=5002`.

### Mac Users: "TensorFlow not found"
If you are on an M-series Mac, ensure you installed metal support:
```bash
pip install tensorflow-metal
```