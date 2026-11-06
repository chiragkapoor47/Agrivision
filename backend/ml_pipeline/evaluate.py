"""
TAH-015: Model Evaluation, Confusion Matrix & Performance Metrics
"""
import os
import sys
import json
import argparse
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ml_pipeline.model import CropDiseaseClassifier, CLASS_NAMES
from ml_pipeline.dataset import create_data_loaders

def plot_training_curves(history_path, output_dir="model_weights"):
    if not os.path.exists(history_path):
        print(f"History file {history_path} does not exist.")
        return
        
    with open(history_path, "r") as f:
        history = json.load(f)
        
    epochs = range(1, len(history["train_loss"]) + 1)
    
    plt.figure(figsize=(12, 5))
    
    # Loss plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history["train_loss"], 'b-o', label='Train Loss')
    plt.plot(epochs, history["val_loss"], 'r-s', label='Val Loss')
    plt.title('Training & Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Accuracy plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs, [a * 100 for a in history["train_acc"]], 'b-o', label='Train Acc')
    plt.plot(epochs, [a * 100 for a in history["val_acc"]], 'r-s', label='Val Acc')
    plt.title('Training & Validation Accuracy (%)')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    curve_path = os.path.join(output_dir, "accuracy_loss_curves.png")
    plt.tight_layout()
    plt.savefig(curve_path, dpi=300)
    plt.close()
    print(f"Accuracy/Loss curves saved to: {curve_path}")

def evaluate_model(model_path, data_dir, output_dir="model_weights", batch_size=32):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Evaluating model on: {device}")
    
    _, _, test_loader, classes = create_data_loaders(data_dir, batch_size=batch_size)
    
    checkpoint = torch.load(model_path, map_location=device)
    model = CropDiseaseClassifier(num_classes=len(classes), pretrained=False)
    if "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)
    model = model.to(device)
    model.eval()
    
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    # Metrics
    report = classification_report(all_labels, all_preds, target_names=classes, output_dict=True)
    report_text = classification_report(all_labels, all_preds, target_names=classes)
    print("\n--- Test Set Classification Report ---\n")
    print(report_text)
    
    metrics_path = os.path.join(output_dir, "evaluation_report.json")
    with open(metrics_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Metrics saved to {metrics_path}")
    
    # Confusion Matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(14, 12))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    plt.title('TAH-015 Crop Disease Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90, fontsize=8)
    plt.yticks(tick_marks, classes, fontsize=8)
    plt.ylabel('Ground Truth')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Crop Disease Detection Model")
    parser.add_argument("--model", type=str, default="model_weights/plant_disease_mobilenetv2.pth")
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="model_weights")
    args = parser.parse_args()
    
    evaluate_model(args.model, args.data_dir, args.output_dir)
