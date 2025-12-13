
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryFocalCrossentropy
import shutil

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
CHECKPOINT_DIR = os.path.join(BASE_DIR, 'checkpoints')
MODEL_PATH = os.path.join(CHECKPOINT_DIR, 'final_model_pro.keras')
FINETUNE_DIR = os.path.join(PROJECT_ROOT, 'FineTuneData')
IMG_WIDTH = 150
IMG_HEIGHT = 150
BATCH_SIZE = 4  # Small batch size for small datasets
EPOCHS = 10
LR = 1e-5 # Very slow learning rate to prevent "forgetting"

def setup_directories():
    """Create the folder structure for the user to drop images into"""
    print(f"\n[1] Setting up Fine-Tuning Environment...")
    
    real_dir = os.path.join(FINETUNE_DIR, 'Real')
    fake_dir = os.path.join(FINETUNE_DIR, 'Fake')
    
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(fake_dir, exist_ok=True)
    
    print(f"    Created directory: {FINETUNE_DIR}")
    print(f"    ➜ PLEASE PUT REAL IMAGES IN: {real_dir}")
    print(f"    ➜ PLEASE PUT AI/FAKE IMAGES IN: {fake_dir}")
    
    # Check if empty
    real_count = len(os.listdir(real_dir))
    fake_count = len(os.listdir(fake_dir))
    
    if real_count == 0 and fake_count == 0:
        print("\n    ⚠  Wait! The folders are empty.")
        print("    Please copy your difficult images into these folders now.")
        input("    Press Enter once you have added the images...")
        return False
    return True

def run_finetuning():
    """Run the fine-tuning process"""
    print(f"\n[2] Loading Model from {MODEL_PATH}...")
    
    try:
        model = load_model(MODEL_PATH)
        print("    Model loaded.")
    except Exception as e:
        print(f"    Error loading model: {e}")
        return

    # Data Generators
    print("\n[3] Preparing Data Generators...")
    train_datagen = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.efficientnet.preprocess_input,
        rotation_range=20,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    try:
        train_generator = train_datagen.flow_from_directory(
            FINETUNE_DIR,
            target_size=(IMG_WIDTH, IMG_HEIGHT),
            batch_size=BATCH_SIZE,
            class_mode='binary'
        )
    except Exception as e:
        print(f"    Error preparing data: {e}")
        return

    if train_generator.samples == 0:
        print("    ERROR: No images found in FineTuneData folders!")
        return

    # Unfreeze last few layers (optional, but good for adaptation)
    # Since we are just teaching it "new textures", unfreezing the top block is good.
    print("\n[4] Unfreezing top layers for adaptation...")
    for layer in model.layers[-20:]: 
        if not isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = True
            
    # Compile with low LR
    model.compile(
        optimizer=Adam(learning_rate=LR),
        loss=BinaryFocalCrossentropy(gamma=2.0, from_logits=False),
        metrics=['accuracy']
    )
    
    # Train
    print(f"\n[5] Training for {EPOCHS} epochs...")
    model.fit(
        train_generator,
        epochs=EPOCHS,
        verbose=1
    )
    
    # Save
    new_model_name = 'final_model_pro_v2.keras'
    save_path = os.path.join(CHECKPOINT_DIR, new_model_name)
    model.save(save_path)
    
    print("\n" + "="*50)
    print("SUCCESS! Model Fine-Tuned.")
    print(f"Saved to: {save_path}")
    print("="*50)
    print("To use this model, update app.py to point to this new file.")

if __name__ == "__main__":
    if setup_directories():
        run_finetuning()
