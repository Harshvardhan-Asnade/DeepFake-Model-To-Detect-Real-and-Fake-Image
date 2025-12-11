---
title: Deepfake Detection System
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# 🔍 Deepfake Detection System

> **A high-performance deep learning system to detect deepfake images with 91.6% accuracy**

![Deepfake Detection](https://img.shields.io/badge/Accuracy-91.6%25-success)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Python](https://img.shields.io/badge/Python-3.9-blue)

---

## 🚀 Try It Out!

Upload an image to check if it's **Real** or **Fake**! The AI model analyzes the image and provides a confidence score.

---

## ✨ Features

- 🎯 **91.6% Accuracy** - Fine-tuned EfficientNetB0 model
- ⚡ **Real-time Detection** - Instant results with confidence scores
- 🎨 **Modern UI** - Beautiful dark mode interface
- 📊 **Detailed Analysis** - View prediction confidence and raw scores
- 🔒 **Privacy First** - All processing happens on the server, no data stored

---

## 🧠 How It Works

1. **Upload Image**: Drag and drop or click to upload an image
2. **AI Analysis**: EfficientNetB0 model processes the image
3. **Get Results**: Receive prediction (Real/Fake) with confidence score

### Model Architecture

- **Base**: EfficientNetB0 (Transfer Learning)
- **Custom Head**: Dense layers with Dropout for robustness
- **Training Data**: Deepfake and Real Images dataset
- **Preprocessing**: EfficientNet-specific normalization

---

## 🎯 Model Performance

| Metric | Value |
|--------|-------|
| **Validation Accuracy** | 91.56% |
| **Architecture** | EfficientNetB0 (Fine-Tuned) |
| **Input Size** | 150x150 pixels |
| **Framework** | TensorFlow/Keras |

---

## 🔬 Technical Details

### Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deep Learning**: TensorFlow 2.x
- **Model**: EfficientNetB0 with custom classification head
- **Deployment**: Docker on Hugging Face Spaces

### Training Process

The model was trained in two phases:
1. **Base Training**: EfficientNetB0 with frozen base (10 epochs)
2. **Fine-Tuning**: Unfrozen layers for deeper learning (10 epochs)

**Final Results**: 91.56% validation accuracy

---

## 📚 Documentation

For complete documentation, code, and training details, visit:

🔗 **[GitHub Repository](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image)**

### Available Guides

- [Quick Start Guide](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image/blob/main/QUICK_START.md)
- [Model Training Guide](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image/blob/main/model_training_guide.md)
- [Project Structure](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image/blob/main/STRUCTURE.md)
- [Technologies Explained](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image/blob/main/TECHNOLOGIES.md)

---

## 🛠️ Running Locally

Want to run this on your own machine? Check out the [Deployment Guide](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image/blob/main/DUAL_DEPLOYMENT_GUIDE.md).

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image.git

# Install dependencies
pip install -r requirements.txt

# Run the app
cd backend
python app.py
```

---

## ⚠️ Disclaimer

This tool is designed for **educational and research purposes**. While the model achieves high accuracy, it should not be the sole method for determining image authenticity in critical applications.

---

## 📜 License

This project is open-source under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Visit the [GitHub repository](https://github.com/Harshvardhan-Asnade/Deepfake-Model-To-Detect-Real-and-Fake-Image) to contribute.

---

## 📬 Contact

- **GitHub**: [@Harshvardhan-Asnade](https://github.com/Harshvardhan-Asnade)
- **Hugging Face**: [@YOUR_HF_USERNAME](https://huggingface.co/YOUR_HF_USERNAME)

---

<div align="center">
  
**Made with ❤️ for detecting deepfakes**

*Powered by TensorFlow, Flask, and Hugging Face Spaces*

</div>
