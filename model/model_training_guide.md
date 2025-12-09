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

1. Open your terminal (Command Prompt or PowerShell).
2. Navigate to the model directory:
   ```bash
   cd c:\Deepfake\model
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
