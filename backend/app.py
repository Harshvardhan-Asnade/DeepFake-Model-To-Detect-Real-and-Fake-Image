"""
Flask Web Application for Deepfake Detection
Provides a web interface to upload images and get predictions
"""

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image
import io
import base64

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configuration
# Uploads handled in frontend static
UPLOAD_FOLDER = '../frontend/static/uploads' 
MODEL_PATH = '../model/checkpoints/final_model_pro.keras'
IMG_WIDTH = 150
IMG_HEIGHT = 150

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store the model
model = None

def load_trained_model():
    """Load the trained model"""
    global model
    try:
        if os.path.exists(MODEL_PATH):
            print(f"Loading model from {MODEL_PATH}...")
            model = load_model(MODEL_PATH)
            print("Model loaded successfully!")
            return True
        else:
            print(f"Model not found at {MODEL_PATH}")
            return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def preprocess_image(img):
    """Preprocess image for prediction"""
    # Resize image
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    
    # Convert to array
    img_array = image.img_to_array(img)
    
    # Expand dimensions to match batch size
    img_array = np.expand_dims(img_array, axis=0)
    
    # Use EfficientNet preprocessing (expects 0-255 inputs)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    
    return img_array

def predict_image(img):
    """Make prediction on image"""
    if model is None:
        return None, "Model not loaded"
    
    try:
        # Preprocess the image
        processed_img = preprocess_image(img)
        
        # Make prediction
        prediction = model.predict(processed_img, verbose=0)
        confidence = float(prediction[0][0])
        
        # Determine class (0 = Fake, 1 = Real)
        if confidence > 0.5:
            result = "Real"
            confidence_percent = confidence * 100
        else:
            result = "Fake"
            confidence_percent = (1 - confidence) * 100
        
        return {
            'class': result,
            'confidence': round(confidence_percent, 2),
            'raw_score': round(confidence, 4)
        }, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    """Render main page (Analysis)"""
    model_status = "loaded" if model is not None else "not_loaded"
    return render_template('index.html', model_status=model_status)

@app.route('/dashboard')
def dashboard():
    """Render dashboard page"""
    return render_template('dashboard.html')

@app.route('/history')
def history():
    """Render history page"""
    return render_template('history.html')

@app.route('/results')
def results():
    """Render results page"""
    return render_template('results.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    if model is None:
        return jsonify({
            'success': False,
            'error': 'Model not loaded. Please train the model first.'
        }), 503
    
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No image file provided'
        }), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    try:
        # Save file (optional but good for results page)
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read for prediction
        img = Image.open(filepath)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Make prediction
        result, error = predict_image(img)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 500
            
        # Add filename to result
        result['filename'] = filename
        result['image_url'] = f'/static/uploads/{filename}' # Assuming uploads is mapped or we map it
        
        # We need to make sure 'uploads' is served. 
        # By default Flask static folder is 'static'. 
        # If UPLOAD_FOLDER is 'uploads' (root), we need to move it to 'static/uploads' or add route.
        # Let's verify UPLOAD_FOLDER definition.
        
        return jsonify({
            'success': True,
            'prediction': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }), 500

@app.route('/api/model-status')
def model_status():
    """Get model status"""
    return jsonify({
        'loaded': model is not None,
        'model_path': MODEL_PATH,
        'exists': os.path.exists(MODEL_PATH)
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Deepfake Detection Web Application")
    print("="*50)
    
# Load the model directly when app starts (for production/Vercel)
if load_trained_model():
    print("✓ Model loaded successfully!")
else:
    print("⚠ Warning: Model not loaded. Please train the model first.")
    print(f"Expected model path: {MODEL_PATH}")

if __name__ == '__main__':
    # Get port from environment variable (for Hugging Face) or use 5001 for local
    port = int(os.environ.get('PORT', 5001))
    
    print("\n" + "="*50)
    print("Deepfake Detection Web Application")
    print("="*50)
    
    print(f"\nStarting web server on port {port}...")
    print(f"Open your browser and navigate to: http://localhost:{port}")
    print("="*50 + "\n")
    
    # Use debug=False for production (Hugging Face)
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
