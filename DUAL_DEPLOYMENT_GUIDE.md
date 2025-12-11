# 🚀 Dual Deployment Guide: Git + Hugging Face (FREE)

This guide will help you deploy your Deepfake Detection System to **both GitHub and Hugging Face Spaces** for free, using the same folder and Docker.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Creating Dockerfile](#creating-dockerfile)
4. [Hugging Face Configuration](#hugging-face-configuration)
5. [Dual Push Script](#dual-push-script)
6. [Deployment Steps](#deployment-steps)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

Before starting, ensure you have:

- ✅ Git installed on your system
- ✅ GitHub account ([Sign up here](https://github.com/join))
- ✅ Hugging Face account ([Sign up here](https://huggingface.co/join))
- ✅ Git LFS installed (for large model files)
- ✅ Your project working locally

---

## �️ Initial Setup

### Step 1: Install Git LFS (Large File Storage)

Git LFS is needed for large model files (`.keras`, `.h5`).

```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# Windows (download from)
# https://git-lfs.github.com
```

After installation:
```bash
git lfs install
```

### Step 2: Configure Git

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 3: Create Hugging Face Token

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Name it (e.g., `deepfake-deploy`)
4. Select **"Write"** permission
5. Copy the token (you'll need it later)

---

## 🐳 Creating Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
# Use official Python runtime
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Set environment variable for Flask
ENV FLASK_APP=backend/app.py
ENV PORT=7860

# Run the application
CMD ["python", "backend/app.py"]
```

---

## 📝 Hugging Face Configuration

### Step 1: Create `.spacesignore` file

This tells Hugging Face what NOT to upload:

```
venv/
__pycache__/
*.pyc
.git/
.DS_Store
*.log
.env
```

### Step 2: Create `README.md` for Hugging Face

Create a special `README_HF.md` that will be copied to Hugging Face:

```markdown
---
title: Deepfake Detection System
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Deepfake Detection System

A high-performance deep learning system to detect deepfake images with **91.6% accuracy**.

## 🚀 Try it out!

Upload an image to check if it's real or fake!

## 🧠 Model

- Architecture: EfficientNetB0 (Fine-Tuned)
- Accuracy: 91.56%
- Framework: TensorFlow/Keras

## 📚 Documentation

For full documentation, visit the [GitHub Repository](https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image)
```

### Step 3: Modify `backend/app.py` for Hugging Face

Update your Flask app to use the correct port:

```python
import os

# ... your existing code ...

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))  # Hugging Face uses 7860
    app.run(host='0.0.0.0', port=port, debug=False)
```

---

## 🔄 Dual Push Script

Create `dual_push.sh` in your project root:

```bash
#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Dual Deployment: Git + HF      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════╝${NC}"

# Get commit message
read -p "Enter commit message: " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Track large files with Git LFS
echo -e "\n${BLUE}[1/6] Setting up Git LFS...${NC}"
git lfs track "*.keras"
git lfs track "*.h5"
git add .gitattributes

# Add all changes
echo -e "${BLUE}[2/6] Staging changes...${NC}"
git add .

# Commit changes
echo -e "${BLUE}[3/6] Committing changes...${NC}"
git commit -m "$commit_msg"

# Push to GitHub
echo -e "${BLUE}[4/6] Pushing to GitHub...${NC}"
git push origin main || git push origin master

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub!${NC}"
else
    echo -e "${RED}✗ Failed to push to GitHub${NC}"
    exit 1
fi

# Push to Hugging Face
echo -e "\n${BLUE}[5/6] Pushing to Hugging Face...${NC}"
if git remote | grep -q 'huggingface'; then
    git push huggingface main
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully pushed to Hugging Face!${NC}"
    else
        echo -e "${RED}✗ Failed to push to Hugging Face${NC}"
    fi
else
    echo -e "${RED}✗ Hugging Face remote not configured${NC}"
    echo -e "${BLUE}Run setup first:${NC}"
    echo "git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME"
fi

echo -e "\n${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Deployment Complete! 🎉       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
```

Make it executable:
```bash
chmod +x dual_push.sh
```

---

## 🚀 Deployment Steps

### Part A: GitHub Setup

1. **Create GitHub Repository**:
   - Go to [github.com/new](https://github.com/new)
   - Name: `Deepfake-Model-To-Detect-Real-and-Fake-Image`
   - Make it **Public**
   - Don't initialize with README (you already have one)

2. **Connect Local Repo to GitHub**:
   ```bash
   cd /Users/harshvardhan/Developer/Deepfake-Model-To-Detect-Real-and-Fake-Image
   
   # Initialize git (if not already done)
   git init
   
   # Add GitHub remote
   git remote add origin https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image.git
   ```

### Part B: Hugging Face Setup

1. **Create Hugging Face Space**:
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Space name: `deepfake-detection`
   - License: `MIT`
   - SDK: **Docker**
   - Make it **Public** (for free hosting)
   - Click **Create Space**

2. **Connect Local Repo to Hugging Face**:
   ```bash
   # Add Hugging Face remote
   git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection
   
   # Configure Hugging Face credentials
   git config credential.helper store
   ```

3. **Set up Git LFS for Large Files**:
   ```bash
   # Track model files with LFS
   git lfs track "*.keras"
   git lfs track "*.h5"
   git lfs track "*.pkl"
   
   # Add .gitattributes
   git add .gitattributes
   ```

### Part C: Deploy to Both Platforms

1. **First Deployment**:
   ```bash
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial deployment: Deepfake Detection System"
   
   # Push to GitHub
   git push -u origin main
   
   # Push to Hugging Face
   git push huggingface main
   ```

2. **For Future Updates** (Easy Way):
   ```bash
   # Just run the dual push script!
   ./dual_push.sh
   ```

---

## 🎯 Using the Dual Push Workflow

After initial setup, deploying updates is super simple:

```bash
# Make your changes to code...

# Run the dual push script
./dual_push.sh
```

The script will:
1. ✅ Track large files with Git LFS
2. ✅ Stage all changes
3. ✅ Commit with your message
4. ✅ Push to GitHub
5. ✅ Push to Hugging Face
6. ✅ Show success/failure for each

---

## � What Gets Deployed Where?

| Item | GitHub | Hugging Face |
|------|--------|--------------|
| Source Code | ✅ Yes | ✅ Yes |
| Model Files (.keras) | ✅ Yes (via LFS) | ✅ Yes (via LFS) |
| Documentation | ✅ Yes | ✅ Yes |
| Frontend | ✅ Yes | ✅ Yes (served via Docker) |
| Backend | ✅ Yes | ✅ Yes (runs via Docker) |
| Virtual Env | ❌ No (.gitignore) | ❌ No (.spacesignore) |

---

## 🔧 Troubleshooting

### Issue 1: "Failed to push large file"

**Solution**: Make sure Git LFS is tracking the file:
```bash
git lfs track "*.keras"
git lfs track "*.h5"
git add .gitattributes
git add your-large-file.keras
git commit -m "Add large file with LFS"
```

### Issue 2: "Repository not found" (Hugging Face)

**Solution**: Check your remote URL:
```bash
git remote -v
# Should show:
# huggingface  https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE (fetch)
# huggingface  https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE (push)
```

Update if needed:
```bash
git remote set-url huggingface https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
```

### Issue 3: Docker Build Fails on Hugging Face

**Check the logs** on your Space page. Common fixes:

1. **Port mismatch**: Ensure `backend/app.py` uses port 7860
2. **Missing dependencies**: Check `requirements.txt`
3. **Path issues**: Use relative paths in code

### Issue 4: Model File Too Large

Hugging Face free tier supports files up to **10GB** total. If exceeded:

1. **Optimize model**:
   ```python
   # Use float16 instead of float32
   model.save('model.keras', save_format='keras')
   ```

2. **Compress model** (if possible):
   ```bash
   tar -czf model.tar.gz model/*.keras
   ```

### Issue 5: "Authentication Failed"

**For GitHub**:
```bash
# Use Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens
git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/YOUR_USERNAME/REPO.git main
```

**For Hugging Face**:
```bash
# Use your HF token
git push https://YOUR_USERNAME:YOUR_HF_TOKEN@huggingface.co/spaces/YOUR_USERNAME/SPACE.git main
```

---

## 🌟 Best Practices

1. **Always test locally first** before pushing
2. **Use meaningful commit messages**
3. **Keep `.gitignore` updated** to exclude unnecessary files
4. **Monitor Hugging Face build logs** after pushing
5. **Tag important releases**:
   ```bash
   git tag -a v1.0 -m "First stable release"
   git push origin v1.0
   git push huggingface v1.0
   ```

---

## 📊 Checking Deployment Status

### GitHub
- Visit: `https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image`
- Check for latest commit

### Hugging Face
- Visit: `https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection`
- Check **"Building"** status
- Once built, app will be live!

---

## 🎉 Success!

Your app is now deployed to:
- 📁 **GitHub**: `https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image`
- 🤗 **Hugging Face**: `https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection`

Share your Hugging Face Space with anyone - it's **100% FREE** hosting! 🚀

---

## 📚 Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Docker Documentation](https://docs.docker.com/)
- [Git LFS Documentation](https://git-lfs.github.com/)
- [GitHub Pages](https://pages.github.com/) (for hosting documentation)

---

**Need help?** Open an issue on GitHub or check the [Hugging Face Forums](https://discuss.huggingface.co/)!
