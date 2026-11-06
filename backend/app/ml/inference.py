"""
TAH-015: AI Computer Vision Inference Engine
Performs real PyTorch MobileNetV2 classification, confidence calculation,
confidence-threshold uncertainty handling, crop override routing,
and severity integration.
"""
import os
import sys
import json
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Ensure imports resolve
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ml_pipeline.model import CropDiseaseClassifier, CLASS_NAMES
from app.ml.severity_analyzer import analyze_leaf_severity
from app.ml.knowledge_base import get_treatment_for_disease

# Inference transforms
INFERENCE_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

CONFIDENCE_THRESHOLD = 0.40 # Below this, mark as Uncertain/Unknown

class DiseaseInferenceEngine:
    _instance = None

    def __init__(self, weights_path=None):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.classes = CLASS_NAMES
        
        # Determine weights path
        if weights_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            weights_path = os.path.join(base_dir, "ml_pipeline", "model_weights", "plant_disease_mobilenetv2.pth")
            classes_path = os.path.join(base_dir, "ml_pipeline", "model_weights", "class_names.json")
            if os.path.exists(classes_path):
                try:
                    with open(classes_path, "r") as f:
                        self.classes = json.load(f)
                except Exception as e:
                    print(f"Warning loading classes: {e}")

        self.model = CropDiseaseClassifier(num_classes=len(self.classes), pretrained=False)
        
        if os.path.exists(weights_path):
            try:
                checkpoint = torch.load(weights_path, map_location=self.device)
                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    self.model.load_state_dict(checkpoint["model_state_dict"])
                else:
                    self.model.load_state_dict(checkpoint)
                print(f"[AI Model] Successfully loaded trained weights from: {weights_path}")
            except Exception as e:
                print(f"[AI Model] Warning loading weights ({e}), initializing standard MobileNetV2 backbone.")
                self.model = CropDiseaseClassifier(num_classes=len(self.classes), pretrained=True)
        else:
            print(f"[AI Model] Checkpoint {weights_path} not found. Using pretrained MobileNetV2.")
            self.model = CropDiseaseClassifier(num_classes=len(self.classes), pretrained=True)

        self.model = self.model.to(self.device)
        self.model.eval()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, image_data, crop_hint=None, state="", district="", language="en", output_upload_dir="uploads"):
        """
        Runs complete AI diagnostic pipeline on leaf image.
        image_data can be filepath (str), bytes, or PIL.Image.
        """
        # Load PIL image
        if isinstance(image_data, str):
            image = Image.open(image_data).convert("RGB")
            raw_cv_input = image_data
        elif isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            raw_cv_input = image_data
        elif isinstance(image_data, Image.Image):
            image = image_data.convert("RGB")
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            raw_cv_input = buf.getvalue()
        else:
            raise ValueError("Unsupported image data format")

        # Tensor preprocessing
        tensor = INFERENCE_TRANSFORMS(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probs = F.softmax(outputs, dim=1).squeeze(0)

        # Handle crop manual hint if provided by farmer
        valid_indices = list(range(len(self.classes)))
        if crop_hint and crop_hint.lower() not in ["", "all", "auto"]:
            hint_clean = crop_hint.strip().lower()
            filtered_indices = [
                i for i, c in enumerate(self.classes) 
                if c.split("___")[0].lower() == hint_clean or hint_clean in c.lower()
            ]
            if filtered_indices:
                valid_indices = filtered_indices

        # Sub-distribution over valid classes
        sub_probs = probs[valid_indices]
        best_sub_idx = torch.argmax(sub_probs).item()
        best_class_idx = valid_indices[best_sub_idx]
        confidence = float(probs[best_class_idx].item())
        predicted_raw_class = self.classes[best_class_idx]

        # Top 3 predictions for transparency
        top_k = min(3, len(valid_indices))
        top_vals, top_sub_inds = torch.topk(sub_probs, k=top_k)
        top_candidates = []
        for val, sub_i in zip(top_vals, top_sub_inds):
            c_idx = valid_indices[sub_i.item()]
            raw_c = self.classes[c_idx]
            parts = raw_c.split("___")
            c_crop = parts[0]
            c_dis = parts[1].replace("_", " ") if len(parts) > 1 else raw_c
            top_candidates.append({
                "crop": c_crop,
                "disease": c_dis,
                "confidence": round(float(val.item()) * 100, 1)
            })

        # Parse crop and disease names
        if "___" in predicted_raw_class:
            parts = predicted_raw_class.split("___")
            detected_crop = parts[0]
            detected_disease = parts[1].replace("_", " ")
        else:
            detected_crop = "Plant"
            detected_disease = predicted_raw_class.replace("_", " ")

        is_healthy = "healthy" in detected_disease.lower()

        # Confidence check
        is_uncertain = confidence < CONFIDENCE_THRESHOLD
        if is_uncertain:
            status_note = "Low Confidence Prediction (< 40%). Leaf symptoms may be in very early or ambiguous stage, or image may have motion blur/harsh shadows."
        else:
            status_note = "High Confidence Identification"

        # 2. Run Computer Vision Severity Segmentation
        severity_result = analyze_leaf_severity(
            image_input=raw_cv_input,
            disease_name=detected_disease,
            is_healthy=is_healthy,
            output_dir=output_upload_dir
        )

        # 3. Retrieve Agronomic Treatments from Knowledge Base
        treatment_plan = get_treatment_for_disease(
            disease_key=predicted_raw_class,
            state=state,
            district=district,
            language=language
        )

        return {
            "crop": treatment_plan["crop"],
            "disease": treatment_plan["disease"],
            "raw_class": predicted_raw_class,
            "confidence_score": round(confidence * 100, 1),
            "is_uncertain": is_uncertain,
            "confidence_status": status_note,
            "is_healthy": is_healthy,
            "top_candidates": top_candidates,
            "severity": {
                "level": severity_result["severity_level"],
                "affected_area_percentage": severity_result["affected_area_percentage"],
                "is_reliable": severity_result["is_reliable"],
                "explanation": severity_result["explanation"],
                "overlay_url": severity_result["overlay_path"],
                "lesion_count": severity_result["lesion_count"]
            },
            "pathogen": treatment_plan.get("pathogen", ""),
            "symptoms": treatment_plan["symptoms"],
            "organic_treatment": treatment_plan["organic_treatment"],
            "chemical_treatment": treatment_plan["chemical_treatment"],
            "preventive_measures": treatment_plan["preventive_measures"],
            "regional_advisory": treatment_plan["regional_advisory"],
            "disclaimer": "AI Diagnostic Notice: This analysis is computer vision-assisted for farmer decision support and should be verified with your local Krishi Vigyan Kendra (KVK) or agricultural extension specialist for commercial field decisions."
        }

# Singleton accessor
def get_inference_engine():
    return DiseaseInferenceEngine.get_instance()
