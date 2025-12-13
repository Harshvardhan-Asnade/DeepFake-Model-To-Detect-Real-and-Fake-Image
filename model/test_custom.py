
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

def predict_image(model, img_path, img_width=380, img_height=380):
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
        
        # In generator: Fake=0, Real=1
        # Model output is probability of Class 1 (Real)
        # So "Real Probability" = score
        # "Fake Probability" = 1 - score
        
        return score, None
    except Exception as e:
        return None, str(e)

import random

def main():
    # Config
    model_path = 'model/checkpoints/final_model_pro.keras'
    # Use the large dataset we were training on
    dataset_path = '/Users/harshvardhan/Developer/deepfake/Dataset/Image Dataset' 
    if not os.path.exists(dataset_path):
        # Fallback to the one in the parent if subfolder doesn't exist
        dataset_path = '/Users/harshvardhan/Developer/deepfake/Dataset'
        
    # Check if "Test" folder exists inside
    if os.path.exists(os.path.join(dataset_path, "Test")):
        dataset_path = os.path.join(dataset_path, "Test")
        print(f"Using Test split at: {dataset_path}")
    elif os.path.exists(os.path.join(dataset_path, "Validation")):
        dataset_path = os.path.join(dataset_path, "Validation")
        print(f"Using Validation split at: {dataset_path}")
    
    samples_per_class = 5  # Number of images to test per class
    
    print(f"Loading model: {model_path}")
    if not os.path.exists(model_path):
        print("Model file not found!")
        return

    try:
        model = load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Get input shape from model if possible
    try:
        input_shape = model.input_shape
        img_height = input_shape[1]
        img_width = input_shape[2]
        print(f"Model input shape: {img_width}x{img_height}")
    except:
        img_width = 150
        img_height = 150
        print(f"Using default shape: {img_width}x{img_height}")

    print("\n" + "="*80)
    print(f"{'FILENAME':<30} | {'TRUE':<6} | {'PRED':<6} | {'CONF':<8} | {'STATUS'}")
    print("="*80)
    
    correct_count = 0
    total_count = 0
    
    # Iterate through folders
    for label in ['Fake', 'Real']:
        folder_path = os.path.join(dataset_path, label)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue
            
        all_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        # Randomly sample
        if len(all_files) > samples_per_class:
            selected_files = random.sample(all_files, samples_per_class)
        else:
            selected_files = all_files
            
        for filename in selected_files:
            file_path = os.path.join(folder_path, filename)
            
            score, error = predict_image(model, file_path, img_width, img_height)
            
            if error:
                print(f"{filename[:30]:<30} | {label:<6} | ERROR  | -        | {error}")
                continue
            
            # Logic: Score > 0.5 is Real, < 0.5 is Fake
            is_real = score > 0.5
            predicted_label = "Real" if is_real else "Fake"
            
            confidence = score if is_real else (1 - score)
            
            total_count += 1
            if predicted_label == label:
                correct_count += 1
                status = "✅"
            else:
                status = "❌"
                
            print(f"{filename[:30]:<30} | {label:<6} | {predicted_label:<6} | {confidence:.2%} | {status}")
                
    print("="*80)
    if total_count > 0:
        print(f"Accuracy: {correct_count}/{total_count} ({correct_count/total_count:.2%})")
        print(f"Tested on {total_count} random images from {dataset_path}")
    else:
        print("No images found.")

if __name__ == "__main__":
    main()
