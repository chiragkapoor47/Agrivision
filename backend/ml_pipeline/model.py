"""
TAH-015: Precision Agriculture and Crop Disease Predictor
Model Architecture: MobileNetV2 with Custom Agronomic Classifier Head
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
from torchvision import models

# 33 Standard Classes covering the 9 required crops + diseases + healthy classes
CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Cotton___Bacterial_blight",
    "Cotton___Leaf_spot",
    "Cotton___healthy",
    "Grape___Black_rot",
    "Grape___Esca_Black_Measles",
    "Grape___Leaf_blight",
    "Grape___healthy",
    "Pepper___Bacterial_spot",
    "Pepper___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Rice___Bacterial_leaf_blight",
    "Rice___Brown_spot",
    "Rice___Leaf_blast",
    "Rice___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___healthy",
    "Wheat___Leaf_rust",
    "Wheat___Powdery_mildew",
    "Wheat___Stripe_rust",
    "Wheat___healthy"
]

class CropDiseaseClassifier(nn.Module):
    """
    MobileNetV2 backbone for fast, low-latency edge/cloud inference with high accuracy.
    Transfer learning with frozen or fine-tuned feature extractor + custom classification head.
    """
    def __init__(self, num_classes=len(CLASS_NAMES), pretrained=True):
        super(CropDiseaseClassifier, self).__init__()
        weights = models.MobileNet_V2_Weights.DEFAULT if pretrained else None
        self.backbone = models.mobilenet_v2(weights=weights)
        
        in_features = self.backbone.classifier[1].in_features
        # Replace default classifier with enhanced regularized head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(512, num_classes)
        )
        
    def forward(self, x):
        return self.backbone(x)

def get_model(num_classes=len(CLASS_NAMES), pretrained=True):
    return CropDiseaseClassifier(num_classes=num_classes, pretrained=pretrained)
