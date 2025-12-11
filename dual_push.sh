#!/bin/bash

# ════════════════════════════════════════════════════════════════
# Dual Push Script - Deploy to GitHub AND Hugging Face
# ════════════════════════════════════════════════════════════════

# Colors for beautiful output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print header
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║     🚀 DUAL DEPLOYMENT SYSTEM 🚀                      ║"
echo "║     GitHub + Hugging Face Sync                        ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get commit message from user
echo -e "${CYAN}📝 Enter your commit message:${NC}"
read -p "> " commit_msg

# Use default message if none provided
if [ -z "$commit_msg" ]; then
    commit_msg="Update: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${YELLOW}⚠️  No message provided. Using: '$commit_msg'${NC}"
fi

echo ""

# ════════════════════════════════════════════════════════════════
# Step 1: Setup Git LFS for large files
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[1/6] 📦 Setting up Git LFS for large files...${NC}"

# Check if .gitattributes exists
if [ ! -f .gitattributes ]; then
    echo -e "${YELLOW}Creating .gitattributes...${NC}"
    touch .gitattributes
fi

# Track large model files
git lfs track "*.keras" 2>/dev/null
git lfs track "*.h5" 2>/dev/null
git lfs track "*.pkl" 2>/dev/null
git lfs track "*.pb" 2>/dev/null

# Add .gitattributes
git add .gitattributes

echo -e "${GREEN}✓ Git LFS configured${NC}"
echo ""

# ════════════════════════════════════════════════════════════════
# Step 2: Stage all changes
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[2/6] 📂 Staging changes...${NC}"

git add .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Changes staged successfully${NC}"
else
    echo -e "${RED}✗ Failed to stage changes${NC}"
    exit 1
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 3: Show what will be committed
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[3/6] 👀 Files to be committed:${NC}"
git status --short
echo ""

# ════════════════════════════════════════════════════════════════
# Step 4: Commit changes
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[4/6] 💾 Committing changes...${NC}"

git commit -m "$commit_msg"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Changes committed successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Nothing to commit or commit failed${NC}"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 5: Push to GitHub
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[5/6] 🐙 Pushing to GitHub...${NC}"

# Try main branch first, then master
git push origin main 2>/dev/null || git push origin master 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pushed to GitHub! 🎉${NC}"
    GITHUB_SUCCESS=true
else
    echo -e "${RED}✗ Failed to push to GitHub${NC}"
    echo -e "${YELLOW}💡 Tip: Make sure you have set up the GitHub remote:${NC}"
    echo -e "   ${CYAN}git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git${NC}"
    GITHUB_SUCCESS=false
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Step 6: Push to Hugging Face
# ════════════════════════════════════════════════════════════════
echo -e "${BLUE}[6/6] 🤗 Pushing to Hugging Face...${NC}"

# Check if Hugging Face remote exists (either 'huggingface' or 'space')
if git remote | grep -q 'huggingface'; then
    HF_REMOTE="huggingface"
elif git remote | grep -q 'space'; then
    HF_REMOTE="space"
else
    HF_REMOTE=""
fi

if [ -n "$HF_REMOTE" ]; then
    git push $HF_REMOTE main 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully pushed to Hugging Face! 🎉${NC}"
        HF_SUCCESS=true
    else
        echo -e "${RED}✗ Failed to push to Hugging Face${NC}"
        echo -e "${YELLOW}💡 Tip: Check your credentials or remote URL${NC}"
        HF_SUCCESS=false
    fi
else
    echo -e "${YELLOW}⚠️  Hugging Face remote not configured${NC}"
    echo -e "${CYAN}To add Hugging Face remote:${NC}"
    echo -e "   ${CYAN}git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE${NC}"
    HF_SUCCESS=false
fi
echo ""

# ════════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════════
echo -e "${PURPLE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║              DEPLOYMENT SUMMARY                        ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# GitHub Status
if [ "$GITHUB_SUCCESS" = true ]; then
    echo -e "  🐙 GitHub:        ${GREEN}✓ SUCCESS${NC}"
else
    echo -e "  🐙 GitHub:        ${RED}✗ FAILED${NC}"
fi

# Hugging Face Status
if [ "$HF_SUCCESS" = true ]; then
    echo -e "  🤗 Hugging Face:  ${GREEN}✓ SUCCESS${NC}"
else
    echo -e "  🤗 Hugging Face:  ${YELLOW}⚠ NOT CONFIGURED / FAILED${NC}"
fi

echo ""

# Final message
if [ "$GITHUB_SUCCESS" = true ] && [ "$HF_SUCCESS" = true ]; then
    echo -e "${GREEN}🎊 Both deployments successful! Your app is live everywhere! 🎊${NC}"
elif [ "$GITHUB_SUCCESS" = true ]; then
    echo -e "${YELLOW}⚠️  GitHub deployment successful, but Hugging Face needs setup${NC}"
    echo -e "${CYAN}See DUAL_DEPLOYMENT_GUIDE.md for Hugging Face setup instructions${NC}"
else
    echo -e "${RED}❌ Deployments failed. Check the errors above.${NC}"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}💡 Quick Links:${NC}"
echo -e "${CYAN}   • Dual Deployment Guide: DUAL_DEPLOYMENT_GUIDE.md${NC}"
echo -e "${CYAN}   • Check remotes: git remote -v${NC}"
echo -e "${CYAN}   • Check status: git status${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
