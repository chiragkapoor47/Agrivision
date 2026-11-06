"""
TAH-015: Model Training & Fine-Tuning Script for Crop Disease Prediction
Trains MobileNetV2 using two-stage transfer learning (Head Warmup + Feature Fine-Tuning)
on the PlantVillage agricultural leaf dataset.
"""
import os
import sys

# Ensure UTF-8 console output and OpenMP fix on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
import time
import copy
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_pipeline.model import CropDiseaseClassifier
from ml_pipeline.dataset import create_data_loaders
from ml_pipeline.evaluate import evaluate_model, plot_training_curves

def train_and_finetune(
    data_dir, 
    output_model_path="ml_pipeline/model_weights/plant_disease_mobilenetv2.pth", 
    warmup_epochs=3,
    finetune_epochs=4,
    batch_size=32, 
    max_samples_per_class=50,
    device=None
):
    if device is None:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"==================================================")
    print(f"🌾 AgriVision AI Model Training & Fine-Tuning Pipeline")
    print(f"==================================================")
    print(f"Hardware Compute Device : {device}")
    print(f"Dataset Root Directory  : {data_dir}")
    print(f"Output Checkpoint Path  : {output_model_path}")
    print(f"Max Samples per Class   : {max_samples_per_class if max_samples_per_class else 'Full Dataset'}")
    print(f"Warmup / Finetune Epochs: {warmup_epochs} / {finetune_epochs}")
    print(f"==================================================")
    
    # 1. Load Data
    print(f"\n[1/4] Preparing stratified train/val/test data loaders...")
    train_loader, val_loader, test_loader, classes = create_data_loaders(
        data_dir, 
        batch_size=batch_size, 
        max_samples_per_class=max_samples_per_class,
        num_workers=0
    )
    print(f"[+] Loaded {len(classes)} classes across {len(train_loader.dataset)} training, {len(val_loader.dataset)} validation, and {len(test_loader.dataset)} testing images.")
    for idx, c in enumerate(classes):
        print(f"    {idx+1}. {c}")
        
    output_dir = os.path.dirname(os.path.abspath(output_model_path))
    os.makedirs(output_dir, exist_ok=True)
    
    # Save class mapping
    class_map_path = os.path.join(output_dir, "class_names.json")
    with open(class_map_path, "w") as f:
        json.dump(classes, f, indent=2)
    print(f"[+] Saved class mapping to {class_map_path}")
    
    # 2. Initialize Model
    print(f"\n[2/4] Initializing MobileNetV2 with custom agronomic classifier head...")
    model = CropDiseaseClassifier(num_classes=len(classes), pretrained=True)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss(label_smoothing=0.08)
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    
    total_epochs = warmup_epochs + finetune_epochs
    start_time = time.time()
    
    # -------------------------------------------------------------------------
    # STAGE 1: Classifier Head Warmup (Backbone Frozen)
    # -------------------------------------------------------------------------
    print(f"\n>>> STAGE 1: Head Warmup ({warmup_epochs} epochs, Backbone Frozen) <<<")
    for param in model.backbone.features.parameters():
        param.requires_grad = False
    for param in model.backbone.classifier.parameters():
        param.requires_grad = True
        
    optimizer = optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3, weight_decay=1e-4)
    
    for epoch in range(warmup_epochs):
        epoch_idx = epoch + 1
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_samples += inputs.size(0)
            
        epoch_loss = running_loss / total_samples
        epoch_acc = (running_corrects.double() / total_samples).item()
        
        # Validation
        model.eval()
        val_loss, val_corrects, val_total = 0.0, 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                _, preds = torch.max(outputs, 1)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                val_total += inputs.size(0)
                
        val_epoch_loss = val_loss / val_total
        val_epoch_acc = (val_corrects.double() / val_total).item()
        
        history["train_loss"].append(round(epoch_loss, 4))
        history["train_acc"].append(round(epoch_acc, 4))
        history["val_loss"].append(round(val_epoch_loss, 4))
        history["val_acc"].append(round(val_epoch_acc, 4))
        
        print(f"Epoch {epoch_idx:2d}/{total_epochs} [Warmup]   - Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc*100:.1f}% | Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc*100:.1f}%")
        
        if val_epoch_acc > best_acc:
            best_acc = val_epoch_acc
            best_model_wts = copy.deepcopy(model.state_dict())

    # -------------------------------------------------------------------------
    # STAGE 2: End-to-End Fine-Tuning (Top Inverted Residual Blocks Unfrozen)
    # -------------------------------------------------------------------------
    print(f"\n>>> STAGE 2: Deep Fine-Tuning ({finetune_epochs} epochs, Top Feature Layers Unfrozen) <<<")
    # Unfreeze top feature layers (layers 14 to 18 of MobileNetV2)
    for i, layer in enumerate(model.backbone.features):
        if i >= 14:
            for param in layer.parameters():
                param.requires_grad = True
                
    finetune_optimizer = optim.AdamW([
        {'params': model.backbone.features[14:].parameters(), 'lr': 2e-5},
        {'params': model.backbone.classifier.parameters(), 'lr': 1e-4}
    ], weight_decay=1e-3)
    
    scheduler = lr_scheduler.CosineAnnealingLR(finetune_optimizer, T_max=finetune_epochs, eta_min=1e-6)
    
    for epoch in range(finetune_epochs):
        epoch_idx = warmup_epochs + epoch + 1
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total_samples = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            finetune_optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            finetune_optimizer.step()
            
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_samples += inputs.size(0)
            
        scheduler.step()
        epoch_loss = running_loss / total_samples
        epoch_acc = (running_corrects.double() / total_samples).item()
        
        # Validation
        model.eval()
        val_loss, val_corrects, val_total = 0.0, 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                _, preds = torch.max(outputs, 1)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                val_total += inputs.size(0)
                
        val_epoch_loss = val_loss / val_total
        val_epoch_acc = (val_corrects.double() / val_total).item()
        
        history["train_loss"].append(round(epoch_loss, 4))
        history["train_acc"].append(round(epoch_acc, 4))
        history["val_loss"].append(round(val_epoch_loss, 4))
        history["val_acc"].append(round(val_epoch_acc, 4))
        
        print(f"Epoch {epoch_idx:2d}/{total_epochs} [FineTune] - Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc*100:.1f}% | Val Loss: {val_epoch_loss:.4f} | Val Acc: {val_epoch_acc*100:.1f}%")
        
        if val_epoch_acc > best_acc:
            best_acc = val_epoch_acc
            best_model_wts = copy.deepcopy(model.state_dict())

    # 3. Save Best Model Checkpoint
    elapsed = time.time() - start_time
    print(f"\n[3/4] Training and Fine-Tuning complete in {elapsed // 60:.0f}m {elapsed % 60:.0f}s")
    print(f"[+] Highest Validation Accuracy Achieved: {best_acc*100:.2f}%")
    
    torch.save({
        "model_state_dict": best_model_wts,
        "val_acc": best_acc,
        "classes": classes,
        "architecture": "MobileNetV2"
    }, output_model_path)
    print(f"[+] Best fine-tuned weights saved to: {output_model_path}")
    
    history_path = os.path.join(output_dir, "training_history.json")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"[+] Training history saved to: {history_path}")
    
    # 4. Generate Evaluation Metrics, Confusion Matrix, and Loss Curves
    print(f"\n[4/4] Generating evaluation reports and plots...")
    try:
        plot_training_curves(history_path, output_dir=output_dir)
        evaluate_model(output_model_path, data_dir, output_dir=output_dir, batch_size=batch_size)
    except Exception as e:
        print(f"Evaluation visualization notice: {e}")
        
    print(f"\n==================================================")
    print(f"✅ Model training, fine-tuning, and evaluation complete!")
    print(f"==================================================")
    return output_model_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and Fine-Tune MobileNetV2 for Crop Disease Prediction")
    parser.add_argument("--data_dir", type=str, default="backend/dataset/plantvillage", help="Path to dataset")
    parser.add_argument("--warmup_epochs", type=int, default=3, help="Warmup epochs for classifier head")
    parser.add_argument("--finetune_epochs", type=int, default=3, help="Fine-tuning epochs for top layers")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--max_samples_per_class", type=int, default=50, help="Max samples per class for efficient fine-tuning")
    parser.add_argument("--output", type=str, default="ml_pipeline/model_weights/plant_disease_mobilenetv2.pth", help="Output model path")
    args = parser.parse_args()
    
    train_and_finetune(
        data_dir=args.data_dir,
        output_model_path=args.output,
        warmup_epochs=args.warmup_epochs,
        finetune_epochs=args.finetune_epochs,
        batch_size=args.batch_size,
        max_samples_per_class=args.max_samples_per_class
    )
