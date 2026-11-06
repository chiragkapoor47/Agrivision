"""
TAH-015: Educational Agricultural Resources Router
Provides comprehensive agronomic learning modules in English, Hindi, and Assamese.
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas.common import EducationalResource

router = APIRouter(prefix="/resources", tags=["Educational Resources"])

EDUCATIONAL_CATALOG: List[dict] = [
    {
        "id": "edu-1",
        "category": "disease_identification",
        "title": "Early vs Late Blight Identification Guide",
        "title_hi": "अगेती बनाम पछेती झुलसा पहचान गाइड",
        "title_as": "আগতীয়া বনাম পাচতীয়া পাতপোৰা চিনাক্তকৰণ সহায়িকা",
        "summary": "Master visual discrimination between Alternaria solani target rings and Phytophthora infestans water-soaked lesions.",
        "summary_hi": "ऑल्टरनेरिया के गोल छल्लों और फाइटोफ्थोरा के पानीदार धब्बों में सटीक अंतर पहचानें।",
        "summary_as": "অল্টাৰনেৰিয়া আৰু ফাইটোফথৰাৰ পাতৰ দাগৰ মাজত পাৰ্থক্য বুজি লওক।",
        "steps_or_points": [
            "Check spot patterns: Early blight displays concentric rings like a target board, while late blight shows irregular water-soaked blotches.",
            "Inspect leaf undersides: In humid mornings, late blight displays white cottony mildew on the underside of leaves.",
            "Examine disease progression: Early blight begins on older lower leaves; late blight attacks tender upper leaves, stems, and fruits simultaneously.",
            "Weather correlation: Early blight flourishes in warm fluctuating conditions; late blight spreads exponentially during cool foggy rain (15-22°C)."
        ],
        "read_time_mins": 5,
        "badge": "Field Guide"
    },
    {
        "id": "edu-2",
        "category": "organic_farming",
        "title": "Making Potent Neem Oil Foliar Bio-Shield (1500 ppm)",
        "title_hi": "शक्तिशाली नीम तेल बायो-कीटनाशक घोल बनाना",
        "title_as": "শক্তিশালী নিম তেলৰ জৈৱিক কীটনাশক প্ৰস্তুত কৰা",
        "summary": "Step-by-step recipe to formulate cold-pressed neem spray that breaks insect vector life cycles and curtails fungal mycelia.",
        "summary_hi": "कीटों और फफूंद दोनों की रोकथाम के लिए घर पर नीम तेल का प्रभावी घोल तैयार करें।",
        "summary_as": "কীট-পতঙ্গ আৰু ভেকুৰ নাশ কৰিবলৈ নিম তেলৰ ফলপ্ৰসূ স্প্ৰে প্ৰস্তুত কৰক।",
        "steps_or_points": [
            "Measure 5 ml of cold-pressed neem oil (minimum 1500 ppm azadirachtin) per 1 liter of lukewarm water.",
            "Add 1 ml of mild organic liquid soap or khadi soap solution as an emulsifier.",
            "Shake vigorously until a uniform milky white emulsion forms with no free floating oil droplets.",
            "Spray during early morning (6:30 - 8:30 AM) or dusk to protect beneficial pollinators and avoid sun leaf scorch."
        ],
        "read_time_mins": 4,
        "badge": "Organic Protocol"
    },
    {
        "id": "edu-3",
        "category": "preventive_practices",
        "title": "Canopy Microclimate & Spacing Management",
        "title_hi": "हवादार पौध दूरी और नमी प्रबंधन",
        "title_as": "গছৰ ব্যৱধান আৰু বায়ু চলাচল নিয়ন্ত্ৰণ",
        "summary": "How strategic crop spacing, staking, and lower foliage pruning reduces canopy relative humidity below fungal sporulation thresholds.",
        "summary_hi": "उचित दूरी और कटाई-छंटाई द्वारा पत्तियों के बीच हवा का प्रवाह बनाकर फफूंद रोकें।",
        "summary_as": "উপযুক্ত ব্যৱধান আৰু তলৰ পাত ছাঁটি ভেকুৰৰ সংক্ৰমণ হ্ৰাস কৰক।",
        "steps_or_points": [
            "Never exceed recommended plant density; maintain 60 x 60 cm for indeterminate tomatoes and 45 x 20 cm for potatoes.",
            "Prune all ground-touching suckers and foliage within 30 cm of soil surface to halt splash-borne pathogen inoculation.",
            "Stake vines securely with bamboo trellises to elevate green tissue above soil dampness.",
            "Orient rows parallel to prevailing wind directions to facilitate continuous airflow through dense canopies."
        ],
        "read_time_mins": 6,
        "badge": "Cultural Practice"
    },
    {
        "id": "edu-4",
        "category": "organic_farming",
        "title": "Trichoderma & Pseudomonas Soil Bio-Priming",
        "title_hi": "ट्राइकोडर्मा और स्यूडोमोनास से जैविक भूमि उपचार",
        "title_as": "ট্ৰাইকোডাৰ্মাৰে মাটি আৰু বীজ শোধন পদ্ধতি",
        "summary": "Harness antagonist microbial bio-agents to suppress root rots, damping off, and vascular wilts naturally.",
        "summary_hi": "जड़ सड़न और उकठा रोग की रोकथाम के लिए लाभकारी मित्र फफूंद का प्रयोग।",
        "summary_as": "শিপা পচন ৰোগ প্ৰতিৰোধ কৰিবলৈ বন্ধু ভেঁকুৰ আৰু বেক্টেৰিয়াৰ ব্যৱহাৰ।",
        "steps_or_points": [
            "Mix 2.5 kg Trichoderma viride powder with 500 kg well-cured farmyard manure (FYM); keep moist under shade for 7 days until white mycelial filaments bloom.",
            "Broadcast enriched manure evenly over 1 acre prior to final harrowing.",
            "For seed treatment, dress 1 kg seeds with 10 g Trichoderma powder using 10 ml jaggery (gur) slurry as a sticker.",
            "Never mix bio-agents directly with chemical fungicides; maintain an interval of at least 10 days."
        ],
        "read_time_mins": 5,
        "badge": "Bio-Control"
    },
    {
        "id": "edu-5",
        "category": "crop_care",
        "title": "Paddy Bacterial Leaf Blight: Integrated Containment",
        "title_hi": "धान में जीवाणु झुलसा का एकीकृत रोकथाम",
        "title_as": "ধানৰ বেক্টেৰিয়াজনিত পাতপোৰা ৰোগৰ সংহত প্ৰতিৰোধ",
        "summary": "Urgent remedial steps when translucent wavy lesions appear on rice leaf tips during the tillering and panicle emergence stages.",
        "summary_hi": "धान में पत्ते झुलसने पर तुरंत अपनाए जाने वाले कदम और यूरिया नियंत्रण।",
        "summary_as": "ধানৰ পাত শুকোৱাৰ লক্ষণ দেখা পালে তাৎক্ষণিকভাৱে ল'বলগীয়া ব্যৱস্থা।",
        "steps_or_points": [
            "Immediately stop top-dressing with nitrogen/urea fertilizers during active lesion expansion.",
            "Drain field water completely for 3-4 days to expose soil and lower stem sheaths to direct sunlight.",
            "Spray fresh cow dung supernatant filtrate (20 kg cow dung in 100 L water) across affected paddy plots.",
            "If severe, apply recommended antibiotic bactericide (Streptocycline 6 g + Copper Oxychloride 50 g in 60 L water per bigha)."
        ],
        "read_time_mins": 7,
        "badge": "Rice Guide"
    }
]

@router.get("", response_model=List[EducationalResource])
def get_educational_resources(
    category: Optional[str] = Query(None, description="Filter by category (disease_identification, organic_farming, preventive_practices, crop_care)"),
    language: Optional[str] = Query("en")
):
    """Retrieve educational guides and agricultural extension articles"""
    items = EDUCATIONAL_CATALOG
    if category and category.lower() not in ["", "all"]:
        items = [i for i in items if i["category"].lower() == category.lower()]
    return items
