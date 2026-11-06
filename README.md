# TAH-015: Precision Agriculture and Crop Disease Predictor

An AI-powered computer vision agricultural diagnostic platform that empowers farmers to detect crop diseases, quantify infection severity through automated leaf lesion segmentation, and receive verified organic and chemical treatment prescriptions tailored to their specific agro-climatic region.

Designed with an ultra-simple, mobile-first interface supporting **English**, **हिन्दी (Hindi)**, and **অসমীয়া (Assamese)**.

---

## 🌾 Key Capabilities

- **Deep Learning Disease Classification**: Transfer-learning with PyTorch **MobileNetV2** supporting 33 disease & healthy classes across 9 major agricultural crops (**Tomato**, **Potato**, **Rice**, **Wheat**, **Corn / Maize**, **Cotton**, **Apple**, **Grape**, **Pepper**).
- **Automated Severity Quantification**: OpenCV HSV & LAB color space segmentation measures precise percentage of affected leaf lamina area, categorized into:
  - 🟢 **Low Severity**: $< 20\%$ affected area.
  - 🟡 **Moderate Severity**: $20\% - 50\%$ affected area.
  - 🔴 **Severe Infestation**: $> 50\%$ affected area.
- **Diagnostic Visual Overlay**: Automatically generates high-contrast lesion overlays highlighting diseased clusters in red/amber and leaf margins in green for visual inspection.
- **Certified Agronomic Prescriptions**:
  - **Organic Treatments**: Cold-pressed Neem oil (1500 ppm), *Trichoderma harzianum*, *Bacillus subtilis*, cow dung supernatant filtrate, and bio-priming.
  - **Chemical Treatments**: Approved active ingredients (Mancozeb 75% WP, Streptocycline, Metalaxyl, Azoxystrobin, Propiconazole), exact application methods, PPE safety warnings, and Pre-Harvest Intervals (PHI in days).
  - **Preventive Cultural Practices**: Drip irrigation, 2-3 year crop rotation, staking, canopy spacing, and post-harvest sanitation.
- **Regional Agro-Climatic Advisory**: Tailored recommendations for Indian agricultural zones (e.g. Humid Subtropical Brahmaputra Valley, Indo-Gangetic Plains, Deccan Plateau).
- **Real-Time Agro-Weather Intelligence**: Analyzes temperature, relative humidity, and wind speed to assess risk indices for late blight, bacterial blight, and rust spores.
- **Farmer Analytics Dashboard**: Real-time KPI cards, health index gauge, and interactive Recharts visualizations for severity distribution and crop diagnostics.
- **Multilingual Support**: Fully localized in **English**, **Hindi (हिन्दी)**, and **Assamese (অসমীয়া)** with a modular dictionary structure.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, Tailwind CSS v4, Lucide Icons, Recharts, React Router v7 |
| **Backend API** | Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, Pydantic v2 |
| **AI / ML & CV** | PyTorch 2.2+, TorchVision, MobileNetV2, OpenCV (cv2), Pillow, NumPy, Scikit-Learn |
| **Database** | SQLite (Default zero-config local), PostgreSQL & Supabase ready |
| **Deployment** | Vercel (Frontend), Render / Docker (Backend), Supabase (Cloud Database) |

---

## 📁 Project Directory Structure

