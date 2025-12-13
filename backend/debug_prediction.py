
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import sys

# Constants matching app.py
# Use absolute path to avoid CWD confusion
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'checkpoints', 'final_model.keras')

IMG_WIDTH = 380
IMG_HEIGHT = 380

def test_images():
    print(f"Loading model from {MODEL_PATH}...")
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Check model input shape
    input_shape = model.input_shape
    print(f"Model expects input shape: {input_shape}")
    
    # Images to test
    image_paths = [
        "/Users/harshvardhan/.gemini/antigravity/brain/298299fc-f211-4894-b52c-0ab9108fe9d3/uploaded_image_0_1765594599369.png",
        "/Users/harshvardhan/.gemini/antigravity/brain/298299fc-f211-4894-b52c-0ab9108fe9d3/uploaded_image_1_1765594599369.jpg"
    ]

    print("\nStarting Predictions...\n")
    print(f"{'Image':<60} | {'Raw Score':<10} | {'Prediction':<10} | {'Confidence':<10}")
    print("-" * 100)

    for img_path in image_paths:
        try:
            # Load and resize
            img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            
            # Preprocess
            img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
            
            # Predict
            prediction = model.predict(img_array, verbose=0)
            confidence = float(prediction[0][0])
            
            if confidence > 0.5:
                result = "Real"
                conf_val = confidence * 100
            else:
                result = "Fake"
                conf_val = (1 - confidence) * 100
            
            filename = os.path.basename(img_path)
            print(f"{filename:<60} | {confidence:.4f}     | {result:<10} | {conf_val:.2f}%")

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    test_images()
