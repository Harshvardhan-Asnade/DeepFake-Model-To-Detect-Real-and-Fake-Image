# DeepGuard - Deepfake Detection Web Application

![DeepGuard](https://img.shields.io/badge/AI-Powered-blue) ![Status](https://img.shields.io/badge/Status-Ready-green) ![Flask](https://img.shields.io/badge/Flask-2.0+-red)

A beautiful, modern web application for detecting deepfake images using advanced deep learning technology. Built with Flask backend and a stunning responsive frontend.

## 🌟 Features

- **🎨 Modern UI/UX**: Premium dark theme with gradients, animations, and glassmorphism effects
- **🚀 Fast Detection**: Analyze images in under 1 second
- **📊 Detailed Results**: View confidence scores, classification, and raw predictions
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **🎯 High Accuracy**: ~91.6% accuracy using EfficientNetB0 architecture
- **🔄 Drag & Drop**: Easy image upload with drag-and-drop support

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **TensorFlow**: Deep learning framework
- **EfficientNetB0**: Pre-trained model for transfer learning
- **Pillow**: Image processing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties, gradients, and animations
- **Vanilla JavaScript**: Interactive functionality
- **Inter & JetBrains Mono**: Premium typography from Google Fonts

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Trained model** at `model/checkpoints/final_model_pro.keras`
   - If you haven't trained the model yet, run: `python model/main.py --epochs 10`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model (if not already done)

```bash
cd model
python main.py --epochs 10 --batch-size 32
cd ..
```

This will:
- Load the offline deepfake dataset
- Train the EfficientNetB0-based model
- Save the best model to `model/checkpoints/final_model_pro.keras`

### 3. Run the Web Application

```bash
cd backend
python app.py
```

### 4. Open in Browser

Navigate to: **http://localhost:5001**

## 📖 Usage Guide

### Uploading Images

1. **Drag & Drop**: Simply drag an image file onto the upload area
2. **Click to Browse**: Click the "Choose File" button to select an image
3. **Supported Formats**: JPG, PNG, WEBP

### Analyzing Images

1. Upload your image using one of the methods above
2. Preview the image to ensure it uploaded correctly
3. Click the **"Analyze Image"** button
4. Wait for the analysis to complete (usually < 1 second)
5. View the detailed results

### Understanding Results

- **Classification**: Either "Real" or "Fake"
- **Confidence Score**: Percentage confidence of the prediction (0-100%)
- **Raw Prediction**: The raw model output (0-1 scale)
  - Values > 0.5 indicate "Real"
  - Values < 0.5 indicate "Fake"

## 🎨 Design Highlights

### Visual Features
- **Animated Gradient Background**: Smooth, shifting gradient overlays
- **Glassmorphism Cards**: Semi-transparent cards with backdrop blur
- **Micro-animations**: Hover effects, button ripples, and smooth transitions
- **Color Palette**: Carefully curated indigo/purple gradient theme
- **Dark Mode**: Easy on the eyes with high contrast elements

### User Experience
- **Responsive Layout**: Mobile-first design that scales beautifully
- **Keyboard Shortcuts**: 
  - `Enter`: Analyze image (when loaded)
  - `Escape`: Close results/overlays
- **Loading States**: Visual feedback during analysis
- **Error Handling**: Clear error messages with auto-dismiss

## 📁 Project Structure

```
Deepfake/
├── backend/
│   └── app.py               # Flask application (Port 5001)
├── frontend/
│   ├── templates/
│   │   └── index.html       # Main HTML template
│   └── static/
│       ├── style.css        # Comprehensive styling
│       └── script.js        # Frontend JavaScript
├── model/
│   ├── checkpoints/
│   │   └── final_model_pro.keras # Trained model
│   ├── model.py             # EfficientNetB0 architecture
│   ├── train.py             # Training utilities
│   ├── evaluate.py          # Evaluation functions
│   ├── data_preparation.py  # Dataset handling
│   └── main.py              # Training pipeline
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

## 🔧 Configuration

### Flask Settings (backend/app.py)

```python
MODEL_PATH = '../model/checkpoints/final_model_pro.keras'  # Path to trained model
IMG_WIDTH = 150                                            # Input image width
IMG_HEIGHT = 150                                           # Input image height
```

### Server Settings

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

- **debug=True**: Enable debug mode (disable in production)
- **host='0.0.0.0'**: Listen on all network interfaces
- **port=5001**: Server port

## 🧪 API Endpoints

### GET /
- **Description**: Render main application page
- **Returns**: HTML page

### POST /api/predict
- **Description**: Analyze uploaded image
- **Input**: Form data with 'image' file
- **Returns**: JSON response with prediction results

```json
{
  "success": true,
  "prediction": {
    "class": "Real",
    "confidence": 97.23,
    "raw_score": 0.9723
  }
}
```

### GET /api/model-status
- **Description**: Check if model is loaded
- **Returns**: Model status information

```json
{
  "loaded": true,
  "model_path": "../model/checkpoints/final_model_pro.keras",
  "exists": true
}
```

## 🐛 Troubleshooting

### Model Not Found Error

**Problem**: "Model not loaded. Please train the model first."

**Solution**: 
```bash
cd model
python main.py --epochs 10 --batch-size 32
```

### Port Already in Use

**Problem**: Port 5001 is already occupied

**Solution**: Change the port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5002)
```

### Image Upload Fails

**Problem**: Image doesn't upload or preview

**Solution**: 
- Check file format (must be JPG, PNG, or WEBP)
- Ensure file size is reasonable (< 10MB recommended)
- Check browser console for JavaScript errors

### Model Loading Slow

**Problem**: Takes long time to load model

**Solution**: This is normal on first load. The model is ~10-20MB and needs to be loaded into memory.

## 🎯 Performance Optimization

### For Production

1. **Disable Debug Mode**:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5001)
   ```

2. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   cd backend
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

## 📊 Model Information

- **Architecture**: EfficientNetB0 (Transfer Learning)
- **Input Size**: 150x150x3 RGB images
- **Accuracy**: ~91.6% (Pro Version)
- **Inference Time**: < 1 second per image

## 🔒 Security Considerations

- File upload validation (image types only)
- Maximum file size limits recommended
- No persistent storage of uploaded images
- CORS configuration needed for cross-origin requests

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Support

For questions or issues, please open an issue on the repository.

---

Built with ❤️ using TensorFlow, Flask, and modern web technologies.
