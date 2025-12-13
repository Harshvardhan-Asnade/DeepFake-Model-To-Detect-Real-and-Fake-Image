"""
Model Architecture Module for Deepfake Detection
Defines the neural network architecture using transfer learning
"""

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def create_model(model_type='EfficientNetB0', img_width=None, img_height=None, learning_rate=0.001):
    """
    Create a deepfake detection model using Transfer Learning
    
    Args:
        model_type: Type of EfficientNet model to use (e.g., 'EfficientNetB0', 'EfficientNetB4')
        img_width: Width of input images (optional, defaults to model optimal)
        img_height: Height of input images (optional, defaults to model optimal)
        learning_rate: Learning rate for optimizer
        
    Returns:
        Compiled Keras model
    """
    import tensorflow as tf
    from tensorflow.keras.applications import (
        EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3,
        EfficientNetB4, EfficientNetB5, EfficientNetB6, EfficientNetB7
    )
    
    # Model Configurations (Optimal Resolutions)
    model_config = {
        'EfficientNetB0': {'model': EfficientNetB0, 'res': 224},
        'EfficientNetB1': {'model': EfficientNetB1, 'res': 240},
        'EfficientNetB2': {'model': EfficientNetB2, 'res': 260},
        'EfficientNetB3': {'model': EfficientNetB3, 'res': 300},
        'EfficientNetB4': {'model': EfficientNetB4, 'res': 380},
        'EfficientNetB5': {'model': EfficientNetB5, 'res': 456},
        'EfficientNetB6': {'model': EfficientNetB6, 'res': 528},
        'EfficientNetB7': {'model': EfficientNetB7, 'res': 600},
    }
    
    if model_type not in model_config:
        raise ValueError(f"Invalid model_type. Available: {list(model_config.keys())}")
    
    # Set default resolution if not provided
    if img_width is None or img_height is None:
        default_res = model_config[model_type]['res']
        img_width = default_res
        img_height = default_res
        print(f"Auto-setting resolution to {img_width}x{img_height} for {model_type}")

    IMG_SHAPE = (img_width, img_height, 3)
    
    # Load pre-trained model
    BaseModel = model_config[model_type]['model']
    base_model = BaseModel(
        input_shape=IMG_SHAPE,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the layers of the pre-trained convolutional base
    base_model.trainable = False
    
    # Build the custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    output_layer = Dense(1, activation='sigmoid')(x)
    
    # Combine the pre-trained base and the custom classification head
    model = Model(inputs=base_model.input, outputs=output_layer)
    
    # Compile the model
    # Compile the model
    # Using BinaryFocalCrossentropy (gamma=2.0) to focus on hard examples
    # This is crucial for pushing accuracy from ~90% to 99%
    from tensorflow.keras.losses import BinaryFocalCrossentropy
    
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss=BinaryFocalCrossentropy(gamma=2.0, from_logits=False),
        metrics=['accuracy']
    )
    
    print("\n" + "="*50)
    print(f"Model: {model_type}")
    print(f"Input Shape: {IMG_SHAPE}")
    print("="*50)
    # model.summary() # Commented out to reduce noise, can uncommment if needed
    print("="*50 + "\n")
    
    return model

def unfreeze_base_model(model, num_layers_to_unfreeze=20):
    """
    Unfreeze the last few layers of the base model for fine-tuning
    
    Args:
        model: The compiled model
        num_layers_to_unfreeze: Number of layers to unfreeze from the end
        
    Returns:
        Modified model with unfrozen layers
    """
    # We are using Functional API, so model.layers contains all layers flattened
    
    # 1. Unfreeze all layers initially (so we can selectively freeze) 
    # OR better: Traverse and set.
    
    print(f"Unfreezing last {num_layers_to_unfreeze} layers for fine-tuning...")
    
    # Check total layers
    total_layers = len(model.layers)
    freeze_until = total_layers - num_layers_to_unfreeze
    
    for i, layer in enumerate(model.layers):
        if i < freeze_until:
            layer.trainable = False
        else:
            # Important: Keep BatchNormalization layers frozen during fine-tuning
            # to prevent destroying the learned statistics
            if 'batch_normalization' in layer.name or 'bn' in layer.name:
                layer.trainable = False
            else:
                layer.trainable = True
                
    # Recompile the model with a lower learning rate
    # Recompile the model with a lower learning rate
    # Maintain Focal Loss during fine-tuning
    from tensorflow.keras.losses import BinaryFocalCrossentropy
    
    model.compile(
        optimizer=Adam(learning_rate=0.0001),  # Lower learning rate for fine-tuning
        loss=BinaryFocalCrossentropy(gamma=2.0, from_logits=False),
        metrics=['accuracy']
    )
    
    print(f"\nModel recompiled. Last {num_layers_to_unfreeze} layers (excluding BN) are trainable.")
    
    return model

if __name__ == "__main__":
    # Test model creation
    model = create_model()
    print(f"\nTotal parameters: {model.count_params():,}")
    print(f"Trainable parameters: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}")