```
crop-disease-predictor/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application entrypoint & demo seeder
│   │   ├── config.py                   # App configuration & environment settings
│   │   ├── database.py                 # SQLAlchemy database session & engine
│   │   ├── models/
│   │   │   ├── user.py                 # Farmer user profile & geolocation model
│   │   │   └── diagnosis.py            # Leaf scan records & treatment storage
│   │   ├── schemas/
│   │   │   ├── user.py                 # Auth schemas
│   │   │   ├── diagnosis.py            # Diagnostic & severity response schemas
│   │   │   └── common.py               # Dashboard & educational resource schemas
│   │   ├── routers/
│   │   │   ├── auth.py                 # /api/auth/register, /login, /me, /profile
│   │   │   ├── predict.py              # /api/predict (Core AI & CV Pipeline)
│   │   │   ├── diagnosis.py            # /api/diagnosis/history, /{id}, delete
│   │   │   ├── agricultural.py         # /api/crops, /api/diseases, /api/treatments, /api/weather
│   │   │   ├── dashboard.py            # /api/dashboard/stats
│   │   │   └── resources.py            # /api/resources
│   │   ├── ml/
│   │   │   ├── inference.py            # PyTorch MobileNetV2 inference engine
│   │   │   ├── severity_analyzer.py    # OpenCV leaf segmentation & lesion overlay generator
│   │   │   └── knowledge_base.py       # Verified agronomic database & regional advisories
│   │   ├── utils/
│   │   │   ├── auth_utils.py           # Bcrypt password hashing & JWT token management
│   │   │   └── image_utils.py          # File integrity check, size validator, and storage
│   │   └── uploads/                    # Stored leaf images & generated visual overlays
│   ├── ml_pipeline/                    # Standalone AI Training & Evaluation Module
│   │   ├── model.py                    # MobileNetV2 with custom classification head
│   │   ├── dataset.py                  # PlantVillage augmentations, transforms & data loaders
│   │   ├── train.py                    # Training script with checkpoints & cosine annealing
│   │   ├── evaluate.py                 # Confusion matrix, classification report & loss curves
│   │   ├── export_model.py             # Export calibrated weights & sample test leaves
│   │   ├── model_weights/              # Saved model weights (.pth) & class mapping
│   │   │   ├── plant_disease_mobilenetv2.pth
│   │   │   └── class_names.json
│   │   └── sample_data/                # Verified genuine leaf test samples
│   ├── test_integration.py             # Automated end-to-end integration test suite
│   ├── database_schema.sql             # PostgreSQL / Supabase schema definition
│   ├── Dockerfile                      # Production container definition
│   ├── render.yaml                     # Render cloud deployment specification
│   ├── requirements.txt                # Python backend dependencies
│   └── .env.example                    # Sample environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx              # Responsive header with language switcher & user menu
│   │   │   ├── Footer.jsx              # Agricultural footer with helpline & disclaimer
│   │   │   ├── CameraCapture.jsx       # Live smartphone camera capture with reticle guide
│   │   │   ├── LanguageSelector.jsx    # Language switcher (EN, HI, AS)
│   │   │   └── SeverityBadge.jsx       # Visual severity indicator
│   │   ├── context/
│   │   │   ├── AuthContext.jsx         # Farmer authentication context
│   │   │   └── LanguageContext.jsx     # Deep translation context provider
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx         # Hero, 3-step guide, weather risk, crop showcase
│   │   │   ├── DiseaseDetectionPage.jsx# Leaf upload, camera capture, manual crop selector
│   │   │   ├── DiagnosisResultPage.jsx # Original vs overlay, severity %, symptoms, treatments
│   │   │   ├── DashboardPage.jsx       # KPI metrics, Recharts charts, recent scans
│   │   │   ├── HistoryPage.jsx         # Past diagnoses table/cards with filters and delete
│   │   │   ├── TreatmentsPage.jsx      # Treatment reference directory
│   │   │   ├── EducationalResourcesPage.jsx # Farmer learning center & step-by-step guides
│   │   │   ├── ProfilePage.jsx         # Farmer location & farm size configuration
│   │   │   ├── SettingsPage.jsx        # Language preferences & AI model specs
│   │   │   ├── LoginPage.jsx           # Farmer sign in with 1-click demo login
│   │   │   └── RegisterPage.jsx        # Farmer account registration
│   │   ├── services/
│   │   │   └── api.js                  # Frontend API client
│   │   ├── translations/               # Translation dictionaries
│   │   │   ├── en.json                 # English
│   │   │   ├── hi.json                 # Hindi
│   │   │   └── as.json                 # Assamese
│   │   ├── App.jsx                     # Router & App layout
│   │   └── index.css                   # Tailwind v4 styles
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json                     # Vercel deployment configuration
└── README.md
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### Step 1: Clone or Set Active Workspace
Ensure your active workspace is set to this project directory:
```bash
cd "C:\Users\12chi\.gemini\antigravity\scratch\crop-disease-predictor"
```

### Step 2: Backend Setup
```bash
cd backend

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated integration tests to verify setup
python test_integration.py

# Start the FastAPI backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API is now live at:
- **API Server**: `http://localhost:8000`
- **Swagger Interactive API Documentation**: `http://localhost:8000/api/docs`
- **ReDoc Documentation**: `http://localhost:8000/api/redoc`

### Step 3: Frontend Setup
In a new terminal:
```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```
The frontend is now accessible at `http://localhost:3000` (or the port Vite indicates).

---

## 🧠 Model Training & Dataset Pipeline

