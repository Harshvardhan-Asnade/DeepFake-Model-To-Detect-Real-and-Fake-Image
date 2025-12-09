# Technologies & Terminologies

This document provides a detailed overview of the technical stack and key concepts used in the Deepfake Detection System.

## 🛠 Technology Stack

### Core AI & Machine Learning
*   **Python 3.x**: The primary programming language used for all model training and backend logic.
*   **TensorFlow & Keras**: The deep learning framework used to build, train, and deploy the neural networks.
    *   *Usage*: Model construction, training loops, data preprocessing.
*   **EfficientNetB0**: A state-of-the-art Convolutional Neural Network (CNN) architecture developed by Google.
    *   *Why use it?*: It captures complex image features (textures, artifacts) with high efficiency and accuracy.
*   **MobileNetV2 (Legacy)**: A lightweight CNN used in earlier versions of this project for faster (but less accurate) training.
*   **NumPy**: Fundamental package for scientific computing, used for matrix operations and image array manipulation.

### Backend Infrastructure
*   **Flask**: A lightweight WSGI web application framework for Python.
    *   *Role*: Serves the web interface and exposes the prediction API (`/api/predict`).
*   **Pillow (PIL)**: Python Imaging Library.
    *   *Role*: Handles image opening, resizing, and conversion before passing data to the AI model.

### Frontend Interface
*   **HTML5**: Structure of the web application.
*   **CSS3 (Vanilla)**: Styling with modern features like Flexbox, Grid, and CSS Variables for Dark Mode.
*   **JavaScript (ES6+)**: Handles user interactions (drag & drop), API calls, and dynamic DOM updates.

---

## 📚 Key Concepts & Terminology

### 1. Deep Learning Concepts

#### **Deepfake**
Synthetic media in which a person in an existing image or video is replaced with someone else's likeness using artificial neural networks. This project focuses on detecting these AI-generated modifications.

#### **Convolutional Neural Network (CNN)**
A class of deep neural networks, most commonly applied to analyzing visual imagery. They are designed to automatically and adaptively learn spatial hierarchies of features (edges -> shapes -> complex objects).

#### **Transfer Learning**
A technique where a model developed for a task is reused as the starting point for a model on a second task.
*   *In this project*: We use an EfficientNetB0 model pre-trained on **ImageNet** (14 million images). It already knows how to "see" edges and textures, saving us weeks of training time.

#### **Fine-Tuning**
A process that takes a model that has already been trained for a given task (Transfer Learning) and tunes it to make it perform a second similar task.
*   *Phase 1*: We freeze the pre-trained "base" and only train our custom "head".
*   *Phase 2*: We unfreeze deep layers of the base and train them with a very low learning rate to adapt to specific deepfake artifacts.

### 2. Training Metrics

#### **Epoch**
One complete pass of the entire training dataset through the machine learning algorithm.
*   *Example*: 10 Epochs means the model saw every image in the dataset 10 times.

#### **Batch Size**
The number of training examples utilized in one iteration.
*   *Example*: Batch size of 32 means the model updates its operational weights after every 32 images.

#### **Accuracy vs. Loss**
*   **Accuracy**: The percentage of correct predictions (e.g., 91.6%). Higher is better.
*   **Loss**: A summation of the errors made for each example in training or validation sets. Lower is better.

#### **Overfitting**
A modeling error where a function is too closely fit to a limited set of data points. It performs well on training data but poorly on unseen (test) data. We prevent this using **Dropout** layers and **Data Augmentation**.

### 3. Model Architecture Terms

#### **Dense Layer (Fully Connected)**
A layer where each input node is connected to each output node. It is used in the final stages of the model to make the actual classification decision.

#### **Dropout**
A regularization technique where randomly selected neurons are ignored during training. This prevents the model from relying too heavily on specific neurons, forcing it to learn more robust features.

#### **Sigmoid Activation**
A mathematical function that maps any input value to a value between 0 and 1.
*   *Usage*: The final output layer. Close to 0 means "Fake", close to 1 means "Real".
