# 🚀 Quick Start Guide - DeepGuard Web Application

## Option 1: Using the Batch Script (Easiest)

Simply double-click the `start_webapp.bat` file in Windows Explorer!

This will:
1. Check if the model exists
2. Start the Flask web server
3. Show you the URL to open in your browser

## Option 2: Manual Start

### Step 1: Ensure Model is Trained

Your model is currently training. Once it completes:
- The trained model will be saved to: `checkpoints/best_model.keras`

If you want to train manually or re-train:
```bash
python main.py --epochs 10 --batch-size 32
```

### Step 2: Run the Web Application

Open a terminal in the `c:\Deepfake` directory and run:

```bash
python app.py
```

You should see:
```
==================================================
Deepfake Detection Web Application
==================================================

✓ Model loaded successfully!

Starting web server...
Open your browser and navigate to: http://localhost:5000
==================================================
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

## 🎯 How to Use the Web App

### 1. Upload an Image

**Method A - Drag & Drop:**
- Drag any image file from your computer
- Drop it onto the upload area (the dashed box)

**Method B - Click to Browse:**
- Click the "Choose File" button
- Select an image from your file explorer

### 2. Analyze the Image

- Once uploaded, you'll see a preview of your image
- Click the **"Analyze Image"** button
- A loading animation will appear while the model processes the image

### 3. View Results

The results card will display:
- **Classification Badge**: Shows "Real" (green) or "Fake" (red)
- **Confidence Meter**: Visual bar showing confidence percentage
- **Detailed Information**:
  - Classification (Real/Fake)
  - Confidence Score (0-100%)
  - Raw Prediction Value (0-1)

### 4. Analyze Another Image

Click "Analyze Another Image" to start over!

## ✨ Features to Try

### Keyboard Shortcuts
- **Enter**: Analyze the uploaded image
- **Escape**: Close results panel

### Drag and Drop
- Drag images directly from your file explorer or desktop
- The upload area will highlight when you drag over it

### Mobile Responsive
- Open the site on your phone or tablet
- The design automatically adapts to smaller screens

## 🎨 What Makes This App Special

1. **Beautiful Design**
   - Dark theme that's easy on the eyes
   - Smooth animations and transitions
   - Glassmorphism effects (semi-transparent cards)
   - Gradient accents in indigo and purple

2. **Fast & Responsive**
   - Results in under 1 second
   - Smooth animations
   - Real-time model status indicator

3. **User Friendly**
   - Clear visual feedback
   - Helpful error messages
   - Intuitive interface

## 🔧 Troubleshooting

### "Model Not Loaded" Warning

If you see this in the top-right corner:
1. Wait for your current training to complete
2. Or run: `python main.py --epochs 10 --batch-size 32`
3. Restart the web app

### Cannot Connect to Server

Make sure:
- The Flask app is running (you should see console output)
- You're navigating to `http://localhost:5000`
- No other application is using port 5000

### Upload Not Working

Ensure:
- Your file is an image (JPG, PNG, or WEBP)
- The file size is reasonable (< 10MB recommended)
- Your browser has JavaScript enabled

## 📱 Browser Compatibility

Works best on modern browsers:
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

## 🎊 Enjoy!

You now have a fully functional, beautiful deepfake detection web application!

Try uploading different images and see how the model performs. The interface provides detailed feedback on each prediction.

---

**Need help?** Check the full `WEB_APP_README.md` for detailed documentation.
