"""
TAH-015: Dataset Preprocessing and Data Augmentation Pipeline
"""
import os
import sys
import torch
from torch.utils.data import Dataset, DataLoader, Subset
from torchvision import transforms, datasets
from PIL import Image
from collections import defaultdict
import random

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ImageNet normalization standard
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def get_train_transforms():
    return transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.2),
        transforms.RandomRotation(degrees=20),
        transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

def get_eval_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD)
    ])

class CustomTransformedSubset(Dataset):
    """Applies specific transformation dynamically to a PyTorch dataset subset."""
    def __init__(self, base_dataset, indices, transform=None):
        self.base_dataset = base_dataset
        self.indices = indices
        self.transform = transform

    def __getitem__(self, idx):
        path, target = self.base_dataset.samples[self.indices[idx]]
        img = Image.open(path).convert("RGB")
        if self.transform is not None:
            img = self.transform(img)
        return img, target

    def __len__(self):
        return len(self.indices)

def create_data_loaders(data_dir, batch_size=32, train_val_test_split=(0.7, 0.15, 0.15), 
                        num_workers=0, max_samples_per_class=None):
    """
    Creates train, val, and test data loaders from a folder containing class subdirectories.
    Handles nested directory anomalies and supports stratified class-balanced sampling.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
        
    # Check if there is an inner PlantVillage folder
    inner_dir = os.path.join(data_dir, "PlantVillage")
    if os.path.exists(inner_dir) and os.path.isdir(inner_dir):
        # Check if inner_dir contains leaf class folders
        subdirs = [d for d in os.listdir(inner_dir) if os.path.isdir(os.path.join(inner_dir, d))]
        if len(subdirs) >= 10:
            data_dir = inner_dir

    raw_dataset = datasets.ImageFolder(root=data_dir)
    
    # Filter out any classes that are just nested folders (not actual leaf folders)
    valid_classes = []
    class_to_idx = {}
    valid_samples = []
    
    for path, target in raw_dataset.samples:
        class_name = raw_dataset.classes[target]
        # Ignore if class_name is 'PlantVillage'
        if class_name.lower() == "plantvillage":
            continue
        valid_samples.append((path, class_name))
        if class_name not in class_to_idx:
            class_to_idx[class_name] = len(class_to_idx)
            valid_classes.append(class_name)

    # Re-index samples
    indexed_samples = [(p, class_to_idx[c]) for p, c in valid_samples]
    
    # Group indices by class for stratified split
    class_indices = defaultdict(list)
    for idx, (path, target) in enumerate(indexed_samples):
        class_indices[target].append(idx)
        
    train_indices = []
    val_indices = []
    test_indices = []
    
    random.seed(42)
    for target, indices in class_indices.items():
        random.shuffle(indices)
        if max_samples_per_class and len(indices) > max_samples_per_class:
            indices = indices[:max_samples_per_class]
            
        n = len(indices)
        n_train = max(1, int(train_val_test_split[0] * n))
        n_val = max(1, int(train_val_test_split[1] * n))
        
        train_indices.extend(indices[:n_train])
        val_indices.extend(indices[n_train:n_train + n_val])
        test_indices.extend(indices[n_train + n_val:])

    # Reconstruct container dataset
    class ReindexedDataset:
        def __init__(self, samples, classes):
            self.samples = samples
            self.classes = classes
            
    base_ds = ReindexedDataset(indexed_samples, valid_classes)
    
    train_set = CustomTransformedSubset(base_ds, train_indices, transform=get_train_transforms())
    val_set = CustomTransformedSubset(base_ds, val_indices, transform=get_eval_transforms())
    test_set = CustomTransformedSubset(base_ds, test_indices, transform=get_eval_transforms())
    
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, val_loader, test_loader, valid_classes
