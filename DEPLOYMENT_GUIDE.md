   # Deployment Guide for Deepfake Detection App on Vercel

## Prerequisites
1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com).
2. **Node.js & npm**: Ensure you have Node.js installed to use Vercel CLI.

## Preparation (Already Done)
We have automatically prepared the following configuration files for you:
- `vercel.json`: Configure the serverless function.
- `requirements.txt`: List of Python dependencies (optimized with `tensorflow-cpu`).
- `.vercelignore`: Excludes unnecessary files (like logs and unused checkpoints) to reduce upload size.
- `app.py`: Updated to load the model correctly in a serverless environment.

## Option 1: Deploy using Vercel CLI (Recommended for quick test)

1. **Install Vercel CLI**:
   Open a terminal and run:
   ```bash
   npm install -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```
   Follow the prompts to authorize via email or GitHub.

3. **Deploy**:
   Run the following command in your project folder (`c:\Deepfake`):
   ```bash
   vercel
   ```
   - Accept the default settings (just press Enter for most questions).
   - Project Name: `deepfake-detection` (or similar)
   - In root directory: `Yes` (`./`)

   Wait for the build to complete. It will give you a **Production** URL (e.g., `https://deepfake-detection.vercel.app`).

## Option 2: Deploy via GitHub

1. Create a new repository on GitHub.
2. Push your code to the repository.
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin <YOUR_REPO_URL>
   git push -u origin main
   ```
   *Note: Ensure your single file size is under 100MB (GitHub limit) and total repo size is reasonable. We excluded `final_model.keras` so it should be fine.*
3. Go to your Vercel Dashboard -> **Add New Project**.
4. Import your GitHub repository.
5. Vercel will auto-detect the configuration from `vercel.json` and deploy.

## Troubleshooting

- **Serverless Function Size Limit**: TensorFlow is a large library. If the deployment fails due to size limits (250MB unzipped), consider:
  - Using a smaller model format (like TFLite).
  - Removing other dependencies.
- **Cold Starts**: The first request might be slow (10-15s) because it needs to load the model (~60MB) into memory. Subsequent requests will be faster.
