
# Deepfake Model Training on Mac M4 (Apple Silicon)

## Prerequisite
Ensure you have the dataset folder `Dataset` (containing Train/Test folders) inside the `Deepfake/model` folder (or know its path).

## Step 1: Install Python & Environment
Open your Terminal on Mac and run:

```bash
# Install Miniforge (if you don't have it) or use Homebrew
brew install python@3.10

# Go to project folder
cd /path/to/Deepfake

# Create a virtual environment
python3.10 -m venv venv
source venv/bin/activate
```

## Step 2: Install TensorFlow for Mac (Metal)
This enables the M4 GPU acceleration.

```bash
pip install tensorflow-macos tensorflow-metal matplotlib scikit-learn
```

## Step 3: Train the Model
This command uses your M4 GPU to train EfficientNetB0 efficiently.

```bash
cd model
python main.py --epochs 10 --batch-size 32 --model-name final_model_m4.keras
```

## Step 4: Verify
After training, copy the `final_model_m4.keras` file back to your project backend if you want to deploy it.
