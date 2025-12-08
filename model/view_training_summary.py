"""
Quick script to view training summary
"""
import os
from datetime import datetime

def print_training_summary():
    """Print a summary of the training status"""
    
    print("\n" + "=" * 80)
    print(" " * 25 + "🤖 DEEPFAKE DETECTION MODEL")
    print(" " * 28 + "TRAINING SUMMARY")
    print("=" * 80 + "\n")
    
    # Check checkpoint
    checkpoint_path = "checkpoints/best_model.keras"
    if os.path.exists(checkpoint_path):
        file_size = os.path.getsize(checkpoint_path) / (1024 * 1024)
        mod_time = os.path.getmtime(checkpoint_path)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        time_diff = datetime.now() - datetime.fromtimestamp(mod_time)
        minutes_ago = int(time_diff.total_seconds() / 60)
        
        print("📊 MODEL CHECKPOINT STATUS:")
        print("-" * 80)
        print(f"  ✓ Status: SAVED")
        print(f"  📁 Location: {checkpoint_path}")
        print(f"  📦 Size: {file_size:.2f} MB")
        print(f"  🕒 Last Updated: {mod_time_str} ({minutes_ago} minutes ago)")
        print()
    else:
        print("📊 MODEL CHECKPOINT STATUS:")
        print("-" * 80)
        print("  ⏳ Waiting for first epoch to complete...")
        print()
    
    # Check logs
    log_dir = "logs/20251208-165604"
    if os.path.exists(log_dir):
        print("📈 TENSORBOARD LOGS:")
        print("-" * 80)
        print(f"  ✓ Log Directory: {log_dir}")
        
        train_dir = os.path.join(log_dir, "train")
        val_dir = os.path.join(log_dir, "validation")
        
        if os.path.exists(train_dir):
            print(f"  ✓ Training logs: ACTIVE")
        if os.path.exists(val_dir):
            print(f"  ✓ Validation logs: ACTIVE")
        print()
    
    # Training configuration
    print("⚙️  TRAINING CONFIGURATION:")
    print("-" * 80)
    print("  • Epochs: 10")
    print("  • Batch Size: 32")
    print("  • Image Size: 150x150")
    print("  • Architecture: EfficientNetB0 (Transfer Learning)")
    print()
    
    # Instructions
    print("🔍 HOW TO VIEW DETAILED TRAINING PROGRESS:")
    print("-" * 80)
    print("  1. Open TensorBoard Dashboard:")
    print("     → Run: tensorboard --logdir=logs")
    print("     → Open: http://localhost:6006")
    print()
    print("  2. View real-time metrics:")
    print("     • Training & Validation Accuracy")
    print("     • Training & Validation Loss")
    print("     • Learning Rate")
    print()
    
    print("=" * 80)
    print(" " * 25 + "Training is currently IN PROGRESS...")
    print(" " * 20 + "The training history plot will be saved when")
    print(" " * 25 + "training completes as 'training_history.png'")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    print_training_summary()
