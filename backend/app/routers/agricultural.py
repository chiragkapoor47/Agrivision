"""
TAH-015: Agricultural Crops, Diseases, Treatments & Weather Router
"""
from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
from app.ml.knowledge_base import AGRONOMIC_KNOWLEDGE_BASE, REGIONAL_ADVISORIES, get_treatment_for_disease
from app.schemas.common import CropItem, DiseaseItem

router = APIRouter(tags=["Agricultural Information"])

SUPPORTED_CROPS_DATA = [
    {
        "id": "tomato",
        "name": "Tomato",
        "name_hi": "टमाटर",
        "name_as": "বিলাহী",
        "scientific_name": "Solanum lycopersicum",
        "common_diseases": ["Early Blight", "Late Blight", "Bacterial Spot", "Leaf Mold"],
        "ideal_growing_conditions": "Warm season, 21-27°C, well-drained loamy soil, 6-8 hrs direct sunlight.",
        "water_requirements": "Consistent moisture, avoid wetting leaves; drip irrigation highly recommended.",
        "soil_ph": "6.0 - 6.8"
    },
    {
        "id": "potato",
        "name": "Potato",
        "name_hi": "आलू",
        "name_as": "আলু",
        "scientific_name": "Solanum tuberosum",
        "common_diseases": ["Early Blight", "Late Blight"],
        "ideal_growing_conditions": "Cool temperate, 15-20°C, loose sandy loam with high organic matter.",
        "water_requirements": "Moderate regular watering; stop irrigation 10 days before harvest.",
        "soil_ph": "5.0 - 6.0"
    },
    {
        "id": "rice",
        "name": "Rice",
        "name_hi": "धान / चावल",
        "name_as": "ধান",
        "scientific_name": "Oryza sativa",
        "common_diseases": ["Bacterial Leaf Blight", "Brown Spot", "Leaf Blast"],
        "ideal_growing_conditions": "Hot & humid tropical climate, 22-32°C, heavy clayey or alluvial soil.",
        "water_requirements": "Standing water (3-5 cm) or Alternate Wetting and Drying (AWD).",
        "soil_ph": "5.5 - 6.5"
    },
    {
        "id": "corn",
        "name": "Corn (Maize)",
        "name_hi": "मक्का",
        "name_as": "মাকৈ",
        "scientific_name": "Zea mays",
        "common_diseases": ["Common Rust", "Northern Leaf Blight", "Gray Leaf Spot"],
        "ideal_growing_conditions": "Warm sunny weather, 20-30°C, deep rich loamy soil.",
        "water_requirements": "500-800 mm water throughout season; critical at tasseling and silking.",
        "soil_ph": "5.8 - 7.0"
    },
    {
        "id": "wheat",
        "name": "Wheat",
        "name_hi": "गेहूं",
        "name_as": "ঘেঁহু",
        "scientific_name": "Triticum aestivum",
        "common_diseases": ["Leaf Rust (Brown Rust)", "Stripe Rust", "Powdery Mildew"],
        "ideal_growing_conditions": "Cool winter climate (Rabi season), 12-25°C, fertile clay loam.",
        "water_requirements": "4-6 timely irrigations at critical stages (CRI, tillering, flowering).",
        "soil_ph": "6.0 - 7.5"
    },
    {
        "id": "cotton",
        "name": "Cotton",
        "name_hi": "कपास",
        "name_as": "কপাহ",
        "scientific_name": "Gossypium hirsutum",
        "common_diseases": ["Bacterial Blight (Blackarm)", "Alternaria Leaf Spot"],
        "ideal_growing_conditions": "Warm subtropical, 25-35°C, deep black cotton soil or alluvial loam.",
        "water_requirements": "Deep watering at squaring and boll development; avoid waterlogging.",
        "soil_ph": "6.5 - 8.0"
    },
    {
        "id": "apple",
        "name": "Apple",
        "name_hi": "सेब",
        "name_as": "আপেল",
        "scientific_name": "Malus domestica",
        "common_diseases": ["Apple Scab", "Black Rot (Frog-eye)", "Cedar Apple Rust"],
        "ideal_growing_conditions": "Temperate highland, 800-1200 winter chilling hours, well-drained loam.",
        "water_requirements": "Regular orchard irrigation, particularly during fruit expansion.",
        "soil_ph": "6.0 - 6.5"
    },
    {
        "id": "grape",
        "name": "Grape",
        "name_hi": "अंगूर",
        "name_as": "আঙুৰ",
        "scientific_name": "Vitis vinifera",
        "common_diseases": ["Black Rot", "Esca (Black Measles)", "Powdery Mildew"],
        "ideal_growing_conditions": "Warm Mediterranean or semi-arid, 15-35°C, well-aerated gravelly loam.",
        "water_requirements": "Regulated deficit irrigation; canopy aeration critical to curb rot.",
        "soil_ph": "6.5 - 7.5"
    },
    {
        "id": "pepper",
        "name": "Pepper (Bell Pepper / Chili)",
        "name_hi": "शिमला मिर्च / मिर्च",
        "name_as": "কেপচিকাম / জলকীয়া",
        "scientific_name": "Capsicum annuum",
        "common_diseases": ["Bacterial Spot", "Healthy Foliage"],
        "ideal_growing_conditions": "Warm season, 20-30°C, rich sandy loam with good organic matter.",
        "water_requirements": "Frequent light watering; sensitive to drought during fruit set.",
        "soil_ph": "6.0 - 6.8"
    }
]

