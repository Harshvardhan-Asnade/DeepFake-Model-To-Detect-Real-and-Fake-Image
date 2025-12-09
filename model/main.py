"""
Main Script for Deepfake Detection Model
Orchestrates the entire pipeline: data preparation, model creation, training, and evaluation
"""

import os
import argparse
from data_preparation import get_dataset_path, inspect_dataset, create_data_generators
from model import create_model, unfreeze_base_model
from train import train_model, plot_training_history
from evaluate import full_evaluation
from tensorflow.keras.models import load_model

def main(args):
    """
    Main function to run the deepfake detection pipeline
    
    Args:
        args: Command line arguments
    """
    print("\n" + "="*70)
    print(" "*15 + "DEEPFAKE DETECTION MODEL PIPELINE")
    print("="*70 + "\n")
    
    # Step 1: Get Offline Dataset Path
    print("Step 1: Loading Offline Dataset...")
    dataset_path = get_dataset_path()
    full_dataset_path = inspect_dataset(dataset_path)
    
    # Step 2: Create Data Generators
    print("\nStep 2: Creating Data Generators...")
    train_gen, val_gen, test_gen = create_data_generators(
        full_dataset_path,
        img_width=args.img_width,
        img_height=args.img_height,
        batch_size=args.batch_size
    )
    
    # Step 3: Create or Load Model
    if args.load_model:
        print(f"\nStep 3: Loading Model from {args.load_model}...")
        model = load_model(args.load_model)
    else:
        print("\nStep 3: Creating Model...")
        model = create_model(
            img_width=args.img_width,
            img_height=args.img_height,
            learning_rate=args.learning_rate
        )
    
    # Step 4: Train Model (if not skipped)
    if not args.skip_training:
        print("\nStep 4: Training Model...")
        history = train_model(
            model,
            train_gen,
            val_gen,
            epochs=args.epochs,
            checkpoint_dir=args.checkpoint_dir,
            model_name=args.model_name
        )
        
        # Plot training history
        plot_training_history(history, save_path='training_history.png')
        
        # Fine-tuning (optional)
        if args.fine_tune:
            print("\nStep 4b: Fine-tuning Model...")
            model = unfreeze_base_model(model, num_layers_to_unfreeze=args.unfreeze_layers)
            history_fine = train_model(
                model,
                train_gen,
                val_gen,
                epochs=args.fine_tune_epochs,
                checkpoint_dir=args.checkpoint_dir
            )
            plot_training_history(history_fine, save_path='fine_tuning_history.png')
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
        print(f"\nFinal model saved to: {final_model_path}")
    
    print("\n" + "="*70)
    print(" "*20 + "PIPELINE COMPLETED!")
    print("="*70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deepfake Detection Model Pipeline')
    
    # Data parameters
    parser.add_argument('--img-width', type=int, default=150, help='Image width')
    parser.add_argument('--img-height', type=int, default=150, help='Image height')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    
    # Training parameters
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--learning-rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--checkpoint-dir', type=str, default='checkpoints', help='Directory to save checkpoints')
    
    # Fine-tuning parameters
    parser.add_argument('--fine-tune', action='store_true', help='Enable fine-tuning')
    parser.add_argument('--fine-tune-epochs', type=int, default=20, help='Number of fine-tuning epochs')
    parser.add_argument('--unfreeze-layers', type=int, default=20, help='Number of layers to unfreeze for fine-tuning')
    
    # Pipeline control
    parser.add_argument('--skip-training', action='store_true', help='Skip training')
    parser.add_argument('--skip-evaluation', action='store_true', help='Skip evaluation')
    parser.add_argument('--load-model', type=str, default=None, help='Path to load existing model')
    parser.add_argument('--save-model', action='store_true', default=True, help='Save final model')
    parser.add_argument('--model-name', type=str, default='final_model.keras', help='Name of the model file to save')
    
    args = parser.parse_args()
    
    main(args)
