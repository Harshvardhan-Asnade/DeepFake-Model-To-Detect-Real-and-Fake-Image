# How to Train the Model

Simple guide to training your deepfake detection model.

## 🚀 Quick Start

### First Time Training
```bash
python main.py --epochs 3
```
This trains a **new model** for 3 epochs and saves it to `checkpoints/best_model.keras`.

---

## 📚 Training Options

### 1. Train New Model (Start Fresh)
```bash
python main.py --epochs 10
```
- Creates a brand new model
- Trains for 10 epochs
- **Overwrites** any existing model

### 2. Continue Training (Add More Epochs)
```bash
python main.py --epochs 5 --load-model checkpoints/best_model.keras
```
- Loads your existing trained model
- Trains for 5 **additional** epochs
- Model gets **6 epochs total** of knowledge (if previous had 3)
- Epoch counter shows 1/5, 2/5... but model improves from where it left off

### 3. Fast Training (Large Batches)
```bash
python main.py --epochs 3 --batch-size 64
```
- Larger batch size = faster training
- Uses more memory

### 4. Custom Learning Rate
```bash
python main.py --epochs 10 --learning-rate 0.0005
```
- Lower learning rate = slower but more precise training
- Default is 0.001

---

## 💡 Understanding Epochs

### What are epochs?
One epoch = model sees **all training images once**

### How many epochs to use?
- **Quick test**: 3-5 epochs (~10-15 mins)
- **Good model**: 10-20 epochs (~30-60 mins)
- **Best model**: 50+ epochs (several hours)

### Example:
```bash
# Quick test (fast)
python main.py --epochs 3

# Production quality (better)
python main.py --epochs 20
```

---

## 📊 What Happens During Training?

```
Epoch 1/3: val_accuracy improved from None to 0.77780
```

**What this means:**
- `Epoch 1/3`: Training epoch 1 of 3
- `val_accuracy`: Validation accuracy (how good the model is)
- `None`: No previous best (first epoch)
- `0.77780`: Current accuracy (77.78%)
- Model is **saved** automatically if it's the best so far!

---

## 🎯 Common Commands

### Start fresh training
```bash
python main.py --epochs 10
```

### Add 5 more epochs to existing model
```bash
python main.py --epochs 5 --load-model checkpoints/best_model.keras
```

### Only evaluate (no training)
```bash
python main.py --skip-training --load-model checkpoints/best_model.keras
```

---

## ⚠️ Important Notes

1. **Starting Fresh vs Continuing**
   - `python main.py --epochs 3` → Starts from scratch (overwrites old model)
   - `python main.py --epochs 3 --load-model checkpoints/best_model.keras` → Continues training

2. **Model is Auto-Saved**
   - Best model automatically saved to `checkpoints/best_model.keras`
   - Only saves when validation accuracy **improves**

3. **Epoch Counter Resets**
   - When using `--load-model`, counter shows 1/3, 2/3, 3/3
   - But model **keeps** all previous training knowledge!

---

## 🏆 Pro Tips

✅ **Start small**: Test with 3 epochs first  
✅ **Then continue**: Add more epochs using `--load-model`  
✅ **Monitor progress**: Watch the validation accuracy improve  
✅ **Be patient**: Good models take time (20+ epochs recommended)  

---

## 📍 Where is My Model?

Your trained model is saved at:
```
checkpoints/best_model.keras
```

Use it with the web app or for evaluation!

---

## Quick Reference

| Command | What It Does |
|---------|-------------|
| `--epochs 10` | Train for 10 epochs |
| `--batch-size 64` | Use larger batches (faster) |
| `--learning-rate 0.0005` | Set custom learning rate |
| `--load-model checkpoints/best_model.keras` | Continue from saved model |
| `--skip-training` | Only evaluate, don't train |
| `--fine-tune` | Enable advanced fine-tuning |

---

**That's it! Start with 3 epochs and work your way up!** 🚀
