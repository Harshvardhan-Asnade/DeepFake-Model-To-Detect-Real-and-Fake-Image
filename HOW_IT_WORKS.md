# Deepfake Detection System: How It Works

This document provides a detailed technical explanation of the Deepfake Detection System, breaking down both the AI components ("The Brain") and the Web Application ("The Body").

---

## 1. System Overview

The system is designed to classify facial images as either **"Real"** or **"Fake"** (Deepfake) with high accuracy (~91.6%). It uses a **Hybrid Architecture** combining a state-of-the-art pre-trained Convolutional Neural Network (EfficientNetB0) with a custom-built classification head.

The solution consists of three main parts:
1.  **The AI Model**: A deep learning model trained to spot artifacts in fake images.
2.  **The Backend API**: A Flask-based server that hosts the model and processes requests.
3.  **The Frontend UI**: A modern web interface for users to interact with the system.

---

## 2. The AI Model ("The Brain")

The core of the system is the deep learning model located in `model/model.py`.

### A. Architecture: Transfer Learning with EfficientNetB0

We use **Transfer Learning**, a technique where we take a model trained on a massive dataset (ImageNet, with 14 million images) and adapt it for our specific task.

*   **Base Model (Feature Extractor)**: `EfficientNetB0`
    *   **Why EfficientNet?** It balances high accuracy with computational efficiency (speed). It uses "compound scaling" to optimize depth, width, and resolution.
    *   **Input**: Images resized to `150x150` pixels with 3 color channels (RGB).
    *   **Role**: It acts as a powerful eye, extracting complex features (edges, textures, facial structures) from the image.

*   **Custom Classification Head**:
    *   **GlobalAveragePooling2D**: Condenses the complex feature maps from EfficientNet into a single 1D vector.
    *   **Dense Layer (512 Units, ReLU)**: A large fully connected layer to learn patterns from the extracted features.
    *   **BatchNormalization**: Stabilizes the learning process, making the model faster and more reliable.
    *   **Dropout (0.5)**: Randomly "turns off" 50% of neurons during training. This forces the model to learn robust features and prevents "overfitting" (memorizing the training data).
    *   **Output Layer (1 Unit, Sigmoid)**: A single neuron that outputs a probability between 0 and 1.
        *   `0.0` to `0.5` → **Fake**
        *   `0.51` to `1.0` → **Real**

### B. Data Preparation (`model/data_preparation.py`)

Before the model sees an image, the data undergoes rigorous preparation:

1.  **Resizing**: All images are standardized to `150x150` pixels.
2.  **Preprocessing**: Pixel values are scaled to the range expected by EfficientNet (roughly -1 to 1).
3.  **Data Augmentation (Training Only)**: To make the model "smarter", we artificially expand the dataset by creating variations of training images:
    *   Rotation (±20°)
    *   Shifting (Width/Height)
    *   Shearing & Zooming
    *   Horizontal Flips
    *   Brightness adjustments

**Why Augmentation?** It ensures the model recognizes a fake face even if it's tilted, zoomed in, or has different lighting.

---

## 3. The Website ("The Body")

The website allows users to easily use the complex model. It is split into the Backend (Server) and Frontend (Client).

### A. Backend API (`backend/app.py`)

The backend is built with **Flask**, a lightweight Python web framework.

*   **Model Loading**: When the server starts, it loads the trained weights (`final_model_pro.keras`) into memory.
*   **The Prediction Pipeline (`predict_image` function)**:
    1.  **Receive**: Takes a raw image from the user.
    2.  **Resize**: Forces the image to `150x150` pixels.
    3.  **Preprocess**: Applies the same mathematical scaling used during training (`tf.keras.applications.efficientnet.preprocess_input`).
    4.  **Inference**: Passes the processed matrix through the Neural Network.
    5.  **Interpret**:
        *   Output > 0.5: Return **"Real"** (with confidence score).
        *   Output ≤ 0.5: Return **"Fake"** (with confidence score).
*   **API Endpoint**: `/api/predict` accepts POST requests with an image file and returns specific JSON data.

### B. Frontend UI (`frontend/`)

The user interface uses **HTML5, CSS3, and Vanilla JavaScript**.

*   **Design**: A dark-mode, responsive design with "Glassmorphism" effects.
*   **JavaScript Logic (`script.js`)**:
    *   Handles Drag & Drop events.
    *   Previews the image locally in the browser.
    *   Sends the image to the backend using the `fetch` API.
    *   Dynamically updates the DOM (HTML) to show results without reloading the page.
    *   Polls `/api/model-status` to ensure the backend is ready before allowing uploads.

---

## 4. The Complete Workflow: Trace of an Image

Here is what happens precisely when a user checks an image:

1.  **User Action**: User drops `photo.jpg` onto the web page.
2.  **Frontend**:
    *   JavaScript catches the file.
    *   Shows a preview instantly to the user.
    *   Wraps the file in a `FormData` object.
    *   Sends a `POST` request to `http://localhost:5001/api/predict`.
3.  **Backend Processing**:
    *   Flask receives the request.
    *   Saves `photo.jpg` to a temporary folder.
    *   Opens the image using the `PIL` (Pillow) library.
    *   **Transformation**: Image is resized (150x150) -> Converted to Array -> Batched -> Preprocessed.
    *   **Inference**: The EfficientNetB0 model analyzes the array. It outputs a number, e.g., `0.02`.
    *   **Logic**: `0.02` is < `0.5`, so it classifies as **FAKE**. Confidence is `(1 - 0.02) = 98%`.
4.  **Response**: Backend sends JSON: `{"class": "Fake", "confidence": 98.0}`.
5.  **Display**:
    *   Frontend receives the JSON.
    *   Hides the loading spinner.
    *   Updates the result card to show "Fake" in Red with a 98% progress bar.

---

## 5. Technical Stack Summary

*   **Language**: Python 3.x
*   **Deep Learning**: TensorFlow / Keras
*   **Model Base**: EfficientNetB0
*   **Server**: Flask
*   **Image Processing**: Pillow (PIL)
*   **Frontend**: HTML, CSS, JavaScript (Vanilla)
