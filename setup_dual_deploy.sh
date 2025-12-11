#!/bin/bash

# ════════════════════════════════════════════════════════════════
# Setup Script for Dual Deployment (GitHub + Hugging Face)
# ════════════════════════════════════════════════════════════════

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║     🚀 DUAL DEPLOYMENT SETUP 🚀                       ║"
echo "║     Configure GitHub + Hugging Face                   ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# ════════════════════════════════════════════════════════════════
# Step 1: Check if Git is initialized
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[1/7] 📦 Checking Git initialization...${NC}"

if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Git not initialized. Initializing now...${NC}"
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
else
    echo -e "${GREEN}✓ Git already initialized${NC}"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 2: Install Git LFS
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[2/7] 📦 Setting up Git LFS...${NC}"

if command -v git-lfs &> /dev/null; then
    echo -e "${GREEN}✓ Git LFS is installed${NC}"
    git lfs install
else
    echo -e "${YELLOW}⚠️  Git LFS not found. Please install it:${NC}"
    echo -e "${CYAN}macOS:     brew install git-lfs${NC}"
    echo -e "${CYAN}Ubuntu:    sudo apt-get install git-lfs${NC}"
    echo -e "${CYAN}Windows:   Download from https://git-lfs.github.com${NC}"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 3: Configure Git user
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[3/7] 👤 Configuring Git user...${NC}"

GIT_NAME=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_NAME" ]; then
    read -p "Enter your name: " name
    git config --global user.name "$name"
    echo -e "${GREEN}✓ Git name set to: $name${NC}"
else
    echo -e "${GREEN}✓ Git name already set: $GIT_NAME${NC}"
fi

if [ -z "$GIT_EMAIL" ]; then
    read -p "Enter your email: " email
    git config --global user.email "$email"
    echo -e "${GREEN}✓ Git email set to: $email${NC}"
else
    echo -e "${GREEN}✓ Git email already set: $GIT_EMAIL${NC}"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 4: Setup GitHub Remote
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[4/7] 🐙 Setting up GitHub remote...${NC}"

if git remote | grep -q '^origin$'; then
    ORIGIN_URL=$(git remote get-url origin)
    echo -e "${GREEN}✓ GitHub remote already exists: $ORIGIN_URL${NC}"
else
    echo -e "${CYAN}Enter your GitHub repository URL:${NC}"
    echo -e "${CYAN}Example: https://github.com/YOUR_USERNAME/Deepfake-Model-To-Detect-Real-and-Fake-Image.git${NC}"
    read -p "> " github_url
    
    if [ -n "$github_url" ]; then
        git remote add origin "$github_url"
        echo -e "${GREEN}✓ GitHub remote added: $github_url${NC}"
    else
        echo -e "${YELLOW}⚠️  Skipped GitHub remote setup${NC}"
    fi
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 5: Setup Hugging Face Remote
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[5/7] 🤗 Setting up Hugging Face remote...${NC}"

if git remote | grep -q '^huggingface$'; then
    HF_URL=$(git remote get-url huggingface)
    echo -e "${GREEN}✓ Hugging Face remote already exists: $HF_URL${NC}"
else
    echo -e "${CYAN}Enter your Hugging Face Space URL:${NC}"
    echo -e "${CYAN}Example: https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection${NC}"
    read -p "> " hf_url
    
    if [ -n "$hf_url" ]; then
        git remote add huggingface "$hf_url"
        echo -e "${GREEN}✓ Hugging Face remote added: $hf_url${NC}"
    else
        echo -e "${YELLOW}⚠️  Skipped Hugging Face remote setup${NC}"
    fi
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 6: Setup Git LFS tracking
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[6/7] 📦 Configuring Git LFS for large files...${NC}"

# Create .gitattributes if it doesn't exist
if [ ! -f ".gitattributes" ]; then
    touch .gitattributes
fi

# Track model files
git lfs track "*.keras"
git lfs track "*.h5"
git lfs track "*.pkl"
git lfs track "*.pb"

echo -e "${GREEN}✓ Git LFS configured to track model files${NC}"
echo ""

# ════════════════════════════════════════════════════════════════
# Step 7: Show remotes
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[7/7] 📋 Current Git remotes:${NC}"
git remote -v
echo ""

# ════════════════════════════════════════════════════════════════
# Summary and Next Steps
# ════════════════════════════════════════════════════════════════
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║              SETUP COMPLETE! ✅                        ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}🎉 Your dual deployment is ready!${NC}\n"

echo -e "${CYAN}Next Steps:${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────${NC}"
echo -e "1. ${YELLOW}Review your changes:${NC}"
echo -e "   ${CYAN}git status${NC}\n"

echo -e "2. ${YELLOW}Deploy to both platforms:${NC}"
echo -e "   ${CYAN}./dual_push.sh${NC}\n"

echo -e "3. ${YELLOW}Read the full deployment guide:${NC}"
echo -e "   ${CYAN}cat DUAL_DEPLOYMENT_GUIDE.md${NC}\n"

echo -e "${CYAN}─────────────────────────────────────────────────────${NC}"
echo -e "${GREEN}💡 Tips:${NC}"
echo -e "  • Make the script executable: ${CYAN}chmod +x dual_push.sh${NC}"
echo -e "  • Check remotes anytime: ${CYAN}git remote -v${NC}"
echo -e "  • View LFS tracked files: ${CYAN}git lfs ls-files${NC}"
echo -e "${CYAN}─────────────────────────────────────────────────────${NC}\n"
