#!/usr/bin/env python3
"""
Compare predictions from two different model checkpoints
"""

import os
import sys
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

def predict_image(model, img_path, img_width=380, img_height=380):
    """
    Make a prediction on a single image
    
    Args:
        model: Loaded Keras model
        img_path: Path to the image
        img_width: Target width
        img_height: Target height
        
    Returns:
        tuple: (confidence_score, error_message)
    """
    try:
        img = cv2.imread(img_path)
        if img is None:
            return None, "Error reading image"
            
        img = cv2.resize(img, (img_width, img_height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_array = np.expand_dims(img, axis=0)
        img_array = preprocess_input(img_array)
        
        prediction = model.predict(img_array, verbose=0)
        score = prediction[0][0]
        
        # Model output is probability of Class 1 (Real)
        # Fake=0, Real=1
        return score, None
    except Exception as e:
        return None, str(e)

def load_and_test_models(image_path, model1_path, model2_path):
    """
    Load both models and test them on the same image
    
    Args:
        image_path: Path to the test image
        model1_path: Path to first model
        model2_path: Path to second model
    """
    print("\n" + "="*80)
    print(" "*25 + "MODEL COMPARISON TEST")
    print("="*80)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"\n📸 Test Image: {os.path.basename(image_path)}")
    print(f"   Full Path: {image_path}")
    
    # Load Model 1
    print(f"\n🔄 Loading Model 1: {os.path.basename(model1_path)}")
    try:
        model1 = load_model(model1_path)
        img_width1 = model1.input_shape[2]
        img_height1 = model1.input_shape[1]
        print(f"   ✅ Model loaded successfully (Input: {img_width1}x{img_height1})")
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        return
    
    # Load Model 2
    print(f"\n🔄 Loading Model 2: {os.path.basename(model2_path)}")
    try:
        model2 = load_model(model2_path)
        img_width2 = model2.input_shape[2]
        img_height2 = model2.input_shape[1]
        print(f"   ✅ Model loaded successfully (Input: {img_width2}x{img_height2})")
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        return
    
    # Test with Model 1
    print(f"\n🧪 Testing with Model 1...")
    score1, error1 = predict_image(model1, image_path, img_width1, img_height1)
    
    # Test with Model 2
    print(f"🧪 Testing with Model 2...")
    score2, error2 = predict_image(model2, image_path, img_width2, img_height2)
    
    # Display Results
    print("\n" + "="*80)
    print(" "*30 + "RESULTS")
    print("="*80)
    
    def format_result(model_name, score, error):
        """Format prediction result"""
        if error:
            print(f"\n{model_name}:")
            print(f"  ❌ Error: {error}")
            return
        
        # Determine prediction
        is_real = score > 0.5
        predicted_label = "REAL" if is_real else "FAKE"
        confidence = score if is_real else (1 - score)
        
        # Visual indicator
        emoji = "✅" if is_real else "⚠️"
        
        print(f"\n{model_name}:")
        print(f"  Prediction: {emoji} {predicted_label}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Raw Score:")
        print(f"    - Real Probability: {score:.4f}")
        print(f"    - Fake Probability: {1-score:.4f}")
    
    format_result("📊 Model 1 (final_model_pro.keras)", score1, error1)
    format_result("📊 Model 2 (final_model.keras)", score2, error2)
    
    # Comparison
    if score1 is not None and score2 is not None:
        print("\n" + "-"*80)
        print(" "*30 + "COMPARISON")
        print("-"*80)
        
        pred1 = "Real" if score1 > 0.5 else "Fake"
        pred2 = "Real" if score2 > 0.5 else "Fake"
        
        if pred1 == pred2:
            print(f"\n✅ Both models AGREE: Image is {pred1}")
        else:
            print(f"\n⚠️  Models DISAGREE:")
            print(f"   Model 1: {pred1}")
            print(f"   Model 2: {pred2}")
        
        diff = abs(score1 - score2)
        print(f"\n📏 Score Difference: {diff:.4f} ({diff*100:.2f}%)")
        
        if score1 > score2:
            print(f"   Model 1 is MORE confident the image is Real")
        elif score2 > score1:
            print(f"   Model 2 is MORE confident the image is Real")
        else:
            print(f"   Models have IDENTICAL confidence")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    # Default paths
    if len(sys.argv) >= 2:
        image_path = sys.argv[1]
    else:
        image_path = "/Users/harshvardhan/.gemini/antigravity/brain/da5fec4e-15a2-400e-be08-9a98540900f1/uploaded_image_1765605122584.jpg"
    
    if len(sys.argv) >= 3:
        model1_path = sys.argv[2]
    else:
        model1_path = "/Users/harshvardhan/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image/model/checkpoints/final_model_pro.keras"
    
    if len(sys.argv) >= 4:
        model2_path = sys.argv[3]
    else:
        model2_path = "/Users/harshvardhan/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image/model/checkpoints/final_model.keras"
    
    load_and_test_models(image_path, model1_path, model2_path)
