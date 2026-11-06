"""
TAH-015: Model Training Script for Crop Disease Prediction
Trains MobileNetV2 with transfer learning on agricultural leaf datasets (e.g. PlantVillage).
"""
import os
import sys
import argparse
import time
import copy
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ml_pipeline.model import CropDiseaseClassifier, CLASS_NAMES
from ml_pipeline.dataset import create_data_loaders

def train_model(data_dir, output_model_path="model_weights/plant_disease_mobilenetv2.pth", 
                epochs=15, batch_size=32, lr=1e-4, device=None):
    if device is None:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    print(f"Loading dataset from: {data_dir}")
    train_loader, val_loader, test_loader, classes = create_data_loaders(data_dir, batch_size=batch_size)
    print(f"Classes ({len(classes)}): {classes}")
    
    # Save class mapping
    class_map_path = os.path.join(os.path.dirname(output_model_path), "class_names.json")
    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    with open(class_map_path, "w") as f:
        json.dump(classes, f, indent=2)
    print(f"Class names saved to {class_map_path}")
    
    model = CropDiseaseClassifier(num_classes=len(classes), pretrained=True)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-3)
    scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)
    
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    
    start_time = time.time()
    for epoch in range(epochs):
        print(f"\n--- Epoch {epoch+1}/{epochs} ---")
        
        # Training Phase
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_samples += inputs.size(0)
            
        scheduler.step()
        
        epoch_loss = running_loss / total_samples
        epoch_acc = (running_corrects.double() / total_samples).item()
        history["train_loss"].append(epoch_loss)
        history["train_acc"].append(epoch_acc)
        print(f"Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc * 100:.2f}%")
        
        # Validation Phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        val_total = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                val_total += inputs.size(0)
                
        val_epoch_loss = val_loss / val_total
        val_epoch_acc = (val_corrects.double() / val_total).item()
        history["val_loss"].append(val_epoch_loss)
        history["val_acc"].append(val_epoch_acc)
        print(f"Val Loss:   {val_epoch_loss:.4f} | Val Acc:   {val_epoch_acc * 100:.2f}%")
        
        # Track best model
        if val_epoch_acc > best_acc:
            best_acc = val_epoch_acc
            best_model_wts = copy.deepcopy(model.state_dict())
            torch.save({
                "epoch": epoch,
                "model_state_dict": best_model_wts,
                "val_acc": best_acc,
                "classes": classes
            }, output_model_path)
            print(f"[*] New best model saved to {output_model_path} (Val Acc: {best_acc*100:.2f}%)")
            
    time_elapsed = time.time() - start_time
    print(f"\nTraining complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
    print(f"Best Val Accuracy: {best_acc * 100:.2f}%")
    
    # Save training history
    history_path = os.path.join(os.path.dirname(output_model_path), "training_history.json")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)
        
    return output_model_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train MobileNetV2 for Plant Disease Detection")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to PlantVillage dataset root directory")
    parser.add_argument("--epochs", type=int, default=15, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--lr", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--output", type=str, default="model_weights/plant_disease_mobilenetv2.pth", help="Output model path")
    args = parser.parse_args()
    
    train_model(
        data_dir=args.data_dir,
        output_model_path=args.output,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr
    )
