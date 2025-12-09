"""
Model Architecture Module for Deepfake Detection
Defines the neural network architecture using transfer learning
"""

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

def create_model(img_width=150, img_height=150, learning_rate=0.001):
    """
    Create a deepfake detection model using EfficientNetB0 as base
    
    Args:
        img_width: Width of input images
        img_height: Height of input images
        learning_rate: Learning rate for optimizer
        
    Returns:
        Compiled Keras model
    """
    IMG_SHAPE = (img_width, img_height, 3)
    
    # Load pre-trained EfficientNetB0 model
    # Upgraded to EfficientNetB0 for >95% accuracy goal
    base_model = EfficientNetB0(
        input_shape=IMG_SHAPE,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the layers of the pre-trained convolutional base
    base_model.trainable = False
    
    # Build the custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    output_layer = Dense(1, activation='sigmoid')(x)
    
    # Combine the pre-trained base and the custom classification head
    model = Model(inputs=base_model.input, outputs=output_layer)
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print("\n" + "="*50)
    print("Model Architecture Summary")
    print("="*50)
    model.summary()
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
    model.compile(
        optimizer=Adam(learning_rate=0.0001),  # Lower learning rate for fine-tuning
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"\nModel recompiled. Last {num_layers_to_unfreeze} layers (excluding BN) are trainable.")
    
    return model

if __name__ == "__main__":
    # Test model creation
    model = create_model()
    print(f"\nTotal parameters: {model.count_params():,}")
    print(f"Trainable parameters: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}")
