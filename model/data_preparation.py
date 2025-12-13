"""
Data Preparation Module for Deepfake Detection
Prepares the offline dataset for training
"""

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_dataset_path(path_arg=None):
    """
    Get the path to the offline dataset.
    Checks common locations and returns the path if found.
    """
    # Check if a specific path was provided
    if path_arg and os.path.exists(path_arg):
        print(f"Using dataset from provided path: {path_arg}")
        return os.path.abspath(path_arg)

    # Check for "dataset" (lowercase) in current directory
    if os.path.exists("dataset"):
         return os.path.abspath("dataset")

    # Check for "Dataset" (uppercase) in current directory
    if os.path.exists("Dataset"):
         return os.path.abspath("Dataset")
    
    # User specific new path (High Priority)
    new_dataset_path = "/Users/harshvardhan/Developer/deepfake/Dataset"
    
    # Heuristic: Check if this path contains the actual data or a subfolder
    if os.path.exists(new_dataset_path):
        # Specific fix for the user's specific path structure if known or seemingly nested
        # If "Image Dataset" folder exists inside, go into it.
        possible_subfolder = os.path.join(new_dataset_path, "Image Dataset")
        if os.path.exists(possible_subfolder) and os.path.isdir(possible_subfolder):
             new_dataset_path = possible_subfolder
             print(f"Auto-adjusting path to nested folder: {new_dataset_path}")
             
        print(f"Using dataset from: {new_dataset_path}")
        return new_dataset_path

    
    # Common dataset locations
    mac_deepfake_path = os.path.expanduser("~/Developer/deepfake/Dataset/Image Dataset")
    default_path = os.path.expanduser("~/.cache/deepfake-dataset/Dataset")
    
    # Alternative local path
    local_path = os.path.join(os.getcwd(), "Dataset")

    # User provided path (Windows)
    user_path = "C:\\Dataset"
    
    # Check if dataset exists in Mac deepfake location (first priority)
    if os.path.exists(mac_deepfake_path):
        print(f"Using dataset from: {mac_deepfake_path}")
        return mac_deepfake_path
    # Check if dataset exists in default location
    elif os.path.exists(default_path):
        print(f"Using dataset from: {default_path}")
        return default_path
    # Check if dataset exists in local directory
    elif os.path.exists(local_path):
        print(f"Using dataset from: {local_path}")
        return local_path
    # Check if dataset exists in user provided location
    elif os.path.exists(user_path):
        print(f"Using dataset from: {user_path}")
        return user_path
    else:
        error_msg = f"""
Dataset not found! Please ensure the dataset exists in one of these locations:
1. {new_dataset_path}
2. {mac_deepfake_path}
3. {default_path}
4. {local_path}

The dataset should have the following structure:
Option A (Standard):
Dataset/
├── Train/
│   ├── Fake/
│   └── Real/
├── Validation/ (...)
└── Test/ (...)

Option B (Simple):
Dataset/
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
    
    
    # Check for standard split structure
    is_standard_split = os.path.exists(os.path.join(dataset_path, 'Train'))
    
    if is_standard_split:
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
    else:
        # Check for simple flat structure
        print("\nStandard Train/Validation/Test structure not found. Checking for flat Real/Fake structure...")
        classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
        print(f"Found folders: {classes}")
        
        for cls in classes:
             cls_path = os.path.join(dataset_path, cls)
             num_files = len([f for f in os.listdir(cls_path) if os.path.isfile(os.path.join(cls_path, f))])
             print(f"  {cls}: {num_files} images")
             
    return dataset_path

def create_data_generators(dataset_path, img_width=150, img_height=150, batch_size=32):
    """
    Create data generators for training, validation, and testing
    """
    from tensorflow.keras.applications.efficientnet import preprocess_input

    # Check if we have standard split or flat structure
    if os.path.exists(os.path.join(dataset_path, 'Train')):
        # Standard Split Structure
        print("\nUsing Standard Split Structure (Train/Test/Validation)...")
        
        # Data augmentation for training set
        train_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest'
        )
        
        # Preprocessing only for validation and test sets
        validation_test_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input
        )
        
        train_generator = train_datagen.flow_from_directory(
            os.path.join(dataset_path, 'Train'),
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary'
        )
        
        validation_generator = validation_test_datagen.flow_from_directory(
            os.path.join(dataset_path, 'Validation'),
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary'
        )
        
        test_generator = validation_test_datagen.flow_from_directory(
            os.path.join(dataset_path, 'Test'),
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary',
            shuffle=False
        )
        
    else:
        # Flat Structure (Auto-Split)
        print("\nUsing Flat Structure (Auto-Splitting Real/Fake)...")
        print("Note: Using 80% for training, 20% for validation/testing")
        
        # Add validation split to datagen
        train_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=[0.8, 1.2],
            fill_mode='nearest',
            validation_split=0.2  # Use 20% for validation
        )
        
        train_generator = train_datagen.flow_from_directory(
            dataset_path,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='training'
        )
        
        validation_generator = train_datagen.flow_from_directory(
            dataset_path,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='validation'
        )
        
        # For flat structure, we use validation set as test set too
        test_generator = validation_generator

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

