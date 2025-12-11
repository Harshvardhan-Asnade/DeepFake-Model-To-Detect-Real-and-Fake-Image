# 🚀 How to Deploy DeepGuard for Free

This guide will show you how to deploy your Deepfake Detection model for free using **Hugging Face Spaces**.

## Prerequisites
- A GitHub account (optional, but recommended)
- The code on your local machine

## Step 1: Create a Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co/)
2. Click **Sign Up** and create a free account.

## Step 2: Create a New Space
1. Click on your profile picture in the top right and select **New Space**.
2. **Space Name**: Enter a name (e.g., `deepfake-detector`).
3. **License**: Select `MIT` or `Apache 2.0`.
4. **SDK**: Select **Docker** (This is important! Do not select Streamlit or Gradio).
5. **Space Hardware**: Keep it as **CPU Basic (Free)**.
6. **Visibility**: Public.
7. Click **Create Space**.

## Step 3: Upload Your Code
You can upload your code in two ways. The easiest way for beginners is using the web interface or Git from your terminal.

### Option A: Using the Web Interface (Easiest)
1. On your new Space page, click the **Files** tab.
2. Click **Add file** -> **Upload files**.
3. Drag and drop **ALL** the files and folders from your project folder into the browser.
   - Make sure you include: `backend/`, `frontend/`, `model/`, `Dockerfile`, `requirements.txt`.
   - **Note**: You might need to upload the `model/checkpoints/final_model_pro.keras` file separately if it's very large, or use Git LFS (Option B).
4. Click **Commit changes to main**.
5. Hugging Face will automatically start building your app. Click the **App** tab to see the build logs.

### Option B: Using Git (Recommended)
If you have `git` installed:

1. Clone your Space locally (replace `YOUR_USERNAME` and `SPACE_NAME`):
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
   ```
2. Copy all your project files into this new folder.
3. Install Git LFS (for large model files):
   ```bash
   git lfs install
   git lfs track "*.keras"
   ```
4. Push to Hugging Face:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

## Step 4: Troubleshooting
- **Build Errors**: Check the **Logs** tab in your Space.
- **Port Issues**: We configured the `Dockerfile` to expose port `7860`, which is what Hugging Face expects.
- **Model Loading**: Ensure your `final_model_pro.keras` was uploaded correctly. If it's missing, the app will warn you in the logs.

## 🏁 Success!
Once the build finishes (it may take a few minutes), your app will be live at `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`. You can share this link with anyone!
