
"""
Training Module for Deepfake Detection Model
Handles model training, callbacks, and checkpointing
"""

import os
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping, TensorBoard
from datetime import datetime
import matplotlib.pyplot as plt

def create_callbacks(checkpoint_dir='checkpoints', model_name='final_model.keras'):
    """
    Create training callbacks for model checkpointing and early stopping
    
    Args:
        checkpoint_dir: Directory to save model checkpoints
        model_name: Name of the model file
        
    Returns:
        List of callback objects
    """
    # Create checkpoint directory if it doesn't exist
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Model checkpoint - save best model
    checkpoint_path = os.path.join(checkpoint_dir, model_name)
    checkpoint = ModelCheckpoint(
        checkpoint_path,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    # Early stopping - stop if validation loss doesn't improve
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        verbose=1,
        restore_best_weights=True
    )
    
    # Reduce learning rate when validation loss plateaus
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
    
    # TensorBoard for visualization
    log_dir = os.path.join("logs", datetime.now().strftime("%Y%m%d-%H%M%S"))
    tensorboard = TensorBoard(
        log_dir=log_dir,
        histogram_freq=1
    )
    
    return [checkpoint, early_stopping, reduce_lr, tensorboard]

def train_model(model, train_generator, validation_generator, epochs=50, checkpoint_dir='checkpoints', model_name='final_model.keras'):
    """
    Train the model
    
    Args:
        model: Compiled Keras model
        train_generator: Training data generator
        validation_generator: Validation data generator
        epochs: Number of epochs
        checkpoint_dir: Directory to save checkpoints
        model_name: Name of the model file to save
        
    Returns:
        Training history
    """
    # Create checkpoint directory if it doesn't exist
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
        
    checkpoint_path = os.path.join(checkpoint_dir, model_name)
    
    # Callbacks
    # 1. ModelCheckpoint: Save the best model only
    checkpoint = ModelCheckpoint(
        checkpoint_path,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    # 2. ReduceLROnPlateau: Reduce learning rate when learning stops
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=0.00001,
        verbose=1
    )
    
    # 3. EarlyStopping: Stop training if no improvement
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    callbacks_list = [checkpoint, reduce_lr, early_stopping]
    
    print("\n" + "="*50)
    print("Starting Model Training")
    print("="*50)
    print(f"Epochs: {epochs}")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Batch size: {train_generator.batch_size}")
    print(f"Checkpoints will be saved to: {checkpoint_path}")
    print("="*50 + "\n")
    
    # Calculate steps per epoch (robust to small datasets)
    import math
    if train_generator.samples > 0:
        steps_per_epoch = math.ceil(train_generator.samples / train_generator.batch_size)
    else:
        steps_per_epoch = 1 # Fallback, though likely will error later if really 0
        
    # Validation config
    if validation_generator and validation_generator.samples > 0:
        validation_data = validation_generator
        validation_steps = math.ceil(validation_generator.samples / validation_generator.batch_size)
    else:
        print("WARNING: No validation data available. Skipping validation.")
        validation_data = None
        validation_steps = None

    # Calculate class weights for imbalanced datasets
    from sklearn.utils import class_weight
    import numpy as np
    
    class_weights = None
    try:
        # Check if we have classes attribute (standard flow_from_directory)
        if hasattr(train_generator, 'classes'):
            params_weights = class_weight.compute_class_weight(
                class_weight='balanced',
                classes=np.unique(train_generator.classes),
                y=train_generator.classes
            )
            class_weights = dict(enumerate(params_weights))
            print(f"\nDetected Imbalanced Dataset. Using Class Weights: {class_weights}")
            print(f"  (0 = Fake, 1 = Real)")
            print("-" * 50)
    except Exception as e:
        print(f"Warning: Could not calculate class weights: {e}")

    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=validation_data,
        validation_steps=validation_steps,
        callbacks=callbacks_list,
        class_weight=class_weights,
        verbose=1
    )
    
    print("\n" + "="*50)
    print("Training Completed!")
    print("="*50 + "\n")
    
    return history

def plot_training_history(history, save_path='training_history.png'):
    """
    Plot training and validation accuracy/loss
    
    Args:
        history: Training history object
        save_path: Path to save the plot
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nTraining history plot saved to: {save_path}")
    plt.show()

if __name__ == "__main__":
    # This module is meant to be imported, not run directly
    print("This module provides training utilities for the deepfake detection model.")
