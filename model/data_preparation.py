"""
Data Preparation Module for Deepfake Detection
Prepares the offline dataset for training
"""

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_dataset_path():
    """
    Get the path to the offline dataset.
    Checks common locations and returns the path if found.
    """
    # Default cached dataset location
    default_path = os.path.expanduser("~/.cache/deepfake-dataset/Dataset")
    
    # Alternative local path
    local_path = os.path.join(os.getcwd(), "Dataset")
    
    # Check if dataset exists in default location
    if os.path.exists(default_path):
        print(f"Using dataset from: {default_path}")
        return default_path
    # Check if dataset exists in local directory
    elif os.path.exists(local_path):
        print(f"Using dataset from: {local_path}")
        return local_path
    else:
        error_msg = f"""
Dataset not found! Please ensure the dataset exists in one of these locations:
1. {default_path}
2. {local_path}

The dataset should have the following structure:
Dataset/
├── Train/
│   ├── Fake/
│   └── Real/
├── Validation/
│   ├── Fake/
│   └── Real/
└── Test/
    ├── Fake/
    └── Real/
"""
        raise FileNotFoundError(error_msg)

def inspect_dataset(dataset_path):
    """
    Inspect the structure of the offline dataset
    """
    print(f"\nInspecting dataset at: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset path does not exist: {dataset_path}")
    
    # Check each split
    for split in ['Train', 'Validation', 'Test']:
        split_path = os.path.join(dataset_path, split)
        if os.path.exists(split_path):
            classes = os.listdir(split_path)
            print(f"\n{split} split contains: {classes}")
            
            for cls in classes:
                cls_path = os.path.join(split_path, cls)
                if os.path.isdir(cls_path):
                    num_files = len([f for f in os.listdir(cls_path) if os.path.isfile(os.path.join(cls_path, f))])
                    print(f"  {cls}: {num_files} images")
    
    return dataset_path

def create_data_generators(dataset_path, img_width=150, img_height=150, batch_size=32):
    """
    Create data generators for training, validation, and testing
    """
    # Data augmentation for training set
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # Only rescaling for validation and test sets (no augmentation)
    validation_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Construct full paths to the data directories
    train_data_dir = os.path.join(dataset_path, 'Train')
    validation_data_dir = os.path.join(dataset_path, 'Validation')
    test_data_dir = os.path.join(dataset_path, 'Test')
    
    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary'
    )
    
    validation_generator = validation_test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary'
    )
    
    test_generator = validation_test_datagen.flow_from_directory(
        test_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='binary',
        shuffle=False  # Keep data in order for evaluation
    )
    
    print("\nData generators created successfully!")
    print(f"Training samples: {train_generator.samples}")
    print(f"Validation samples: {validation_generator.samples}")
    print(f"Test samples: {test_generator.samples}")
    
    return train_generator, validation_generator, test_generator

if __name__ == "__main__":
    # Get offline dataset path
    dataset_path = get_dataset_path()
    
    # Inspect dataset
    full_dataset_path = inspect_dataset(dataset_path)
    
    # Create data generators
    train_gen, val_gen, test_gen = create_data_generators(full_dataset_path)

