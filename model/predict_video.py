
import cv2
import numpy as np
import argparse
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

def predict_video(video_path, model_path, frame_interval=5, img_width=150, img_height=150):
    """
    Predict if a video is Real or Fake by analyzing frames.
    
    Args:
        video_path: Path to the input video
        model_path: Path to the trained model (.keras file)
        frame_interval: Analyze every Nth frame to speed up processing
        img_width: Target image width for the model
        img_height: Target image height for the model
        
    Returns:
        dict: containing 'prediction' (Real/Fake), 'confidence', and 'frame_stats'
    """
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
        
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    print(f"Loading model from: {model_path}")
    model = load_model(model_path)
    
    print(f"Processing video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Error opening video file")
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video Stats: {total_frames} frames, {fps:.2f} FPS, {duration:.2f} seconds")
    
    frames_processed = 0
    fake_scores = []
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        
        # Skip frames based on interval
        if frame_count % frame_interval != 0:
            continue
            
        # Preprocess frame
        # Resize to model input size
        try:
            processed_frame = cv2.resize(frame, (img_width, img_height))
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Expand dims to create batch of size 1
            frame_batch = np.expand_dims(processed_frame, axis=0)
            
            # Apply EfficientNet preprocessing
            frame_batch = preprocess_input(frame_batch)
            
            # Predict
            prediction = model.predict(frame_batch, verbose=0)
            score = prediction[0][0] # Probability of being "Real" (1.0) or "Fake" (0.0)
            # Note: The model output interpretation depends on your training labels.
            # Typically: 0 = Fake, 1 = Real (based on alphabetical order of folders usually)
            # But let's verify logic:
            # If using flow_from_directory, classes are alphanumeric sorted.
            # Fake comes before Real. So Fake=0, Real=1.
            # High score (>0.5) -> Real
            # Low score (<0.5) -> Fake
            # We want to track "Fake Probability". So if 0=Fake, then FakeProb = 1 - score.
            
            fake_prob = 1.0 - score
            fake_scores.append(fake_prob)
            
            frames_processed += 1
            if frames_processed % 10 == 0:
                print(f"Processed {frames_processed} frames...", end='\r')
                
        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")
            continue

    cap.release()
    print(f"\nFinished processing {frames_processed} frames.")
    
    if not fake_scores:
        return {"error": "No frames could be processed"}
        
    # Aggregate results
    avg_fake_prob = np.mean(fake_scores)
    max_fake_prob = np.max(fake_scores)
    
    # Decision logic
    # If the average fake probability is high, it's likely fake.
    # Use a threshold.
    threshold = 0.5
    is_fake = avg_fake_prob > threshold
    
    prediction_label = "Fake" if is_fake else "Real"
    confidence = avg_fake_prob if is_fake else (1.0 - avg_fake_prob)
    
    result = {
        "prediction": prediction_label,
        "confidence": float(confidence),
        "avg_fake_prob": float(avg_fake_prob),
        "frames_processed": frames_processed
    }
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deepfake Detection Video Inference')
    parser.add_argument('--video_path', type=str, required=True, help='Path to input video file')
    parser.add_argument('--model_path', type=str, default='model/checkpoints/final_model_pro.keras', help='Path to trained model')
    parser.add_argument('--frame_interval', type=int, default=10, help='Process every Nth frame')
    
    args = parser.parse_args()
    
    try:
        result = predict_video(
            args.video_path, 
            args.model_path, 
            frame_interval=args.frame_interval
        )
        
        print("\n" + "="*50)
        print("VIDEO DETECTION RESULT")
        print("="*50)
        print(f"Prediction: {result['prediction'].upper()}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Average Fake Probability: {result['avg_fake_prob']:.4f}")
        print(f"Frames Analyzed: {result['frames_processed']}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
