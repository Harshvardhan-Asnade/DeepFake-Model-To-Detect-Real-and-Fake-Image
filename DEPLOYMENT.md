# 🚀 How to Deploy DeepGuard for Free

This guide will show you how to deploy your Deepfake Detection model for free using **Hugging Face Spaces**.

## Prerequisites
- You have already pushed your code to GitHub (✅ Done!)
- A Hugging Face account ([Sign Up](https://huggingface.co/join))

## Step 1: Create a New Space
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. **Space Name**: Enter a name (e.g., `deepfake-detector`).
3. **License**: Select `MIT` or `Apache 2.0`.
4. **SDK**: Select **Docker** (Crucial!).
5. **Space Hardware**: Keep it as **CPU Basic (Free)**.
6. **Visibility**: Public.
7. Click **Create Space**.

## Step 2: Deploy from your Terminal
Since you already have your code set up locally, we just need to tell Git to send a copy to Hugging Face.

1. **Add Hugging Face as a remote** (replace `YOUR_USERNAME` and `SPACE_NAME`):
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
   ```

2. **Force Push to Deploy**:
   ```bash
   git push --force space main
   ```
   _Note: You might be asked for your Hugging Face `Username` and `Access Token` (password). You can get a token from your [Settings](https://huggingface.co/settings/tokens)._

## 🔄 How to Update
When you make changes to your code (e.g., updating the model or fixing a bug), run these commands:

1. **Save your changes**:
   ```bash
   git add .
   git commit -m "Describe your changes here"
   ```

2. **Push to GitHub** (Safe backup):
   ```bash
   git push origin main
   ```

3. **Push to Hugging Face** (Deploy update):
   ```bash
   git push space main
   ```
   _Your Space will automatically rebuild and restart with the new code!_

## Step 3: Troubleshooting
- **Build Logs**: After pushing, go to your Space URL. Click the **App** tab to see it building.
- **Port 7860**: We configured Docker to use port 7860. The logs should say `Listening on http://0.0.0.0:7860`.
- **Large Files**: If `git push` fails due to large files, ensure you ran `git lfs install` (which you have!).

## 🏁 Success!
Your app will be live at `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`.
