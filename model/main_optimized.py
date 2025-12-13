#!/usr/bin/env python3
"""
OPTIMIZED Main Script for Deepfake Detection Model
Orchestrates the entire pipeline with performance optimizations

Usage:
    # Quick train (5 epochs, optimized)
    python main_optimized.py --dataset-path dataset --epochs 5
    
    # Load and continue training
    python main_optimized.py --load-model model/checkpoints/final_model.keras --epochs 10
    
    # Full training with larger batch size
    python main_optimized.py --dataset-path dataset --epochs 20 --batch-size 64
"""

import os
import argparse
from data_preparation_optimized import get_dataset_path, inspect_dataset, create_data_generators_optimized
from model import create_model, unfreeze_base_model
from train_optimized import train_model_optimized, plot_training_history
from evaluate import full_evaluation
from tensorflow.keras.models import load_model
import tensorflow as tf

# Print optimization status
print("\n" + "="*70)
print(" "*20 + "⚡ OPTIMIZATION STATUS ⚡")
print("="*70)
print(f"✓ TensorFlow version: {tf.__version__}")
print(f"✓ GPU Available: {len(tf.config.list_physical_devices('GPU')) > 0}")
print(f"✓ Mixed Precision: {'Enabled' if tf.keras.mixed_precision.global_policy().name == 'mixed_float16' else 'Disabled'}")
print(f"✓ XLA Compilation: Enabled")
print("="*70 + "\n")

