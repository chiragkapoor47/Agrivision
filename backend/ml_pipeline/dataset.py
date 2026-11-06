"""
TAH-015: Dataset Preprocessing and Data Augmentation Pipeline
"""
import os
import torch
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, datasets
from PIL import Image

# ImageNet normalization standard
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def get_train_transforms():
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=25),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

def get_eval_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

def create_data_loaders(data_dir, batch_size=32, train_val_test_split=(0.7, 0.15, 0.15), num_workers=2):
    """
    Creates train, val, and test data loaders from a folder containing class subdirectories.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
        
    full_dataset = datasets.ImageFolder(root=data_dir, transform=get_train_transforms())
    total_len = len(full_dataset)
    
    train_len = int(train_val_test_split[0] * total_len)
    val_len = int(train_val_test_split[1] * total_len)
    test_len = total_len - train_len - val_len
    
    train_set, val_set, test_set = random_split(
        full_dataset, 
        [train_len, val_len, test_len],
        generator=torch.Generator().manual_seed(42)
    )
    
    # Validation and test datasets should use evaluation transforms (no random augmentation)
    eval_transform = get_eval_transforms()
    val_set.dataset.transform = eval_transform
    test_set.dataset.transform = eval_transform
    
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, val_loader, test_loader, full_dataset.classes
