"""
AgriVision (TAH-015): Kaggle Dataset Downloader & Preparer
Downloads datasets directly using kagglehub (works with or without login for public datasets).
"""
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import shutil
import argparse
import re
from pathlib import Path

# Allow OpenMP duplicate runtimes on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def parse_dataset_handle(input_str: str) -> str:
    """
    Extracts the 'username/dataset-slug' handle from raw strings or full Kaggle URLs.
    Example: https://www.kaggle.com/datasets/emmarex/plantdisease -> emmarex/plantdisease
    """
    input_str = input_str.strip()
    match = re.search(r"kaggle\.com/datasets/([^/?#]+)/([^/?#]+)", input_str)
    if match:
        return f"{match.group(1)}/{match.group(2)}"
    return input_str

def main():
    parser = argparse.ArgumentParser(description="Download and prepare PlantVillage/Crop disease dataset from Kaggle")
    parser.add_argument(
        "--dataset", 
        type=str, 
        default="emmarex/plantdisease",
        help="Kaggle dataset handle or URL (e.g. 'emmarex/plantdisease', 'vipoooool/new-plant-diseases-dataset', or user custom handle)"
    )
    parser.add_argument(
        "--dest", 
        type=str, 
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset"),
        help="Destination directory to copy or link dataset files"
    )
    args = parser.parse_args()

    handle = parse_dataset_handle(args.dataset)
    print("==================================================")
    print("[*] AgriVision Dataset Downloader (KaggleHub)")
    print("==================================================")
    print(f"Target Kaggle Dataset: {handle}")
    print(f"Destination Target   : {args.dest}")
    print("Downloading from Kaggle... (this might take a few moments depending on size)")

    try:
        import kagglehub
        path = kagglehub.dataset_download(handle)
        print(f"\n[+] Successfully downloaded to Kaggle cache: {path}")
        
        # Inspect contents
        items = os.listdir(path)
        print(f"    Contents found ({len(items)} items): {items[:8]}")
        
        # Check if destination exists
        dest_path = Path(args.dest)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        # Scan for image directories
        image_exts = {".jpg", ".jpeg", ".png", ".bmp"}
        class_dirs = []
        for root, dirs, files in os.walk(path):
            img_files = [f for f in files if Path(f).suffix.lower() in image_exts]
            if len(img_files) > 10:
                class_dirs.append((root, os.path.basename(root), len(img_files)))
        
        print(f"\n[+] Found {len(class_dirs)} disease class directories in downloaded dataset.")
        if class_dirs:
            for _, name, count in class_dirs[:5]:
                print(f"    - {name}: {count} leaf images")
            if len(class_dirs) > 5:
                print(f"    - ... and {len(class_dirs) - 5} more classes.")

        print(f"\n[+] Dataset is ready at: {path}")
        print("    To train the MobileNetV2 model using this dataset, run:")
        print(f'    python backend/ml_pipeline/train.py --data_dir "{path}" --epochs 10')
        print("==================================================")
        return path

    except Exception as e:
        print(f"\n[-] Download failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. If this is a private dataset on your Kaggle account, make sure you placed your kaggle.json in ~/.kaggle/kaggle.json")
        print("   or set environment variables KAGGLE_USERNAME and KAGGLE_KEY.")
        print("2. If the handle was different, supply --dataset <username>/<dataset_name>.")
        sys.exit(1)

if __name__ == "__main__":
    main()
