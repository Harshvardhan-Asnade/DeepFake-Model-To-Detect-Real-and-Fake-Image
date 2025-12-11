# 🚀 Quick Reference: Dual Deployment Commands

This is a quick cheat sheet for deploying to both GitHub and Hugging Face.

---

## ⚡ Quick Start (First Time Setup)

```bash
# 1. Run the setup script
./setup_dual_deploy.sh

# 2. Deploy to both platforms
./dual_push.sh
```

---

## 📋 Common Commands

### Deploy to Both Platforms
```bash
./dual_push.sh
```

### Check Git Status
```bash
git status
```

### View Remotes
```bash
git remote -v
```

### Manual Push to GitHub
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Manual Push to Hugging Face
```bash
git push huggingface main
```

---

## 🔧 Setup Commands

### Initialize Git (if needed)
```bash
git init
```

### Add GitHub Remote
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Add Hugging Face Remote
```bash
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
```

### Install Git LFS
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt-get install git-lfs

# After installation
git lfs install
```

### Track Large Files with LFS
```bash
git lfs track "*.keras"
git lfs track "*.h5"
git lfs track "*.pkl"
```

---

## 🐳 Docker Commands (Local Testing)

### Build Docker Image
```bash
docker build -t deepfake-detection .
```

### Run Docker Container
```bash
docker run -p 7860:7860 deepfake-detection
```

### Run in Background
```bash
docker run -d -p 7860:7860 deepfake-detection
```

### View Running Containers
```bash
docker ps
```

### Stop Container
```bash
docker stop <container_id>
```

---

## 🌐 Local Development

### Run Without Docker
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
cd backend
python app.py

# Access at: http://localhost:5001
```

---

## 🔍 Debugging Commands

### Check Git LFS Files
```bash
git lfs ls-files
```

### Check Remote URLs
```bash
git remote get-url origin
git remote get-url huggingface
```

### View Last Commit
```bash
git log -1
```

### Check Branch
```bash
git branch
```

### View Differences
```bash
git diff
```

---

## 🚨 Troubleshooting

### Reset to Last Commit (CAREFUL!)
```bash
git reset --hard HEAD
```

### Unstage All Files
```bash
git reset
```

### Remove File from Staging
```bash
git reset HEAD <filename>
```

### Update Remote URL
```bash
# GitHub
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Hugging Face
git remote set-url huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE
```

### Force Push (DANGEROUS - Use with Caution!)
```bash
git push -f origin main
```

---

## 📦 File Structure

```
.
├── backend/              # Flask application
│   └── app.py           # Main application (Port 7860 for HF, 5001 for local)
├── frontend/            # Web interface
│   ├── static/         # CSS, JS, images
│   └── templates/      # HTML files
├── model/              # ML model files
│   └── checkpoints/    # Trained models
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
├── dual_push.sh       # Deployment script
└── setup_dual_deploy.sh # Setup script
```

---

## 🎯 Deployment Checklist

Before deploying, ensure:

- [ ] Code works locally (`python backend/app.py`)
- [ ] All dependencies in `requirements.txt`
- [ ] Model file exists in `model/checkpoints/`
- [ ] `.gitignore` excludes unnecessary files
- [ ] Git remotes are configured (`git remote -v`)
- [ ] Git LFS is set up for large files
- [ ] Committed all changes (`git status` is clean)

---

## 📚 Resources

- **Full Guide**: `DUAL_DEPLOYMENT_GUIDE.md`
- **GitHub**: https://github.com
- **Hugging Face**: https://huggingface.co
- **Docker Docs**: https://docs.docker.com
- **Git LFS**: https://git-lfs.github.com

---

## 🆘 Need Help?

1. Read `DUAL_DEPLOYMENT_GUIDE.md` for detailed instructions
2. Check Hugging Face build logs on your Space page
3. Verify Docker builds locally: `docker build -t test .`
4. Check GitHub Actions (if configured)

---

**Last Updated**: 2025-12-11
