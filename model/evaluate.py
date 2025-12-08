"""
Evaluation Module for Deepfake Detection Model
Evaluates model performance on test set and generates metrics
"""

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model, test_generator):
    """
    Evaluate the model on test set
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
        
    Returns:
        Test loss and accuracy
    """
    print("\n" + "="*50)
    print("Evaluating Model on Test Set")
    print("="*50)
    
    # Evaluate model
    test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
    
    print(f"\nTest Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("="*50 + "\n")
    
    return test_loss, test_accuracy

def generate_predictions(model, test_generator):
    """
    Generate predictions for test set
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
        
    Returns:
        Predictions and true labels
    """
    # Reset generator
    test_generator.reset()
    
    # Generate predictions
    predictions = model.predict(test_generator, verbose=1)
    
    # Get true labels
    true_labels = test_generator.classes
    
    # Convert predictions to binary (0 or 1)
    predicted_labels = (predictions > 0.5).astype(int).flatten()
    
    return predictions, predicted_labels, true_labels

def plot_confusion_matrix(true_labels, predicted_labels, class_names=['Fake', 'Real'], save_path='confusion_matrix.png'):
    """
    Plot confusion matrix
    
    Args:
        true_labels: True labels
        predicted_labels: Predicted labels
        class_names: Names of classes
        save_path: Path to save the plot
    """
    cm = confusion_matrix(true_labels, predicted_labels)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Confusion matrix saved to: {save_path}")
    plt.show()

def plot_roc_curve(true_labels, predictions, save_path='roc_curve.png'):
    """
    Plot ROC curve
    
    Args:
        true_labels: True labels
        predictions: Prediction probabilities
        save_path: Path to save the plot
    """
    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(true_labels, predictions)
    auc_score = roc_auc_score(true_labels, predictions)
    
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, linewidth=2, label=f'ROC Curve (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"ROC curve saved to: {save_path}")
    plt.show()
    
    return auc_score

def print_classification_report(true_labels, predicted_labels, class_names=['Fake', 'Real']):
    """
    Print detailed classification report
    
    Args:
        true_labels: True labels
        predicted_labels: Predicted labels
        class_names: Names of classes
    """
    print("\n" + "="*50)
    print("Classification Report")
    print("="*50)
    print(classification_report(true_labels, predicted_labels, target_names=class_names))
    print("="*50 + "\n")

def full_evaluation(model, test_generator, class_names=['Fake', 'Real']):
    """
    Perform full evaluation of the model
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
        class_names: Names of classes
    """
    # Evaluate model
    test_loss, test_accuracy = evaluate_model(model, test_generator)
    
    # Generate predictions
    predictions, predicted_labels, true_labels = generate_predictions(model, test_generator)
    
    # Print classification report
    print_classification_report(true_labels, predicted_labels, class_names)
    
    # Plot confusion matrix
    plot_confusion_matrix(true_labels, predicted_labels, class_names)
    
    # Plot ROC curve
    auc_score = plot_roc_curve(true_labels, predictions)
    
    print(f"\nFinal Results:")
    print(f"  Test Accuracy: {test_accuracy:.4f}")
    print(f"  Test Loss: {test_loss:.4f}")
    print(f"  AUC Score: {auc_score:.4f}")

if __name__ == "__main__":
    # This module is meant to be imported, not run directly
    print("This module provides evaluation utilities for the deepfake detection model.")
