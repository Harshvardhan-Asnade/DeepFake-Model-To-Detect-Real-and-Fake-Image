# Project Requirements

This document lists the libraries and dependencies required to run the Deepfake Detection Model and Web Application.

![Tech Stack Workflow](tech_stack_workflow.png)

## Python Dependencies

The project relies on the following Python libraries:

### Core Includes
- **Python 3.8+** (Recommended)

### Deep Learning & Data Processing
- **tensorflow**: Core deep learning framework (includes `keras`).
- **numpy**: Numerical computing and array manipulation.
- **Pillow**: Image processing (PIL).

### Model Evaluation & Visualization
- **matplotlib**: Plotting training history and metrics.
- **seaborn**: Enhanced visualization for confusion matrices.
- **scikit-learn**: Metrics calculation (classification report, confusion matrix, ROC/AUC).

### Web Application (Backend)
- **flask**: Web framework for the dashboard and API.
- **werkzeug**: Utils for Flask (usually installed with Flask).

## Installation

You can install these dependencies using pip:

```bash
pip install tensorflow numpy pillow matplotlib seaborn scikit-learn flask
```

> [!NOTE]
> For macOS with Apple Silicon (M1/M2/M3), it is recommended to use `tensorflow-metal` for GPU acceleration.

## File-Specific Imports

### `backend/app.py`
- `flask`
- `tensorflow`
- `numpy`
- `pillow`

### `model/train.py`
- `tensorflow`
- `matplotlib`

### `model/model.py`
- `tensorflow`

### `model/evaluate.py`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`