def main(args):
    """
    Main function to run the OPTIMIZED deepfake detection pipeline
    
    Args:
        args: Command line arguments
    """
    print("\n" + "="*70)
    print(" "*10 + "🚀 OPTIMIZED DEEPFAKE DETECTION MODEL PIPELINE")
    print("="*70 + "\n")
    
    # Step 1: Get Offline Dataset Path
    print("Step 1: Loading Offline Dataset...")
    dataset_path = get_dataset_path(args.dataset_path)
    full_dataset_path = inspect_dataset(dataset_path)
    
    # Step 2: Create Optimized Data Generators
    print("\nStep 2: Creating OPTIMIZED Data Generators...")
    train_gen, val_gen, test_gen = create_data_generators_optimized(
        full_dataset_path,
        img_width=args.img_width,
        img_height=args.img_height,
        batch_size=args.batch_size
    )
    
    # Step 3: Create or Load Model
    if args.load_model:
        print(f"\nStep 3: Loading Model from {args.load_model}...")
        model = load_model(args.load_model)
        
        # Recompile with optimizations
        print("Recompiling loaded model with optimizations...")
        from tensorflow.keras.optimizers import Adam
        from tensorflow.keras.losses import BinaryFocalCrossentropy
        from tensorflow.keras import mixed_precision
        
        # Create optimizer with mixed precision
        optimizer = Adam(learning_rate=args.learning_rate)
        optimizer = mixed_precision.LossScaleOptimizer(optimizer)
        
        model.compile(
            optimizer=optimizer,
            loss=BinaryFocalCrossentropy(gamma=2.0, from_logits=False),
            metrics=['accuracy']
        )
        
        # Update args with the actual model input shape
        args.img_height = model.input_shape[1]
        args.img_width = model.input_shape[2]
        print(f"✓ Model Input Resolution: {args.img_width}x{args.img_height}")
    else:
        print(f"\nStep 3: Creating {args.model_type} Model...")
        img_width = args.img_width if args.img_width > 0 else None
        img_height = args.img_height if args.img_height > 0 else None
        
        model = create_model(
            model_type=args.model_type,
            img_width=img_width,
            img_height=img_height,
            learning_rate=args.learning_rate
        )
        
        args.img_width = model.input_shape[2]
        args.img_height = model.input_shape[1]
        print(f"✓ Model Input Resolution: {args.img_width}x{args.img_height}")
    
    # Step 4: Train Model (if not skipped)
    if not args.skip_training:
        print("\nStep 4: Training Model with OPTIMIZATIONS...")
        
        # Re-create generators if resolution changed
        if args.img_width != 150 or args.img_height != 150:
             print("Re-creating data generators with correct model resolution...")
             train_gen, val_gen, test_gen = create_data_generators_optimized(
                full_dataset_path,
                img_width=args.img_width,
                img_height=args.img_height,
                batch_size=args.batch_size
            )
            
        history = train_model_optimized(
            model,
            train_gen,
            val_gen,
            epochs=args.epochs,
            checkpoint_dir=args.checkpoint_dir,
            model_name=args.model_name
        )
        
        # Plot training history
        plot_training_history(history, save_path='training_history_optimized.png')
        
        # Fine-tuning (optional)
        if args.fine_tune:
            print("\nStep 4b: Fine-tuning Model...")
            model = unfreeze_base_model(model, num_layers_to_unfreeze=args.unfreeze_layers)
            history_fine = train_model_optimized(
                model,
                train_gen,
                val_gen,
                epochs=args.fine_tune_epochs,
                checkpoint_dir=args.checkpoint_dir
            )
            plot_training_history(history_fine, save_path='fine_tuning_history_optimized.png')
    else:
        print("\nStep 4: Skipping training...")
    
    # Step 5: Evaluate Model
    if not args.skip_evaluation:
        print("\nStep 5: Evaluating Model...")
        full_evaluation(model, test_gen, class_names=['Fake', 'Real'])
    else:
        print("\nStep 5: Skipping evaluation...")
    
    # Save final model
    if args.save_model:
        final_model_path = os.path.join(args.checkpoint_dir, args.model_name)
        model.save(final_model_path)
        print(f"\n✓ Final model saved to: {final_model_path}")
    
    print("\n" + "="*70)
    print(" "*22 + "🎉 PIPELINE COMPLETED!")
    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='OPTIMIZED Deepfake Detection Model Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick optimized training
  python main_optimized.py --epochs 5
  
  # Load and continue training
  python main_optimized.py --load-model model/checkpoints/final_model.keras --epochs 10
  
  # Train with larger batch size for better GPU utilization
  python main_optimized.py --batch-size 64 --epochs 20
        """
    )
    
    # Data parameters
    parser.add_argument('--img-width', type=int, default=0, help='Image width (0 = auto-select)')
    parser.add_argument('--img-height', type=int, default=0, help='Image height (0 = auto-select)')
    parser.add_argument('--batch-size', type=int, default=48, help='Batch size (default: 48, optimized for M4)')
    
    parser.add_argument('--dataset-path', type=str, default=None, help='Path to dataset directory')
    
    # Model parameters
    parser.add_argument('--model-type', type=str, default='EfficientNetB0', 
                       help='Model architecture (EfficientNetB0, EfficientNetB4)')
    
    # Training parameters
    parser.add_argument('--epochs', type=int, default=20, help='Number of training epochs')
    parser.add_argument('--learning-rate', type=float, default=0.001, help='Learning rate')
    
    # Default to 'checkpoints' directory in the same folder as this script
    default_checkpoint_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'checkpoints')
    parser.add_argument('--checkpoint-dir', type=str, default=default_checkpoint_dir, 
                       help='Directory to save checkpoints')
    
    # Fine-tuning parameters
    parser.add_argument('--fine-tune', action='store_true', help='Enable fine-tuning')
    parser.add_argument('--fine-tune-epochs', type=int, default=10, help='Number of fine-tuning epochs')
    parser.add_argument('--unfreeze-layers', type=int, default=20, help='Number of layers to unfreeze')
    
    # Pipeline control
    parser.add_argument('--skip-training', action='store_true', help='Skip training')
    parser.add_argument('--skip-evaluation', action='store_true', help='Skip evaluation')
    parser.add_argument('--load-model', type=str, default=None, help='Path to load existing model')
    parser.add_argument('--save-model', action='store_true', default=True, help='Save final model')
    parser.add_argument('--model-name', type=str, default='final_model.keras', 
                       help='Name of the model file to save')
    
    args = parser.parse_args()
    
    main(args)
