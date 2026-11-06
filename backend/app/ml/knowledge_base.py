"""
TAH-015: Agronomic Knowledge Base & Treatment Recommendation Engine
Provides scientifically verified treatments:
- Organic Treatments (Bio-fungicides, Neem formulations, Botanicals)
- Chemical Treatments (Active ingredients, application methods, safety PPE, Pre-Harvest Intervals [PHI])
- Preventive Measures (Cultural practices, sanitation, rotation)
- Regional Indian Agro-climatic Adaptation (Assam/NE Humid, Indo-Gangetic Plains, Deccan Plateau)
- Multilingual names & descriptions (English, Hindi, Assamese)
"""

AGRONOMIC_KNOWLEDGE_BASE = {
    # TOMATO
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "crop_hi": "टमाटर",
        "crop_as": "বিলাহী",
        "disease": "Early Blight",
        "disease_hi": "अगेती झुलसा",
        "disease_as": "আগতীয়া পাতপোৰা ৰোগ",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": [
            "Concentric rings or 'target-board' spots on older lower leaves.",
            "Yellow halo (chlorosis) surrounding brown necrotic lesions.",
            "Premature defoliation starting from base moving upwards, exposing fruit to sunscald.",
            "Dark, sunken, leathery cankers on stems and fruit calyx."
        ],
        "symptoms_hi": [
            "निचली पुरानी पत्तियों पर संकेन्द्री छल्लों ('टारगेट बोर्ड') जैसे धब्बे।",
            "भूरे घावों के चारों ओर पीला प्रभामंडल (क्लोरोसिस)।",
            "पत्तियों का समय से पहले गिरना जो नीचे से ऊपर की ओर बढ़ता है।",
            "तने और फल के पास गहरे, धंसे हुए घाव।"
        ],
        "symptoms_as": [
            "তলৰ পুৰণি পাতবোৰত বৃত্তাকাৰ বা লক্ষ্য-বোর্ডৰ দৰে কজলা দাগ।",
            "পাতৰ কজলা ঘাঁৰ চাৰিওফালে হালধীয়া আভা।",
            "তলৰ পৰা আৰম্ভ হৈ পাতবোৰ অকালতে সৰি যোৱা।",
            "কাণ্ড আৰু ফলৰ ঠাৰিত ক'লা, বহি যোৱা দাগ।"
        ],
        "organic_treatment": {
            "title": "Bio-Fungicide & Botanical Management",
            "remedies": [
                "Apply cold-pressed Neem Oil (1500 ppm) at 4-5 ml per liter of water with 1 ml liquid soap as an emulsifier every 7-10 days.",
                "Foliar spray of Trichoderma harzianum or Trichoderma viride bio-formulation (5 g/L) to colonize leaf surface and outcompete fungal mycelia.",
                "Spray copper hydroxide (Bordeaux mixture 1%) during early morning hours to inhibit fungal spore germination.",
                "Drench soil with compost tea enriched with Pseudomonas fluorescens (10 ml/L) to strengthen root immunity."
            ]
        },
        "chemical_treatment": {
            "title": "Approved Fungicidal Interventions",
            "active_ingredients": ["Mancozeb 75% WP", "Chlorothalonil 75% WP", "Azoxystrobin 18.2% + Difenoconazole 11.4% SC"],
            "application_method": "Dissolve Mancozeb 75% WP @ 2.5 g/L water or Azoxystrobin + Difenoconazole @ 1 ml/L. Spray evenly across canopy, wetting both upper and lower leaf surfaces.",
            "safety_precautions": "Wear PPE including nitrile gloves, eye goggles, and N95 dust/mist respirator. Never spray during windy conditions or hot midday sun (>32°C). Wash thoroughly after application.",
            "pre_harvest_interval_days": 7
        },
        "preventive_measures": [
            "Practice 2-3 year crop rotation with non-solanaceous crops (avoid planting after potato, eggplant, or pepper).",
            "Utilize drip irrigation to prevent water splash from soil to lower foliage.",
            "Prune bottom 30 cm of foliage as plants mature to enhance airflow and reduce humidity.",
            "Mulch bed with clean straw or plastic mulch to create a barrier between soil-borne spores and lower leaves.",
            "Disinfect pruning shears between plants using 70% isopropyl alcohol."
        ]
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "crop_hi": "टमाटर",
        "crop_as": "বিলাহী",
        "disease": "Late Blight",
        "disease_hi": "पछेती झुलसा",
        "disease_as": "পাচতীয়া পাতপোৰা ৰোগ",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": [
            "Irregular water-soaked pale green lesions on leaves rapidly expanding into large brown-black blotches.",
            "Delicate white cottony fungal mold visible on leaf undersides in humid or foggy conditions.",
            "Stem collapse and greasy brown sunken rot on green and ripe fruits.",
            "Rapid whole-plant destruction within 4-7 days under cool, overcast, high-moisture weather."
        ],
        "symptoms_hi": [
            "पत्तियों पर अनियमित पानी से भीगे जैसे हल्के हरे धब्बे जो तेजी से काले-भूरे हो जाते हैं।",
            "उच्च आर्द्रता या कोहरे में पत्तियों के निचले हिस्से पर सफेद फफूंद दिखाई देना।",
            "तने का सड़ना और फलों पर चिकना, भूरा सड़ांध वाला घाव।",
            "ठंडे, आर्द्र मौसम में 4-7 दिनों के भीतर पूरे पौधे का नष्ट होना।"
        ],
        "symptoms_as": [
            "পাতত পানী লগাৰ দৰে অনিয়মীয়া শেঁতা সেউজীয়া দাগ যিবোৰ সোনকালে ক'লা-মুগা হৈ পৰে।",
            "সেমেকা বতৰত পাতৰ তলফালে বগা কপাহৰ দৰে ভেকুৰ দেখা পোৱা।",
            "গছজোপাৰ কাণ্ড আৰু ফলত পিচ্ছিল মুগা পচন ধৰা।",
            "শীতল আৰু সেমেকা বতৰত ৪-৭ দিনৰ ভিতৰত গছজোপা শুকাই ধ্বংস হোৱা।"
        ],
        "organic_treatment": {
            "title": "Preventive Bio-Shield & Mineral Sprays",
            "remedies": [
                "Spray Bordeaux mixture (1% copper sulfate + hydrated lime) proactively before prolonged cloudy or drizzling spells.",
                "Foliar application of Bacillus subtilis (BS-01 strain) at 4 g/L to colonize leaf surface prior to oomycete penetration.",
                "Extract of Horsetail (Equisetum arvense) rich in natural silica (100 g boiled in 1L water, diluted 1:5) to thicken epidermal cell walls.",
                "Immediately cut and bag infected plants; never add late-blight diseased vines to compost heaps."
            ]
        },
        "chemical_treatment": {
            "title": "Systemic & Translaminar Oomyceticides",
            "active_ingredients": ["Metalaxyl 8% + Mancozeb 64% WP", "Cymoxanil 8% + Mancozeb 64% WP", "Dimethomorph 50% WP"],
            "application_method": "Apply Metalaxyl + Mancozeb @ 2 g/L or Dimethomorph @ 1 g/L at the first visible symptom or local weather blight alert. Repeat after 7-10 days if humid conditions persist.",
            "safety_precautions": "Full personal protective equipment required. Do not apply near aquatic bodies or honeybee hives during flowering. Keep children and livestock away from treated plots for 48 hours.",
            "pre_harvest_interval_days": 14
        },
        "preventive_measures": [
            "Maintain wider spacing (60 x 60 cm) for rapid morning drying of leaves.",
            "Stake and trellis indeterminate varieties securely off the ground.",
            "Strictly avoid overhead sprinkler irrigation; apply water directly to soil via drip tubes.",
            "Choose certified late-blight resistant hybrids (e.g. Mountain Magic, Defiant, or regional resistant varieties)."
        ]
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "crop_hi": "टमाटर",
        "crop_as": "বিলাহী",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ पत्ती",
        "disease_as": "নিৰোগী পাত",
        "pathogen": "None (Healthy)",
        "symptoms": [
            "Vibrant, deep green foliage with uniform chlorophyll distribution.",
            "No necrotic lesions, chlorotic rings, spots, or fungal webbing.",
            "Turgid petiole and upright leaf posture indicating optimum water balance.",
            "Intact leaf margins and active photosynthetic activity."
        ],
        "symptoms_hi": [
            "गहरी हरी, चमकदार पत्तियां जिनमें एकसमान क्लोरोफिल है।",
            "कोई भी सूखा धब्बा, पीलापन या फफूंद का कोई लक्षण नहीं।",
            "पौधे की पत्तियां तरोताजा और मजबूत।",
            "सक्रिय प्रकाश संश्लेषण और स्वस्थ विकास।"
        ],
        "symptoms_as": [
            "উজ্জ্বল সেউজীয়া আৰু স্বাস্থ্যৱান পাত।",
            "কোনো কলা দাগ, হালধীয়া আভা বা ভেকুৰৰ চিহ্ন নাই।",
            "পাত আৰু কাণ্ড সতেজ আৰু দৃঢ়।",
            "উপযুক্ত সালোক-সংশ্লেষণ আৰু সুস্বাস্থ্য।"
        ],
        "organic_treatment": {
            "title": "Maintenance & Growth Optimization",
            "remedies": [
                "Apply vermicompost (250 g per plant) around root zone every 25 days.",
                "Foliar spray of Seaweed extract (2 ml/L) once a month for micronutrient balance and disease resistance.",
                "Prophylactic Neem oil spray (3 ml/L) every 14 days to deter sap-sucking insect vectors (whiteflies/aphids)."
            ]
        },
        "chemical_treatment": {
            "title": "No Chemical Intervention Required",
            "active_ingredients": ["None required"],
            "application_method": "Continue regular nutrient feeding (e.g. 19-19-19 NPK @ 3 g/L fertigation).",
            "safety_precautions": "Avoid unnecessary chemical usage to preserve beneficial predatory insects.",
            "pre_harvest_interval_days": 0
        },
        "preventive_measures": [
            "Keep soil consistently moist, avoiding alternating drought and waterlogging to prevent Blossom End Rot.",
            "Ensure adequate calcium supply in the root zone.",
            "Inspect weekly for early aphid or whitefly presence."
        ]
    },

    # POTATO
    "Potato___Early_blight": {
        "crop": "Potato",
        "crop_hi": "आलू",
        "crop_as": "আলু",
        "disease": "Early Blight",
        "disease_hi": "अगेती झुलसा",
        "disease_as": "আগতীয়া পাতপোৰা ৰোগ",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": [
            "Small, dark brown to black circular lesions on older lower foliage with target concentric rings.",
            "Severe yellowing of tissue adjacent to spots causing leaf drop.",
            "Dark, sunken, dry rot on potato tubers with purplish-brown raised borders."
        ],
        "symptoms_hi": [
            "पुरानी पत्तियों पर गोल, भूरे-काले संकेन्द्री छल्लों वाले धब्बे।",
            "धब्बों के आसपास पत्तियों का पीला पड़ना और गिरना।",
            "आलू के कंदों पर गहरा, सूखा गड्ढेदार सड़ांध।"
        ],
        "symptoms_as": [
            "তলৰ পুৰণি পাতবোৰত ঘুৰণীয়া লক্ষ্য-বোর্ডৰ দৰে কজলা মুগা দাগ।",
            "দাগৰ চাৰিওফালে পাত হালধীয়া হৈ সৰি পৰা।",
            "আলুৰ গাত শুকান ক'লা-মুগা দাগ পৰা।"
        ],
        "organic_treatment": {
            "title": "Organic Defense & Soil Inoculation",
            "remedies": [
                "Spray 5% Neem Seed Kernel Extract (NSKE) at 50 g/L or commercial Azadirachtin (1500 ppm @ 4 ml/L).",
                "Apply Trichoderma viride talc formulation (2.5 kg/ha mixed with 500 kg well-decomposed FYM) at earthing up.",
                "Foliar spray of potassium silicate (2 ml/L) to strengthen cuticle resistance."
            ]
        },
        "chemical_treatment": {
            "title": "Curative and Protective Fungicides",
            "active_ingredients": ["Mancozeb 75% WP", "Propineb 70% WP", "Difenoconazole 25% EC"],
            "application_method": "Spray Propineb 70% WP @ 2.5 g/L or Difenoconazole @ 0.5 ml/L at onset of symptoms. Repeat after 12 days.",
            "safety_precautions": "Wear waterproof apron, gloves, and protective boots. Do not inhale spray mist.",
            "pre_harvest_interval_days": 10
        },
        "preventive_measures": [
            "Plant only certified disease-free seed tubers.",
            "Ensure balanced fertilization; avoid potassium and nitrogen deficiency which predisposes potato to Alternaria.",
            "Avoid harvesting tubers in wet soil conditions to prevent wound contamination."
        ]
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "crop_hi": "आलू",
        "crop_as": "আলু",
        "disease": "Late Blight",
        "disease_hi": "पछेती झुलसा",
        "disease_as": "পাচতীয়া পাতপোৰা ৰোগ",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": [
            "Water-soaked dark lesions at tips and margins of leaves.",
            "White frost-like mildew on leaf under-surfaces during mornings with high relative humidity (>90%).",
            "Entire haulm (foliage) rapidly turning black and collapsing with foul odor.",
            "Coppery-brown dry or wet rot inside stored tubers."
        ],
        "symptoms_hi": [
            "पत्ती के किनारों और सिरों पर पानी से भीगे गहरे काले धब्बे।",
            "सुबह की अधिक नमी में पत्तियों के नीचे सफेद पाले जैसी फफूंद।",
            "पूरा पौधा काला पड़कर सड़ जाना और दुर्गंध आना।",
            "आलू के अंदर तांबे जैसा भूरा सूखा या गीला सड़ांध।"
        ],
        "symptoms_as": [
            "পাতৰ আগ আৰু দাঁতিত পানী লগাৰ দৰে ক'লা দাগ।",
            "ৰাতিপুৱা সেমেকা বতৰত পাতৰ তলফালে কুঁৱলীৰ দৰে বগা ভেকুৰ।",
            "সমগ্ৰ আলু গছজোপা ক'লা পৰি লেবেলি যোৱা।",
            "আলুৰ ভিতৰত তাম বৰণীয়া পচন ধৰা।"
        ],
        "organic_treatment": {
            "title": "Bio-Oomyceticide & Cultural Destruction",
            "remedies": [
                "Prophylactic spray of Bordeaux Mixture (1%) or Copper Oxychloride 50% WP (2.5 g/L).",
                "Foliar spray of bio-fungicide Ampelomyces quisqualis or Trichoderma harzianum at 5 g/L.",
                "Burn or deeply bury all infected haulms at least 15 days before tuber digging."
            ]
        },
        "chemical_treatment": {
            "title": "Potent Translaminar & Systemic Fungicides",
            "active_ingredients": ["Metalaxyl 8% + Mancozeb 64% WP", "Fenamidone 10% + Mancozeb 50% WG", "Mandipropamid 23.4% SC"],
            "application_method": "Apply Fenamidone + Mancozeb @ 2.5 g/L or Mandipropamid @ 0.8 ml/L immediately when cloud cover and drizzle persist for 48 hours.",
            "safety_precautions": "Strict PPE compliance. Wash sprayer completely away from open wells or streams.",
            "pre_harvest_interval_days": 14
        },
        "preventive_measures": [
            "De-haulm (cut foliage at ground level) 10-14 days before harvest to harden tuber skin and prevent spore transfer.",
            "Ensure high earthing-up (at least 15 cm soil ridge) so rain cannot wash spores into tuber zone.",
            "Store harvested tubers only in dry, well-ventilated, cold storage (3-4°C)."
        ]
    },
    "Potato___healthy": {
        "crop": "Potato",
        "crop_hi": "आलू",
        "crop_as": "আলু",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ पत्ती",
        "disease_as": "নিৰোগী পাত",
        "pathogen": "None (Healthy)",
        "symptoms": ["Lush dark green canopy, sturdy stems, uniform leaflet formation without necrotic spots."],
        "symptoms_hi": ["घना गहरा हरा पौधा, मजबूत तने, पत्तियों पर कोई दाग-धब्बा नहीं।"],
        "symptoms_as": ["গাঢ় সেউজীয়া সুস্থ গছ, কোনো দাগ বা পচন নাই।"],
        "organic_treatment": {
            "title": "Crop Vitality Maintenance",
            "remedies": [
                "Apply potassium-rich organic manure or wood ash to promote tuber bulking.",
                "Neem oil spray (3 ml/L) every 14 days as preventative."
            ]
        },
        "chemical_treatment": {
            "title": "None Required",
            "active_ingredients": ["None required"],
            "application_method": "Maintain balanced N-P-K (120:60:120 kg/ha equivalent).",
            "safety_precautions": "Monitor weekly for aphids that transmit potato leafroll virus.",
            "pre_harvest_interval_days": 0
        },
        "preventive_measures": [
            "Perform timely earthing-up to prevent greening of tubers by sunlight.",
            "Avoid excessive late nitrogen fertilization which delays skin setting."
        ]
    },

    # RICE
    "Rice___Bacterial_leaf_blight": {
        "crop": "Rice",
        "crop_hi": "धान / चावल",
        "crop_as": "ধান",
        "disease": "Bacterial Leaf Blight",
        "disease_hi": "जीवाणु पत्ती झुलसा",
        "disease_as": "বেক্টেৰিয়াজনিত পাতপোৰা ৰোগ",
        "pathogen": "Xanthomonas oryzae pv. oryzae (Bacteria)",
        "symptoms": [
            "Water-soaked wavy translucent stripes originating from leaf tips and margins.",
            "Stripes rapidly turn pale yellow to greyish-white, drying up the leaf.",
            "Milky or amber bacterial ooze droplets on leaf surfaces in early morning dew.",
            "Severe 'Kresek' (wilt) symptom in seedlings resulting in complete crop loss."
        ],
        "symptoms_hi": [
            "पत्ती के सिरों और किनारों से शुरू होने वाली पानी जैसी लहरदार धारियां।",
            "धारियों का तेजी से पीला और फिर भूरा-सफेद होकर सूख जाना।",
            "सुबह की ओस में पत्तियों पर हल्के पीले जीवाणु के चिपचिपे कतरे।",
            "शुरुआती पौधों का मुरझाना (क्रेसेक) जिससे भारी नुकसान होता है।"
        ],
        "symptoms_as": [
            "পাতৰ আগ আৰু কাষৰ পৰা পানী লগাৰ দৰে ঢৌ খেলোৱা দাগ আৰম্ভ হোৱা।",
            "দাগবোৰ ক্ৰমে হালধীয়া হৈ বগা-ধূসৰ বৰণ লৈ পাতখন শুকাই যোৱা।",
            "ৰাতিপুৱাৰ নিয়ঁৰত পাতৰ পিঠিত আঠাযুক্ত হালধীয়া বেক্টেৰিয়াৰ টোপাল।",
            "পুলি অৱস্থাত গছজোপাই শুকাই যোৱা ('ক্ৰেচেক' লক্ষণ)।"
        ],
        "organic_treatment": {
            "title": "Botanical and Bio-Control Remedies",
            "remedies": [
                "Spray fresh cow dung filtrate: mix 20 kg fresh cow dung in 100 L water, filter through muslin cloth, and spray over 1 acre.",
                "Foliar spray of Pseudomonas fluorescens (10 g/L) at tillering and panicle initiation stages.",
                "Apply neem cake in paddy soil at 150 kg/hectare during land preparation."
            ]
        },
        "chemical_treatment": {
            "title": "Bactericidal & Copper Combinations",
            "active_ingredients": ["Streptocycline (Streptomycin sulphate 90% + Tetracycline hydrochloride 10%)", "Copper Oxychloride 50% WP"],
            "application_method": "Mix Streptocycline @ 6 g + Copper Oxychloride @ 50 g in 60 liters of water per bigha (approx 150-200 L/acre). Spray twice at 10-day intervals.",
            "safety_precautions": "Avoid direct dermal exposure. Strictly adhere to recommended low antibiotics dosage to prevent antimicrobial resistance.",
            "pre_harvest_interval_days": 21
        },
        "preventive_measures": [
            "Drain flooded field water for 3-4 days to arrest bacterial proliferation.",
            "Temporarily suspend top dressing of nitrogenous fertilizers (Urea) during active outbreak.",
            "Clean farm equipment thoroughly between affected and clean paddies to avoid mechanical transmission.",
            "Adopt certified resistant varieties (e.g. Swarna Sub1, IR64, Bahadur, Ranjit Sub1)."
        ]
    },
    "Rice___Brown_spot": {
        "crop": "Rice",
        "crop_hi": "धान / चावल",
        "crop_as": "ধান",
        "disease": "Brown Spot",
        "disease_hi": "भूरा धब्बा रोग",
        "disease_as": "মুগা দাগ ৰোগ",
        "pathogen": "Bipolaris oryzae (Fungus)",
        "symptoms": [
            "Isolated oval or circular sesame seed-shaped spots with dark brown margins and grey center.",
            "Yellow halo encircling the lesion.",
            "Infected seeds become shriveled, discolored, and light in weight."
        ],
        "symptoms_hi": [
            "पत्तियों पर तिल के आकार के अंडाकार धब्बे जिनका किनारा भूरा और केंद्र राख जैसा होता है।",
            "दाने काले, बदरंग और खोखले हो जाते हैं।"
        ],
        "symptoms_as": [
            "পাতত তিলৰ গুটিৰ দৰে ডিম্বাকৃতিৰ মুগা দাগ যাৰ মাজভাগ ধোঁৱা বৰণীয়া।",
            "ধানৰ চাউলবোৰ ক'লা আৰু পাতল হৈ পৰে।"
        ],
        "organic_treatment": {
            "title": "Nutrient Correction & Bio-Inoculation",
            "remedies": [
                "Treat seed with Trichoderma harzianum @ 10 g/kg seed before sowing.",
                "Apply potassium silicate (2.5 ml/L) or farmyard manure enriched with zinc and potash.",
                "Brown spot predominantly affects nutritionally deficient soils; correct soil zinc and potash immediately."
            ]
        },
        "chemical_treatment": {
            "title": "Triazole Fungicides",
            "active_ingredients": ["Propiconazole 25% EC", "Mancozeb 75% WP", "Isoprothiolane 40% EC"],
            "application_method": "Spray Propiconazole 25% EC @ 1 ml/L or Mancozeb @ 2 g/L at tillering and boot leaf stages.",
            "safety_precautions": "Use protective gloves and face mask. Do not release contaminated wash water into fish ponds.",
            "pre_harvest_interval_days": 15
        },
        "preventive_measures": [
            "Soak seeds in warm water (52°C) for 10 minutes prior to germination.",
            "Apply balanced fertilizer including micronutrients (Zinc sulphate @ 25 kg/ha).",
            "Avoid water deficit during tillering stage."
        ]
    },
    "Rice___healthy": {
        "crop": "Rice",
        "crop_hi": "धान / चावल",
        "crop_as": "ধান",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ धान",
        "disease_as": "নিৰোগী ধান",
        "pathogen": "None (Healthy)",
        "symptoms": ["Uniform green upright blades without lesions, vibrant tillering, clear nodes."],
        "symptoms_hi": ["सीधी हरी पत्तियां, बिना किसी धब्बे के, स्वस्थ कल्ले।"],
        "symptoms_as": ["সুস্থ সেউজীয়া পাত, কোনো দাগ নাই, সুন্দৰ থোক।"],
        "organic_treatment": {
            "title": "Crop Vigor Maintenance",
            "remedies": ["Apply Azospirillum and Phosphobacteria biofertilizers at 2 kg/acre mixed with FYM."]
        },
        "chemical_treatment": {
            "title": "None Required",
            "active_ingredients": ["None required"],
            "application_method": "Monitor field water depth (maintain 3-5 cm shallow water).",
            "safety_precautions": "Follow standard integrated pest management (IPM).",
            "pre_harvest_interval_days": 0
        },
        "preventive_measures": [
            "Alternate wetting and drying (AWD) irrigation to save water and strengthen tillers.",
            "Preserve spider and dragonfly populations as natural biocontrol."
        ]
    },

    # CORN (MAIZE)
    "Corn___Common_rust": {
        "crop": "Corn (Maize)",
        "crop_hi": "मक्का",
        "crop_as": "মাকৈ",
        "disease": "Common Rust",
        "disease_hi": "मक्के का रतुआ",
        "disease_as": "মাকৈৰ ৰাষ্ট ৰোগ",
        "pathogen": "Puccinia sorghi (Fungus)",
        "symptoms": [
            "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces.",
            "Pustules rupture epidermal tissue, releasing clouds of rust spores.",
            "Leaves turn chlorotic and desiccate prematurely under cool, moist weather."
        ],
        "symptoms_hi": [
            "पत्तियों के दोनों तरफ सुनहरे-भूरे से दालचीनी रंग के दानेदार फफोले।",
            "फफोले फूटने पर रतुआ जैसे पाउडर का निकलना।",
            "पत्तियों का सूखना और उपज में कमी।"
        ],
        "symptoms_as": [
            "পাতৰ দুয়োপিঠিত ডাঠ মুগা বৰণৰ ফিৰিঙতিৰ দৰে ফোহা।",
            "ফোহাবোৰ ফাটি ধূলিৰ দৰে ৰঙা-মুগা গুড়ি ওলোৱা।",
            "পাতবোৰ শুকাই ধানৰ দৰে লেবেলি যোৱা।"
        ],
        "organic_treatment": {
            "title": "Sulfur & Bio-Agent Sprays",
            "remedies": [
                "Dust Wettable Sulfur 80% WP @ 2.5 g/L during early morning hours before temperatures exceed 28°C.",
                "Foliar spray of Ampelomyces quisqualis (5 g/L) hyperparasite of rust fungi.",
                "Spray 5% garlic bulb extract (crush 500 g garlic in 10 L water with soap) for natural antifungal allicin action."
            ]
        },
        "chemical_treatment": {
            "title": "Strobilurin & Triazole Fungicides",
            "active_ingredients": ["Azoxystrobin 18.2% + Difenoconazole 11.4% SC", "Pyraclostrobin 20% WG", "Tebuconazole 25.9% EC"],
            "application_method": "Apply Azoxystrobin + Difenoconazole @ 1 ml/L or Tebuconazole @ 1 ml/L upon appearance of pustules on leaves before tasseling.",
            "safety_precautions": "Do not enter field for 24 hours post application. Ensure eye protection.",
            "pre_harvest_interval_days": 21
        },
        "preventive_measures": [
            "Select rust-tolerant hybrid corn seed varieties.",
            "Plant early in the season to avoid peak spore migration period.",
            "Plow under infected maize stover after harvest to reduce overwintering urediniospores."
        ]
    },
    "Corn___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "crop_hi": "मक्का",
        "crop_as": "মাকৈ",
        "disease": "Northern Leaf Blight",
        "disease_hi": "उत्तरी पत्ती झुलसा",
        "disease_as": "উত্তৰীয় পাতপোৰা ৰোগ",
        "pathogen": "Exserohilum turcicum (Fungus)",
        "symptoms": [
            "Long, elliptical, cigar-shaped greyish-green lesions (2.5 to 15 cm long).",
            "Lesions turn tan or dark brown with dark fungal sporulation in damp weather.",
            "Lesions coalesce, causing extensive foliage desiccation."
        ],
        "symptoms_hi": [
            "पत्तियों पर सिगार के आकार के लंबे, धूसर-हरे धब्बे (2.5 से 15 सेमी लंबे)।",
            "नम मौसम में धब्बे भूरे हो जाते हैं और पत्तियां पूरी तरह सूख जाती हैं।"
        ],
        "symptoms_as": [
            "পাতত চিগাৰৰ দৰে দীঘলীয়া ধোঁৱা-বৰণীয়া দাগ (২.৫ ৰ পৰা ১৫ চেমি দীঘল)।",
            "দাগবোৰ ক্ৰমে ডাঙৰ হৈ গোটেই পাতখন পুৰি শুকাই পেলোৱা।"
        ],
        "organic_treatment": {
            "title": "Bio-Fungicide Protection",
            "remedies": [
                "Foliar application of Trichoderma harzianum (5 g/L) before silking stage.",
                "Neem oil (1500 ppm @ 4 ml/L) combined with copper hydroxide."
            ]
        },
        "chemical_treatment": {
            "title": "Foliar Fungicides",
            "active_ingredients": ["Mancozeb 75% WP", "Propiconazole 25% EC"],
            "application_method": "Apply Mancozeb @ 2.5 g/L or Propiconazole @ 1 ml/L at first appearance of cigar lesions.",
            "safety_precautions": "Wear protective clothing and rubber boots during application.",
            "pre_harvest_interval_days": 14
        },
        "preventive_measures": [
            "Rotate corn with non-host crops like soybean or pulses.",
            "Shred and bury crop residue immediately after combining to accelerate fungal breakdown."
        ]
    },
    "Corn___healthy": {
        "crop": "Corn (Maize)",
        "crop_hi": "मक्का",
        "crop_as": "মাকৈ",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ मक्का",
        "disease_as": "নিৰোগী মাকৈ",
        "pathogen": "None (Healthy)",
        "symptoms": ["Broad, deep green leaves with strong central midrib and no fungal pustules."],
        "symptoms_hi": ["चौड़ी गहरी हरी पत्तियां, मजबूत तना, कोई दाग नहीं।"],
        "symptoms_as": ["সুস্থ ডাঠ সেউজীয়া বহল পাত, মজবুত কাণ্ড।"],
        "organic_treatment": {"title": "Normal Maintenance", "remedies": ["Apply farmyard manure and bio-potash during knee-high stage."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "Normal fertigation.", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Maintain optimal plant population (60,000 plants/ha) to ensure good aeration."]
    },

    # WHEAT
    "Wheat___Leaf_rust": {
        "crop": "Wheat",
        "crop_hi": "गेहूं",
        "crop_as": "ঘেঁহু",
        "disease": "Leaf Rust (Brown Rust)",
        "disease_hi": "भूरा रतुआ",
        "disease_as": "ঘেঁহুৰ মুগা ৰাষ্ট ৰোগ",
        "pathogen": "Puccinia triticina (Fungus)",
        "symptoms": [
            "Small, round to oval orange-brown powdery pustules scattered randomly on leaf blade.",
            "Unlike stripe rust, pustules do not form straight linear rows.",
            "Causes premature leaf death, reduced spikelet count, and shriveled grains."
        ],
        "symptoms_hi": [
            "पत्तियों पर नारंगी-भूरे रंग के छोटे-छोटे दानेदार फफोले बिखरे हुए।",
            "पत्तियों का जल्दी सूखना और दानों का पतला रह जाना।"
        ],
        "symptoms_as": [
            "পাতৰ ওপৰত কমলা-মুগা বৰণৰ সৰু সৰু ফোহা।",
            "দাগবোৰৰ বাবে পাতবোৰ অকালতে শুকাই যোৱা আৰু ঘেঁহুৰ দানা সৰু হোৱা।"
        ],
        "organic_treatment": {
            "title": "Bio-Control & Organic Sulfur",
            "remedies": [
                "Dust sulfur powder @ 25 kg/ha or spray Wettable Sulfur 80% WP @ 3 g/L.",
                "Foliar spray of fermented buttermilk (chaas) diluted 1:10 with water as a traditional fungal retardant."
            ]
        },
        "chemical_treatment": {
            "title": "Triazole Systemic Fungicides",
            "active_ingredients": ["Propiconazole 25% EC", "Tebuconazole 25% WG"],
            "application_method": "Spray Propiconazole 25% EC (e.g., Tilt) @ 1 ml/L (500 ml in 500 L water/ha) at flag leaf emergence upon detection of first rust pustules.",
            "safety_precautions": "Do not spray within 30 days of harvest. Wear respirator and protective goggles.",
            "pre_harvest_interval_days": 30
        },
        "preventive_measures": [
            "Sow approved rust-resistant varieties (e.g. PBW 550, HD 2967, HD 3086, DBW 187).",
            "Avoid late sowing which exposes crop to high spring temperatures and rust spore showers.",
            "Avoid excessive nitrogenous fertilizer application which fosters dense lush foliage susceptible to rust."
        ]
    },
    "Wheat___healthy": {
        "crop": "Wheat",
        "crop_hi": "गेहूं",
        "crop_as": "ঘেঁহু",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ गेहूं",
        "disease_as": "নিৰোগী ঘেঁহু",
        "pathogen": "None (Healthy)",
        "symptoms": ["Lush linear green leaves, strong flag leaf, absence of pustules."],
        "symptoms_hi": ["स्वस्थ हरी पत्तियां, कोई रतुआ नहीं।"],
        "symptoms_as": ["নিৰোগী সেউজীয়া পাত, কোনো দাগ নাই।"],
        "organic_treatment": {"title": "Routine Care", "remedies": ["Apply foliar zinc sulfate (0.5%) + urea (2%) spray at tillering."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "None", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Ensure timely irrigation at Crown Root Initiation (CRI) and Flowering stages."]
    },

    # APPLE
    "Apple___Black_rot": {
        "crop": "Apple",
        "crop_hi": "सेब",
        "crop_as": "আপেল",
        "disease": "Black Rot (Frog-eye Leaf Spot)",
        "disease_hi": "काला सड़न रोग (मेंढक-आंख धब्बा)",
        "disease_as": "ক'লা পচন ৰোগ",
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "symptoms": [
            "Small purple specks on leaves expanding to 4-5 mm spots with tan brown centers and purple borders ('frog-eye' appearance).",
            "Concentric rings of black pycnidia (spore structures) visible inside older lesions.",
            "Firm, leathery, dark black rot with concentric rings on developing apple fruits."
        ],
        "symptoms_hi": [
            "पत्तियों पर बैंगनी किनारों और भूरे केंद्र वाले 'मेंढक की आंख' जैसे गोल धब्बे।",
            "फलों पर गहरा काला, चमड़े जैसा सूखा सड़ांध।"
        ],
        "symptoms_as": [
            "পাতত বেঙুনীয়া দাঁতি আৰু কজলা মাজভাগৰ ভেঁকুলীৰ চকুৰ দৰে দাগ।",
            "আপেলৰ গাত ক'লা চামৰাৰ দৰে কঠিন পচন।"
        ],
        "organic_treatment": {
            "title": "Sanitation & Bio-Fungicides",
            "remedies": [
                "Prune out all dead wood, cankered twigs, and mummified fruits from previous season before bud break.",
                "Dormant spray of Liquid Lime Sulfur (30 ml/L) before bud swell.",
                "Foliar spray of Serenade ASO (Bacillus amyloliquefaciens @ 5 ml/L) from petal fall."
            ]
        },
        "chemical_treatment": {
            "title": "Broad Spectrum Orchard Fungicides",
            "active_ingredients": ["Captan 50% WP", "Mancozeb 75% WP", "Kresoxim-methyl 44.3% SC"],
            "application_method": "Spray Captan 50% WP @ 2.5 g/L or Kresoxim-methyl @ 0.5 ml/L from petal fall through cover sprays.",
            "safety_precautions": "Do not spray Captan within 14 days of oil sprays to prevent severe leaf phytotoxicity.",
            "pre_harvest_interval_days": 14
        },
        "preventive_measures": [
            "Burn or dispose of all pruned wood promptly outside the orchard perimeter.",
            "Prune canopy for high sunlight penetration and air movement.",
            "Prevent fire blight and winter freeze injuries which act as entry points for Botryosphaeria."
        ]
    },
    "Apple___healthy": {
        "crop": "Apple",
        "crop_hi": "सेब",
        "crop_as": "আপেল",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ सेब",
        "disease_as": "নিৰোগী আপেল",
        "pathogen": "None (Healthy)",
        "symptoms": ["Serrate oval dark green leaves without frog-eye spots, vigorous shoot growth."],
        "symptoms_hi": ["चमकदार गहरे हरे पत्ते, मजबूत शाखाएं।"],
        "symptoms_as": ["সুস্থ সেউজীয়া পাত, কোনো দাগ নাই।"],
        "organic_treatment": {"title": "Seasonal Orchard Care", "remedies": ["Apply composted manure and beneficial mycorrhizal fungi to root zone in autumn."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "None", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Maintain tree ring mulching and regular irrigation during fruit expansion."]
    },

    # GRAPE
    "Grape___Black_rot": {
        "crop": "Grape",
        "crop_hi": "अंगूर",
        "crop_as": "আঙুৰ",
        "disease": "Black Rot",
        "disease_hi": "अंगूर का काला सड़न",
        "disease_as": "আঙুৰৰ ক'লা পচন",
        "pathogen": "Guignardia bidwellii (Fungus)",
        "symptoms": [
            "Circular reddish-brown necrotic spots on upper leaf surfaces surrounded by thin dark line.",
            "Tiny black pimple-like fruiting bodies (pycnidia) arranged in a ring inside lesions.",
            "Infected berries shrivel, blacken, and turn into hard wrinkled mummies adhering to the vine cluster."
        ],
        "symptoms_hi": [
            "पत्तियों पर लाल-भूरे गोल धब्बे जिनके अंदर काले बिंदुओं के छल्ले होते हैं।",
            "अंगूर के दाने काले पड़कर सिकुड़ जाते हैं और सख्त 'ममी' बन जाते हैं।"
        ],
        "symptoms_as": [
            "পাতৰ ওপৰত ৰঙচুৱা-মুগা ঘুৰণীয়া দাগ যাৰ ভিতৰত ক'লা সৰু ফুট থাকে।",
            "আঙুৰবোৰ ক'লা পৰি শুকাই কোচ খাই শুকান গুটি হৈ পৰে।"
        ],
        "organic_treatment": {
            "title": "Sulfur & Copper Protocols",
            "remedies": [
                "Apply Bordeaux mixture 1% or Copper Octanoate (Copper soap) @ 5 ml/L at 10-14 day intervals.",
                "Foliar spray of Potassium Bicarbonate (4 g/L) to alter leaf surface pH and inhibit spore germ tubes."
            ]
        },
        "chemical_treatment": {
            "title": "Systemic Sterol Inhibitor & Strobilurin",
            "active_ingredients": ["Myclobutanil 10% WP", "Azoxystrobin 23% SC", "Mancozeb 75% WP"],
            "application_method": "Spray Myclobutanil @ 0.4 g/L or Azoxystrobin @ 1 ml/L starting at 10 cm shoot growth through 4 weeks post-bloom.",
            "safety_precautions": "Strict adherence to resistance management: alternate strobilurin (FRAC 11) with triazoles (FRAC 3).",
            "pre_harvest_interval_days": 14
        },
        "preventive_measures": [
            "Thoroughly remove all mummified grape clusters from trellis wires during dormant winter pruning.",
            "Canopy management: shoot thinning, leaf pulling around fruit zone to maximize ventilation and rapid drying.",
            "Keep vineyard floor cleanly mown or cultivated to minimize ground spore reservoirs."
        ]
    },
    "Grape___healthy": {
        "crop": "Grape",
        "crop_hi": "अंगूर",
        "crop_as": "আঙুৰ",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ अंगूर",
        "disease_as": "নিৰোগী আঙুৰ",
        "pathogen": "None (Healthy)",
        "symptoms": ["Lush palmate green leaves without chlorotic spots or berry mummies."],
        "symptoms_hi": ["सुंदर स्वस्थ अंगूर के पत्ते, फल सुरक्षित।"],
        "symptoms_as": ["সুস্থ সতেজ আঙুৰৰ পাত।"],
        "organic_treatment": {"title": "Vine Nutrition", "remedies": ["Apply seaweed liquid extract and amino-acid biostimulants during berry set."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "None", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Trellis canopy training for balanced canopy sunlight exposure."]
    },

    # PEPPER (BELL PEPPER / CHILI)
    "Pepper___Bacterial_spot": {
        "crop": "Pepper",
        "crop_hi": "शिमला मिर्च / मिर्च",
        "crop_as": "কেপচিকাম / জলকীয়া",
        "disease": "Bacterial Spot",
        "disease_hi": "जीवाणु धब्बा रोग",
        "disease_as": "বেক্টেৰিয়াজনিত দাগ ৰোগ",
        "pathogen": "Xanthomonas campestris pv. vesicatoria (Bacteria)",
        "symptoms": [
            "Small water-soaked green-yellow spots on leaves turning purplish-brown with yellow borders.",
            "Center of lesions may drop out giving a shot-hole appearance.",
            "Raised, rough, scab-like brown warts on green pepper fruits.",
            "Extensive defoliation exposing peppers to direct sunscald."
        ],
        "symptoms_hi": [
            "पत्तियों पर पानी से भीगे छोटे धब्बे जो बाद में भूरे होकर बीच से छेद बन जाते हैं।",
            "मिर्च के फलों पर खुरदुरे उभरे हुए दाने।",
            "पत्तियों का तेजी से गिरना।"
        ],
        "symptoms_as": [
            "পাতত পানী লগাৰ দৰে সৰু দাগ যিবোৰ ক্ৰমে মুগা হৈ মাজভাগ ফুটা হৈ পৰে।",
            "জলকীয়া বা কেপচিকামৰ ফলৰ ওপৰত খহটা দাগ।",
            "পাতবোৰ সৰি গছজোপা উদং হোৱা।"
        ],
        "organic_treatment": {
            "title": "Copper Bactericides & Bacillus Agents",
            "remedies": [
                "Apply Copper Oxychloride 50% WP @ 2.5 g/L every 7 days during rainy spells.",
                "Foliar spray of Bacillus amyloliquefaciens (5 ml/L) to suppress bacterial colonization.",
                "Spray 2% cow urine filtrate (gomutra) + 5% neem seed kernel extract as a potent botanical antibacterial."
            ]
        },
        "chemical_treatment": {
            "title": "Copper + Antibiotic Mixture",
            "active_ingredients": ["Copper Hydroxide 53.8% DF", "Streptomycin sulphate 90% + Tetracycline 10%"],
            "application_method": "Mix Copper Hydroxide @ 2 g/L + Streptocycline @ 0.1 g/L. Spray thoroughly upon initial detection.",
            "safety_precautions": "Wear face shield and protective coveralls. Do not spray during high temperatures.",
            "pre_harvest_interval_days": 7
        },
        "preventive_measures": [
            "Hot-water seed treatment: soak seed at 50°C for 25 minutes prior to nursery sowing.",
            "Avoid working in pepper fields when foliage is wet with dew or rain to prevent bacterial spread.",
            "Eliminate solanaceous weeds (e.g. nightshades) around field borders."
        ]
    },
    "Pepper___healthy": {
        "crop": "Pepper",
        "crop_hi": "शिमला मिर्च / मिर्च",
        "crop_as": "কেপচিকাম / জলকীয়া",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ मिर्च",
        "disease_as": "নিৰোগী কেপচিকাম / জলকীয়া",
        "pathogen": "None (Healthy)",
        "symptoms": ["Smooth, dark green glossy leaves, robust flowering, uniform fruit setting."],
        "symptoms_hi": ["चमकदार हरे पत्ते, सुंदर फूल और फल।"],
        "symptoms_as": ["চকচকীয়া সেউজীয়া পাত, সুস্থ ফুল আৰু ফল।"],
        "organic_treatment": {"title": "Flower & Fruit Setting Support", "remedies": ["Apply vermiwash or humic acid foliar spray (2 ml/L) during flower bud emergence."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "None", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Maintain uniform soil moisture; avoid water stress during fruit enlargement."]
    },

    # COTTON
    "Cotton___Bacterial_blight": {
        "crop": "Cotton",
        "crop_hi": "कपास",
        "crop_as": "কপাহ",
        "disease": "Bacterial Blight (Blackarm)",
        "disease_hi": "कपास का जीवाणु अंगमारी (काला हाथ)",
        "disease_as": "কপাহৰ বেক্টেৰিয়াজনিত ক'লা কাণ্ড ৰোগ",
        "pathogen": "Xanthomonas citri subsp. malvacearum (Bacteria)",
        "symptoms": [
            "Angular water-soaked spots bounded by leaf veinlets (angular leaf spot).",
            "Dark brown to black lesions spreading along veins and main stem ('blackarm' phase causing lodging).",
            "Water-soaked oily spots on developing bolls causing internal fiber staining and boll rotting."
        ],
        "symptoms_hi": [
            "पत्तियों की नसों के बीच कोणीय पानी जैसे धब्बे।",
            "तने पर काला घाव (ब्लैकआर्म) जिसके कारण पौधे टूट जाते हैं।",
            "कपास के गूलर (बॉल्स) पर काले धब्बे और रुई का सड़ना।"
        ],
        "symptoms_as": [
            "পাতৰ সিৰাৰে আবৃত কণীয়া আকৃতিৰ পানী লগা দাগ।",
            "কাণ্ডত ক'লা দাগ পৰি গছজোপা ভাঙি পৰা ('ব্লেকআৰ্ম')।",
            "কপাহৰ গুটিত পচন ধৰি আঁহ নষ্ট হোৱা।"
        ],
        "organic_treatment": {
            "title": "Bio-Bactericide & Botanical Sprays",
            "remedies": [
                "Seed treatment with Pseudomonas fluorescens @ 10 g/kg seed before sowing.",
                "Foliar spray of 5% Neem oil (Azadirachtin 1500 ppm @ 4 ml/L) + Copper Oxychloride (2 g/L).",
                "Soil incorporation of Trichoderma-enriched FYM at 5 tons/ha."
            ]
        },
        "chemical_treatment": {
            "title": "Bactericide & Copper Hydroxide",
            "active_ingredients": ["Copper Oxychloride 50% WP", "Streptocycline"],
            "application_method": "Spray Copper Oxychloride @ 2.5 g/L + Streptocycline @ 0.1 g/L at the first appearance of angular leaf spots.",
            "safety_precautions": "Ensure protective mask and nitrile gloves. Do not contaminate irrigation drains.",
            "pre_harvest_interval_days": 21
        },
        "preventive_measures": [
            "Acid delinting of cottonseed with concentrated sulfuric acid (100 ml/kg seed) to eliminate seed-coat bacteria.",
            "Crop rotation with sorghum, maize, or legumes.",
            "Collect and burn infected post-harvest cotton stalks; avoid keeping ratoon crops."
        ]
    },
    "Cotton___healthy": {
        "crop": "Cotton",
        "crop_hi": "कपास",
        "crop_as": "কপাহ",
        "disease": "Healthy Leaf",
        "disease_hi": "स्वस्थ कपास",
        "disease_as": "নিৰোগী কপাহ",
        "pathogen": "None (Healthy)",
        "symptoms": ["Lush lobed green leaves without angular spots or black lesions on stems."],
        "symptoms_hi": ["स्वस्थ चौड़े पत्ते, कोई काला दाग नहीं।"],
        "symptoms_as": ["সুস্থ সেউজীয়া পাত, মজবুত কাণ্ড।"],
        "organic_treatment": {"title": "Boll Development Support", "remedies": ["Apply foliar 2% DAP + 1% Potassium Chloride during flowering and boll formation."]},
        "chemical_treatment": {"title": "None", "active_ingredients": ["None"], "application_method": "None", "safety_precautions": "None", "pre_harvest_interval_days": 0},
        "preventive_measures": ["Install pheromone traps (5/acre) to monitor bollworm infestation early."]
    }
}

# Regional Indian Agro-Climatic Advisory Customizer
REGIONAL_ADVISORIES = {
    "assam": {
        "zone_name": "Humid Subtropical Brahmaputra Valley",
        "climate_notes": "High atmospheric humidity (>85%) and frequent rainfall create high fungal/bacterial pressure.",
        "prevention_emphasis": "Raised seedbeds (15 cm high) are essential for root drainage. Apply prophylactic copper and Trichoderma before monsoon surges.",
        "seasonal_care": "During Boro and Sali paddy seasons, monitor closely for Bacterial Leaf Blight and Brown Spot. Ensure ditch drainage in tomato/potato fields to prevent late blight water saturation.",
        "weather_risk_threshold": "High fungal risk when relative humidity > 80% and temp 18-24°C."
    },
    "north_east": {
        "zone_name": "Eastern Himalayan & Sub-Himalayan Zone",
        "climate_notes": "Moderate temperatures, misty mornings, and heavy precipitation.",
        "prevention_emphasis": "Use organic biocides and sulfur dusting. Avoid low-lying waterlogged plots for vegetables.",
        "seasonal_care": "Watch for Early and Late Blight on hillside potato and tomato terraces.",
        "weather_risk_threshold": "Elevated risk under continuous fog or drizzling conditions."
    },
    "punjab_haryana": {
        "zone_name": "Indo-Gangetic North-Western Plains",
        "climate_notes": "Semi-arid with sharp seasonal temperature swings and dry westerly winds.",
        "prevention_emphasis": "Wheat rust spores travel from sub-mountainous zones with winds; survey flag leaves weekly in January-February.",
        "seasonal_care": "Adopt zero-tillage wheat sowing. Rotate paddy-wheat with summer moong to break soil fungal life cycles.",
        "weather_risk_threshold": "Rust flare-ups when daytime temp reaches 20-25°C accompanied by light rain or dew."
    },
    "deccan": {
        "zone_name": "Deccan Plateau & Semi-Arid Central India",
        "climate_notes": "Black cotton soils with high water retention and warm sunny winters.",
        "prevention_emphasis": "Avoid waterlogging in black soils. Spray neem bio-fungicides proactively during October-November transition.",
        "seasonal_care": "Cotton bacterial blight and tomato leaf spot alert during late monsoon showers.",
        "weather_risk_threshold": "High bacterial spot incidence when rain is accompanied by gusty winds."
    },
    "default": {
        "zone_name": "General Indian Agro-Climatic Zone",
        "climate_notes": "Tropical / subtropical conditions with seasonal monsoon cycles.",
        "prevention_emphasis": "Adopt integrated pest management (IPM), soil testing every 2 seasons, and certified seeds.",
        "seasonal_care": "Maintain balanced N-P-K fertilization and regular crop scouting.",
        "weather_risk_threshold": "Monitor crops closely after any rain event exceeding 25 mm."
    }
}

def get_treatment_for_disease(disease_key: str, state: str = "", district: str = "", language: str = "en"):
    """
    Retrieves full treatment plan, translating dynamically or falling back gracefully.
    Customizes with regional advisory if state/district matches.
    """
    # Clean key matching
    matched_entry = AGRONOMIC_KNOWLEDGE_BASE.get(disease_key)
    
    if not matched_entry:
        # Fuzzy match by disease name or crop
        clean_key = disease_key.replace("___", " ").replace("_", " ").lower()
        for k, v in AGRONOMIC_KNOWLEDGE_BASE.items():
            if v["disease"].lower() in clean_key and v["crop"].lower() in clean_key:
                matched_entry = v
                break
                
    if not matched_entry:
        # Generic fallback
        is_healthy = "healthy" in disease_key.lower()
        matched_entry = {
            "crop": disease_key.split("___")[0] if "___" in disease_key else "Crop",
            "crop_hi": "फसल",
            "crop_as": "শস্য",
            "disease": disease_key.split("___")[-1].replace("_", " ") if "___" in disease_key else disease_key,
            "disease_hi": "पादप रोग",
            "disease_as": "উদ্ভিদ ৰোগ",
            "pathogen": "Fungal/Bacterial agent",
            "symptoms": ["Visible discoloration, chlorotic or necrotic spots on leaf lamina."],
            "symptoms_hi": ["पत्तियों पर रंग बदलना या धब्बे दिखाई देना।"],
            "symptoms_as": ["পাতত অস্বাভাৱিক দাগ বা ৰং সলনি হোৱা।"],
            "organic_treatment": {
                "title": "Standard Bio-Foliar Care",
                "remedies": [
                    "Spray Neem Oil 1500 ppm @ 3-5 ml/L water with mild soap.",
                    "Apply Trichoderma viride or Pseudomonas fluorescens @ 5 g/L.",
                    "Remove and safely destroy heavily infected leaves."
                ]
            },
            "chemical_treatment": {
                "title": "Standard Protective Fungicide",
                "active_ingredients": ["Mancozeb 75% WP", "Copper Oxychloride 50% WP"],
                "application_method": "Apply Mancozeb 75% WP @ 2.5 g/L evenly across both leaf surfaces.",
                "safety_precautions": "Always wear mask and gloves. Avoid spraying during windy conditions.",
                "pre_harvest_interval_days": 10
            },
            "preventive_measures": [
                "Practice crop rotation and avoid monoculture.",
                "Ensure adequate plant spacing for aeration.",
                "Avoid overhead irrigation to minimize leaf moisture duration."
            ]
        }

    # Determine regional advisory
    state_lower = (state or "").lower()
    if "assam" in state_lower or "guwahati" in state_lower or "dibrugarh" in state_lower or "jorhat" in state_lower:
        reg_info = REGIONAL_ADVISORIES["assam"]
    elif any(s in state_lower for s in ["meghalaya", "tripura", "manipur", "nagaland", "mizoram", "arunachal", "sikkim"]):
        reg_info = REGIONAL_ADVISORIES["north_east"]
    elif any(s in state_lower for s in ["punjab", "haryana", "rajasthan", "delhi", "uttar pradesh", "up"]):
        reg_info = REGIONAL_ADVISORIES["punjab_haryana"]
    elif any(s in state_lower for s in ["maharashtra", "karnataka", "telangana", "andhra", "gujarat", "madhya pradesh", "mp"]):
        reg_info = REGIONAL_ADVISORIES["deccan"]
    else:
        reg_info = REGIONAL_ADVISORIES["default"]

    # Language customization
    lang = language.lower() if language else "en"
    
    crop_display = matched_entry.get(f"crop_{lang}", matched_entry["crop"]) if lang in ["hi", "as"] else matched_entry["crop"]
    disease_display = matched_entry.get(f"disease_{lang}", matched_entry["disease"]) if lang in ["hi", "as"] else matched_entry["disease"]
    symptoms_list = matched_entry.get(f"symptoms_{lang}", matched_entry["symptoms"]) if lang in ["hi", "as"] else matched_entry["symptoms"]

    return {
        "crop": crop_display,
        "disease": disease_display,
        "raw_disease_key": disease_key,
        "pathogen": matched_entry.get("pathogen", "Plant pathogen"),
        "symptoms": symptoms_list,
        "organic_treatment": matched_entry["organic_treatment"],
        "chemical_treatment": matched_entry["chemical_treatment"],
        "preventive_measures": matched_entry["preventive_measures"],
        "regional_advisory": {
            "zone": reg_info["zone_name"],
            "location_queried": f"{district}, {state}".strip(", ") if (district or state) else "All-India Average",
            "climate_notes": reg_info["climate_notes"],
            "prevention_emphasis": reg_info["prevention_emphasis"],
            "seasonal_care": reg_info["seasonal_care"],
            "weather_risk_threshold": reg_info["weather_risk_threshold"]
        }
    }
