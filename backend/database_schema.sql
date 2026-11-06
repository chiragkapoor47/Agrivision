-- ==============================================================
-- TAH-015: Precision Agriculture and Crop Disease Predictor
-- Database Schema for PostgreSQL / Supabase
-- ==============================================================

-- 1. Farmers / Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    phone VARCHAR(25),
    state VARCHAR(100) DEFAULT 'Assam',
    district VARCHAR(100) DEFAULT 'Kamrup',
    village VARCHAR(100) DEFAULT 'Azara',
    farm_size_acres REAL DEFAULT 2.5,
    preferred_language VARCHAR(10) DEFAULT 'en',
    primary_crops VARCHAR(255) DEFAULT 'Tomato, Rice, Potato',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. Leaf Diagnosis Records Table
CREATE TABLE IF NOT EXISTS diagnosis_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    crop VARCHAR(80) NOT NULL,
    disease VARCHAR(120) NOT NULL,
    raw_class VARCHAR(120),
    pathogen VARCHAR(150),
    confidence_score REAL NOT NULL,
    severity_level VARCHAR(30) NOT NULL, -- 'Low', 'Moderate', 'Severe', 'None / Healthy'
    affected_area_percentage REAL DEFAULT 0.0,
    is_healthy BOOLEAN DEFAULT FALSE,
    is_uncertain BOOLEAN DEFAULT FALSE,
    image_path VARCHAR(255) NOT NULL,
    overlay_path VARCHAR(255),
    state VARCHAR(100),
    district VARCHAR(100),
    village VARCHAR(100),
    symptoms_json TEXT,
    organic_treatment_json TEXT,
    chemical_treatment_json TEXT,
    preventive_measures_json TEXT,
    regional_advisory_json TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_diagnosis_crop ON diagnosis_records(crop);
CREATE INDEX IF NOT EXISTS idx_diagnosis_disease ON diagnosis_records(disease);
CREATE INDEX IF NOT EXISTS idx_diagnosis_user_id ON diagnosis_records(user_id);
CREATE INDEX IF NOT EXISTS idx_diagnosis_created_at ON diagnosis_records(created_at DESC);