### 1. Dataset Acquisition
1. Download the public **PlantVillage Dataset** from [Kaggle](https://www.kaggle.com/datasets/emmarex/plantdisease) or official academic mirrors.
2. Extract the dataset into a folder structured as:
   ```
   dataset/
   ├── Apple___Apple_scab/
   ├── Tomato___Early_blight/
   ├── Potato___Late_blight/
   └── ...
   ```

### 2. Train MobileNetV2 with Transfer Learning
Run the training script with cosine annealing learning rate scheduler and label smoothing:
```bash
cd backend
python ml_pipeline/train.py --data_dir "/path/to/dataset" --epochs 15 --batch_size 32 --lr 1e-4 --output "ml_pipeline/model_weights/plant_disease_mobilenetv2.pth"
```

### 3. Model Evaluation & Confusion Matrix
Generate accuracy/loss curves and the multi-class confusion matrix:
```bash
python ml_pipeline/evaluate.py --model "ml_pipeline/model_weights/plant_disease_mobilenetv2.pth" --data_dir "/path/to/dataset" --output_dir "ml_pipeline/model_weights"
```
Outputs generated:
- `accuracy_loss_curves.png`
- `confusion_matrix.png`
- `evaluation_report.json`

---

## 🔬 Computer Vision Disease Severity Assessment

The platform calculates infection severity mathematically through an automated OpenCV segmentation algorithm:
1. **Color Space Transformation**: Converts input image to **HSV** (Hue, Saturation, Value) and **LAB** color spaces.
2. **Leaf Lamina Segmentation**: Masks healthy chlorophyll green $[20 \le H \le 102]$ along with chlorotic/senescent leaf boundaries, followed by morphological closing to construct a solid leaf mask.
3. **Lesion Extraction**: Identifies necrotic spots (brown/rust hue $5 \le H \le 24$ or $V < 75$), yellow chlorotic halos, and powdery mildew patches strictly constrained inside the leaf boundary.
4. **Severity Formula**:
   $$\text{Severity \%} = \left(\frac{\text{Lesion Pixels}}{\text{Total Leaf Pixels}}\right) \times 100$$
5. **Visual Diagnostic Overlay**: Creates a high-contrast semi-transparent red/amber mask over lesions and outlines leaf boundaries in emerald green, saving the result for farmer inspection.
6. **Confidence Threshold Rejection**: Predictions with $< 40\%$ confidence are flagged as `Uncertain/Ambiguous`, prompting the farmer to retake the photo with optimal focus and lighting.

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and diagnostics |
| `POST` | `/api/auth/register` | Register farmer profile with farm location & preferred language |
| `POST` | `/api/auth/login` | Authenticate farmer and return signed JWT |
| `GET` | `/api/auth/me` | Retrieve profile of authenticated farmer |
| `PUT` | `/api/auth/profile` | Update farm details and regional language |
| `POST` | `/api/predict` | **Core AI Diagnostic**: accepts leaf image, returns classification, severity %, and treatments |
| `GET` | `/api/diagnosis/history` | List previous diagnoses with crop & severity filtering |
| `GET` | `/api/diagnosis/{id}` | Detailed diagnosis report with visual lesion overlay |
| `DELETE`| `/api/diagnosis/{id}` | Delete previous diagnosis record and associated files |
| `GET` | `/api/crops` | List of supported crops with growing guidelines |
| `GET` | `/api/diseases` | List of supported plant diseases and typical symptoms |
| `GET` | `/api/treatments` | Query scientific treatments by crop/disease |
| `GET` | `/api/weather` | Localized agricultural weather risk intelligence |
| `GET` | `/api/dashboard/stats` | Aggregated metrics & Recharts telemetry data |
| `GET` | `/api/resources` | Farmer educational guides in EN, HI, AS |

---

## ☁️ Production Deployment

### Frontend (Vercel)
The included `frontend/vercel.json` automatically configures Vite single-page application routing and API reverse-proxying.
1. Connect repository to [Vercel](https://vercel.com).
2. Set Framework Preset: **Vite**.
3. Set Root Directory: `frontend`.
4. Deploy!

### Backend (Render / Docker)
The included `backend/render.yaml` and `backend/Dockerfile` enable zero-friction deployment.
1. Create a Web Service on [Render](https://render.com).
2. Set Root Directory: `backend`.
3. Set Environment to **Python** or **Docker**.
4. Set Build Command: `pip install -r requirements.txt`.
5. Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
6. Add Environment Variable `DATABASE_URL` pointing to your managed Supabase PostgreSQL instance.

---

## ⚖️ Field Diagnostic Disclaimer
*AgriVision AI is an assistive decision-support tool. Predictions are generated via computer vision neural feature extraction and should be cross-verified with your local Krishi Vigyan Kendra (KVK) extension officer or agronomist for critical commercial field interventions. Always follow Central Insecticides Board & Registration Committee (CIBRC) pesticide labels and safety guidelines.*
