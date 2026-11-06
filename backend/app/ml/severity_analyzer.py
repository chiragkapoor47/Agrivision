"""
TAH-015: Computer Vision Disease Severity Assessment & Leaf Segmentation Engine
Uses OpenCV HSV/LAB color space thresholding, contour detection, and morphological ops
to accurately calculate affected leaf area percentage and generate diagnostic overlays.
"""
import os
import uuid
import cv2
import numpy as np

def analyze_leaf_severity(image_input, disease_name: str, is_healthy: bool = False, output_dir: str = "uploads"):
    """
    Analyzes leaf image to compute:
    1. Total leaf surface area
    2. Lesion / affected surface area
    3. Severity level (Low: <20%, Moderate: 20-50%, Severe: >50%)
    4. Annotated visual mask overlay showing infected zones in red/amber
    """
    os.makedirs(output_dir, exist_ok=True)
    overlay_filename = f"overlay_{uuid.uuid4().hex[:12]}.jpg"
    overlay_path = os.path.join(output_dir, overlay_filename)

    # Load image from file path or bytes/numpy array
    if isinstance(image_input, str):
        img = cv2.imread(image_input)
        if img is None:
            raise ValueError(f"Could not read image from {image_input}")
    elif isinstance(image_input, bytes):
        nparr = np.frombuffer(image_input, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(image_input, np.ndarray):
        img = image_input.copy()
    else:
        raise ValueError("Unsupported image input format")

    h, w, _ = img.shape
    total_image_pixels = h * w

    # If the leaf is classified as Healthy
    if is_healthy or "healthy" in disease_name.lower():
        # Generate clean overlay with green border highlighting healthy tissue
        annotated = img.copy()
        # Find leaf contours
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Broad leaf mask
        leaf_mask = cv2.inRange(hsv, np.array([20, 25, 25]), np.array([105, 255, 255]))
        contours, _ = cv2.findContours(leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cv2.drawContours(annotated, contours, -1, (46, 184, 46), 3) # Green contour
            
        cv2.imwrite(overlay_path, annotated)
        return {
            "affected_area_percentage": 0.0,
            "severity_level": "None / Healthy",
            "is_reliable": True,
            "explanation": "No active lesions or fungal necrotic spots detected. Leaf tissue exhibits healthy chlorophyll pigmentation.",
            "overlay_filename": overlay_filename,
            "overlay_path": f"/uploads/{overlay_filename}",
            "lesion_count": 0,
            "leaf_pixel_count": int(np.sum(leaf_mask > 0))
        }

    # Diseased leaf analysis:
    # 1. Segment Total Leaf Lamina
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Combined green + chlorotic + senescent leaf mask
    # Lower green: [22, 25, 25], Upper green: [100, 255, 255]
    green_mask = cv2.inRange(hsv, np.array([20, 20, 20]), np.array([102, 255, 255]))
    # Necrotic / brown leaf parts in leaf interior: [5, 30, 20] to [22, 255, 240]
    brown_mask = cv2.inRange(hsv, np.array([5, 25, 20]), np.array([22, 255, 240]))
    
    initial_leaf_mask = cv2.bitwise_or(green_mask, brown_mask)
    
    # Morphological closing to bridge small gaps and create solid leaf body
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    leaf_closed = cv2.morphologyEx(initial_leaf_mask, cv2.MORPH_CLOSE, kernel_large)
    
    # Filter external contours to identify the leaf body
    contours, _ = cv2.findContours(leaf_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid_leaf_mask = np.zeros((h, w), dtype=np.uint8)
    
    min_leaf_area = total_image_pixels * 0.04 # At least 4% of frame
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_leaf_area]
    
    if not valid_contours:
        # Fallback to general threshold if background is unusual
        solid_leaf_mask = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 240, 255, cv2.THRESH_BINARY_INV)[1]
    else:
        cv2.drawContours(solid_leaf_mask, valid_contours, -1, 255, thickness=cv2.FILLED)

    total_leaf_pixels = int(np.sum(solid_leaf_mask > 0))

    if total_leaf_pixels < 2500:
        # Insufficient leaf pixels for reliable segmentation
        cv2.imwrite(overlay_path, img)
        return {
            "affected_area_percentage": 0.0,
            "severity_level": "Uncertain",
            "is_reliable": False,
            "explanation": "Insufficient leaf surface detected in camera frame to compute mathematically reliable severity. Please position the camera closer to the leaf blade.",
            "overlay_filename": overlay_filename,
            "overlay_path": f"/uploads/{overlay_filename}",
            "lesion_count": 0,
            "leaf_pixel_count": total_leaf_pixels
        }

    # 2. Segment Lesions within the Solid Leaf Mask
    # Lesion symptoms:
    # A. Necrotic spots / blight / rust: dark brown, reddish brown, black
    # B. Chlorotic halos: bright yellow
    # C. Powdery mildew: dull whitish patches
    
    is_powdery = "powdery" in disease_name.lower() or "mold" in disease_name.lower()
    
    if is_powdery:
        # High value, low saturation inside leaf
        powdery_mask = cv2.inRange(hsv, np.array([20, 0, 150]), np.array([110, 75, 255]))
        raw_lesion = powdery_mask
    else:
        # Necrotic brown/black lesions:
        # Brown/rust hue: [5, 30, 20] to [22, 255, 210]
        necrotic_hsv = cv2.inRange(hsv, np.array([5, 30, 15]), np.array([24, 255, 220]))
        # Dark black rot / late blight necrosis (low value in HSV)
        dark_necrosis = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 75]))
        # Yellow chlorosis halo: [22, 90, 90] to [35, 255, 255]
        yellow_halo = cv2.inRange(hsv, np.array([22, 90, 80]), np.array([35, 255, 255]))
        
        raw_lesion = cv2.bitwise_or(necrotic_hsv, dark_necrosis)
        raw_lesion = cv2.bitwise_or(raw_lesion, yellow_halo)

    # Strictly constrain lesions to the internal leaf mask
    lesion_in_leaf = cv2.bitwise_and(raw_lesion, raw_lesion, mask=solid_leaf_mask)
    
    # Remove single-pixel noise with opening
    cleaned_lesion = cv2.morphologyEx(lesion_in_leaf, cv2.MORPH_OPEN, kernel_small)
    
    lesion_pixels = int(np.sum(cleaned_lesion > 0))
    affected_percentage = round((lesion_pixels / max(total_leaf_pixels, 1)) * 100.0, 1)
    
    # Bound percentage to realistic max 100%
    affected_percentage = min(100.0, max(0.0, affected_percentage))
    
    # Severity classification according to spec:
    # Low: < 20%
    # Moderate: 20–50%
    # Severe: > 50%
    if affected_percentage < 20.0:
        severity_level = "Low"
        explanation = f"Localized minor infection ({affected_percentage}% of leaf area). Easily manageable with timely bio-fungicide or targeted spot treatments."
    elif affected_percentage <= 50.0:
        severity_level = "Moderate"
        explanation = f"Moderate disease spread ({affected_percentage}% of leaf area). Multiple active lesion clusters observed. Immediate systemic or contact treatment required to arrest progression."
    else:
        severity_level = "Severe"
        explanation = f"Extensive infection ({affected_percentage}% of leaf area). Extensive cellular necrosis and loss of photosynthetic capacity. Requires urgent curative action and pruning of severely damaged foliage."

    # 3. Generate High-Quality Diagnostic Visual Overlay
    # Create semi-transparent colored mask on lesions (Red/Amber for necrotic, Magenta/Cyan for powdery)
    annotated = img.copy()
    overlay_color = (0, 0, 220) if not is_powdery else (210, 105, 30) # BGR Red or Cyan
    
    colored_mask = np.zeros_like(img)
    colored_mask[cleaned_lesion > 0] = overlay_color
    
    # Blend 65% original + 35% lesion highlight
    alpha = 0.40
    cv2.addWeighted(colored_mask, alpha, annotated, 1.0, 0, annotated)
    
    # Outline individual lesion spots in bright amber
    lesion_contours, _ = cv2.findContours(cleaned_lesion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lesion_count = 0
    for lc in lesion_contours:
        if cv2.contourArea(lc) > 20: # Ignore speckles
            cv2.drawContours(annotated, [lc], -1, (0, 140, 255), 1)
            lesion_count += 1
            
    # Outline the whole leaf in crisp emerald green
    if valid_contours:
        cv2.drawContours(annotated, valid_contours, -1, (50, 205, 50), 2)
        
    # Add diagnostic watermark badge in top corner
    badge_color = (46, 139, 87) if severity_level == "Low" else ((0, 140, 255) if severity_level == "Moderate" else (34, 34, 200))
    cv2.rectangle(annotated, (15, 15), (270, 65), (255, 255, 255), -1)
    cv2.rectangle(annotated, (15, 15), (270, 65), badge_color, 2)
    cv2.putText(annotated, f"Severity: {severity_level} ({affected_percentage}%)", (25, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.65, badge_color, 2)

    cv2.imwrite(overlay_path, annotated)

    return {
        "affected_area_percentage": affected_percentage,
        "severity_level": severity_level,
        "is_reliable": True,
        "explanation": explanation,
        "overlay_filename": overlay_filename,
        "overlay_path": f"/uploads/{overlay_filename}",
        "lesion_count": lesion_count,
        "leaf_pixel_count": total_leaf_pixels
    }
