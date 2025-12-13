# How to Train the Model

A simple guide to training your deepfake detection model.

## 🏆 The Best Strategy (Simple Version)

Here is the best way to train your model, depending on your goal:

| Goal | Command | Time (Approx) |
| :--- | :--- | :--- |
| **1. Quick Test** | `python main.py --epochs 3` | ~15 mins |
| **2. Good Model** | `python main.py --epochs 20` | ~30-60 mins |
| **3. Max Accuracy** | `python main.py --epochs 10 --fine-tune --load-model checkpoints/final_model.keras` | +1 hour |

### My Recommendation:
Run **Step 2** (20 epochs). It's the perfect balance of speed and accuracy.

---

## 🚀 How to Run Commands

1. Open your terminal.
2. Navigate to the model directory:
   ```bash
   cd model
   ```
3. Copy and paste one of the commands below.

### 1. Start Fresh (Train New Model)
Use this if you want to start from scratch.
```bash
python main.py --epochs 10
```
- Creates a new model.
- Saves result to `checkpoints/final_model.keras`.

### 2. Continue Training (Improve Existing Model)
Use this if you have a model and want to make it smarter.
```bash
python main.py --epochs 5 --load-model checkpoints/final_model.keras
```
- Loads your existing `final_model.keras`.
- Trains it for 5 more rounds.

### 3. Advanced Configuration
For users who want more control over the training process:

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--batch-size` | `32` | Number of images per training step. Reduce if running out of memory. |
| `--img-width`, `--img-height` | `150` | Resolution of input images. Higher = more detail but slower. |
| `--learning-rate` | `0.001` | How fast the model learns. Lower is more stable but slower. |

**Example High-Quality Training:**
```bash
python main.py --epochs 20 --batch-size 16 --img-width 224 --img-height 224
```

---

## 📍 Where is My Model?

Your trained model is saved here:
```
checkpoints/final_model.keras
```
The website uses this exact file to make predictions.

---

## ❓ Common Questions

**What is an epoch?**
One epoch is one full round of studying all the training images. More epochs = more studying.

**How do I know it's working?**
Look for the `val_accuracy` number in the output. If it goes UP, your model is getting smarter!

**How to stop training?**
Press `Ctrl + C` in the terminal. The model saves the best version automatically during training.

---

## 📂 How to Train on Your Own Dataset

If you want to train the model on a completely new dataset (e.g., typical Kaggle structure), follow these steps:

### 1. Prepare Your Data
You can organize your images in one of two ways:

**Option A (Standard Split - Best for Control):**
```
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
```

**Option B (Simple - Easy):**
Just dump your images into two folders. The code will automatically split them (80% train, 20% validation).
```
Dataset/
├── Fake/
└── Real/
```

### 2. Place the Dataset
The code now automatically checks this location first:
1. `~/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image/NewDataset`

If not found there, it checks:
2. Inside the `model` folder.
3. `~/Developer/deepfake/Dataset/Image Dataset`
4. `~/.cache/deepfake-dataset/Dataset`


### 3. Run Training
Once your data is in place, run the standard training command:
```bash
python main.py --epochs 20
```
The script will key off your new `Dataset` folder automatically.