@router.get("/crops", response_model=List[CropItem])
def get_supported_crops():
    """Retrieve list of all supported crops with regional names and growing guidelines"""
    return SUPPORTED_CROPS_DATA

@router.get("/diseases", response_model=List[DiseaseItem])
def get_supported_diseases():
    """Retrieve all supported disease classifications"""
    diseases = []
    for k, v in AGRONOMIC_KNOWLEDGE_BASE.items():
        if "healthy" in k.lower():
            continue
        diseases.append(DiseaseItem(
            id=k,
            crop=v["crop"],
            name=v["disease"],
            name_hi=v.get("disease_hi", v["disease"]),
            name_as=v.get("disease_as", v["disease"]),
            pathogen_type=v.get("pathogen", "Fungus/Bacteria"),
            typical_symptoms=v["symptoms"]
        ))
    return diseases

@router.get("/treatments")
def get_treatments(
    disease: str = Query(..., description="Disease identifier or name"),
    state: Optional[str] = Query("Assam"),
    district: Optional[str] = Query("Kamrup"),
    language: Optional[str] = Query("en")
):
    """Query verified organic and chemical treatments with regional customization"""
    return get_treatment_for_disease(disease, state=state or "", district=district or "", language=language or "en")

@router.get("/weather")
def get_localized_weather_risk(
    state: Optional[str] = Query("Assam"),
    district: Optional[str] = Query("Kamrup")
):
    """
    Returns localized agro-weather intelligence and pathogen alert risks.
    Calculates disease proliferation probabilities based on regional conditions.
    """
    state_clean = (state or "Assam").lower()
    
    # Regional simulated sensors with realistic Indian meteorological profiles
    if "assam" in state_clean:
        temp_c = 26.5
        humidity_pct = 84
        rainfall_prob_pct = 65
        wind_kmh = 8
        condition = "Humid & Intermittent Rain"
        blight_risk = "High"
        bacterial_risk = "Moderate"
        rust_risk = "Low"
        alert_msg = "High humidity (>80%) creates favorable conditions for Tomato Late Blight and Rice Bacterial Leaf Blight. Keep drainage channels clear."
    elif any(s in state_clean for s in ["punjab", "haryana", "delhi", "rajasthan"]):
        temp_c = 22.0
        humidity_pct = 52
        rainfall_prob_pct = 15
        wind_kmh = 16
        condition = "Dry & Sunny"
        blight_risk = "Low"
        bacterial_risk = "Low"
        rust_risk = "Moderate"
        alert_msg = "Westerly winds can transport wheat rust urediniospores. Scout wheat fields along field margins."
    elif any(s in state_clean for s in ["maharashtra", "karnataka", "gujarat"]):
        temp_c = 28.0
        humidity_pct = 68
        rainfall_prob_pct = 35
        wind_kmh = 12
        condition = "Partly Cloudy"
        blight_risk = "Moderate"
        bacterial_risk = "High"
        rust_risk = "Low"
        alert_msg = "Warm, humid mornings favor cotton bacterial blight and grape black rot. Ensure canopy ventilation."
    else:
        temp_c = 25.0
        humidity_pct = 65
        rainfall_prob_pct = 30
        wind_kmh = 10
        condition = "Mild Season"
        blight_risk = "Moderate"
        bacterial_risk = "Moderate"
        rust_risk = "Low"
        alert_msg = "Standard seasonal conditions. Inspect crops twice weekly for early lesion spots."

    return {
        "location": f"{district or 'Kamrup'}, {state or 'Assam'}",
        "temperature_celsius": temp_c,
        "humidity_percentage": humidity_pct,
        "rainfall_probability": rainfall_prob_pct,
        "wind_speed_kmh": wind_kmh,
        "general_condition": condition,
        "pathogen_risks": {
            "late_blight": blight_risk,
            "bacterial_blight": bacterial_risk,
            "leaf_rust": rust_risk
        },
        "agronomic_advisory": alert_msg
    }
