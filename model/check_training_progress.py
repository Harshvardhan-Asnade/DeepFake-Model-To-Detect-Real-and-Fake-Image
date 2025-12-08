"""
Script to check the current training progress
"""
import os
import glob

def check_training_progress():
    """Check and display current training progress"""
    
    print("=" * 70)
    print(" " * 20 + "TRAINING PROGRESS CHECK")
    print("=" * 70 + "\n")
    
    # Check for saved model checkpoint
    checkpoint_path = "checkpoints/best_model.keras"
    if os.path.exists(checkpoint_path):
        file_size = os.path.getsize(checkpoint_path) / (1024 * 1024)  # Size in MB
        mod_time = os.path.getmtime(checkpoint_path)
        from datetime import datetime
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"✓ Best Model Checkpoint Found:")
        print(f"  - Path: {checkpoint_path}")
        print(f"  - Size: {file_size:.2f} MB")
        print(f"  - Last Updated: {mod_time_str}")
        print()
    else:
        print("✗ No checkpoint found yet (training may have just started)")
        print()
    
    # Check for TensorBoard logs
    log_dirs = glob.glob("logs/*")
    if log_dirs:
        latest_log = max(log_dirs, key=os.path.getmtime)
        print(f"✓ TensorBoard Logs Found:")
        print(f"  - Log Directory: {latest_log}")
        print(f"  - To view live training metrics, run:")
        print(f"    tensorboard --logdir={latest_log}")
        print()
        
        # Check train and validation subdirectories
        train_dir = os.path.join(latest_log, "train")
        val_dir = os.path.join(latest_log, "validation")
        
        if os.path.exists(train_dir):
            train_files = os.listdir(train_dir)
            print(f"  - Training events logged: {len(train_files)} file(s)")
        
        if os.path.exists(val_dir):
            val_files = os.listdir(val_dir)
            print(f"  - Validation events logged: {len(val_files)} file(s)")
        print()
    else:
        print("✗ No TensorBoard logs found yet")
        print()
    
    # Try to parse TensorBoard logs for latest metrics
    try:
        from tensorflow.python.summary.summary_iterator import summary_iterator
        
        print("=" * 70)
        print("LATEST TRAINING METRICS (from TensorBoard logs):")
        print("=" * 70 + "\n")
        
        # Find event files
        train_event_files = glob.glob(os.path.join(latest_log, "train", "events.out.tfevents.*"))
        val_event_files = glob.glob(os.path.join(latest_log, "validation", "events.out.tfevents.*"))
        
        # Parse training metrics
        if train_event_files:
            train_metrics = {}
            for event_file in train_event_files:
                for event in summary_iterator(event_file):
                    for value in event.summary.value:
                        if value.tag not in train_metrics:
                            train_metrics[value.tag] = []
                        train_metrics[value.tag].append((event.step, value.simple_value))
            
            print("Training Metrics:")
            for tag, values in train_metrics.items():
                if values:
                    latest_step, latest_value = values[-1]
                    print(f"  - {tag}: {latest_value:.4f} (Epoch {latest_step + 1})")
            print()
        
        # Parse validation metrics
        if val_event_files:
            val_metrics = {}
            for event_file in val_event_files:
                for event in summary_iterator(event_file):
                    for value in event.summary.value:
                        if value.tag not in val_metrics:
                            val_metrics[value.tag] = []
                        val_metrics[value.tag].append((event.step, value.simple_value))
            
            print("Validation Metrics:")
            for tag, values in val_metrics.items():
                if values:
                    latest_step, latest_value = values[-1]
                    print(f"  - {tag}: {latest_value:.4f} (Epoch {latest_step + 1})")
            print()
        
    except Exception as e:
        print(f"Could not parse TensorBoard logs: {str(e)}")
        print("You can view detailed metrics by running TensorBoard dashboard")
        print()
    
    # Check for training history plot
    if os.path.exists("training_history.png"):
        print("✓ Training History Plot: training_history.png")
    else:
        print("✗ Training History Plot: Not created yet (will be created after training completes)")
    
    print("\n" + "=" * 70)
    print("To view real-time training progress, use TensorBoard:")
    print(f"  tensorboard --logdir=logs")
    print("Then open http://localhost:6006 in your browser")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    check_training_progress()
