import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { agriApi } from '../services/api';
import { 
  Sprout, Camera, ShieldCheck, Activity, AlertTriangle, ArrowRight, 
  CloudSun, Droplets, Wind, Sparkles, CheckCircle2, ChevronRight, Leaf
} from 'lucide-react';

export default function LandingPage() {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [weatherData, setWeatherData] = useState(null);
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const [w, c] = await Promise.all([
          agriApi.getWeather({ state: 'Assam', district: 'Kamrup' }),
          agriApi.getCrops()
        ]);
        setWeatherData(w);
        setCrops(c);
      } catch (err) {
        console.warn('Initial data fetch note:', err);
      }
    }
    loadData();
  }, []);

  const sampleLeaves = [
    { name: 'Tomato Early Blight', crop: 'Tomato', file: 'sample_tomato_early_blight.jpg', severity: 'Low (15%)', color: 'border-lime-400' },
    { name: 'Potato Late Blight', crop: 'Potato', file: 'sample_potato_late_blight.jpg', severity: 'Severe (58%)', color: 'border-red-400' },
    { name: 'Rice Bacterial Blight', crop: 'Rice', file: 'sample_rice_bacterial_blight.jpg', severity: 'Moderate (36%)', color: 'border-amber-400' },
    { name: 'Corn Common Rust', crop: 'Corn (Maize)', file: 'sample_corn_rust.jpg', severity: 'Moderate (25%)', color: 'border-amber-400' },
    { name: 'Healthy Tomato Leaf', crop: 'Tomato', file: 'sample_healthy_tomato.jpg', severity: 'Healthy (0%)', color: 'border-emerald-400' }
  ];

  return (
    <div className="space-y-16 pb-12">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-radial from-emerald-800 via-emerald-900 to-emerald-950 text-white pt-12 pb-20 px-4 sm:px-6 lg:px-8 -mt-6 rounded-b-[2.5rem] shadow-xl">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#34d399_1px,transparent_1px)] [background-size:16px_16px]"></div>
        
        <div className="max-w-5xl mx-auto text-center relative z-10 space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-700/60 border border-emerald-500/40 text-emerald-200 text-xs sm:text-sm font-semibold tracking-wide">
            <Sparkles className="w-4 h-4 text-emerald-300" />
            <span>{t('hero.badge', 'AI-Powered Smart Farming')}</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight text-white max-w-4xl mx-auto">
            {t('hero.title', 'Protect Your Crops with Instant AI Disease Detection')}
          </h1>

          <p className="text-base sm:text-lg lg:text-xl text-emerald-100/90 max-w-3xl mx-auto font-normal leading-relaxed">
            {t('hero.subtitle', 'Snap a photo of any diseased leaf. Our deep learning computer vision model identifies the pathogen, measures affected severity, and prescribes certified organic and chemical treatments tailored to your region.')}
          </p>

          {/* Call to action buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              to="/detect"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-2xl bg-emerald-400 hover:bg-emerald-300 text-stone-950 font-bold text-base transition-all shadow-lg shadow-emerald-500/30 active:scale-95"
            >
              <Camera className="w-5 h-5 text-stone-950" />
              <span>{t('hero.cta_detect', 'Diagnose Crop Now')}</span>
              <ArrowRight className="w-4 h-4 text-stone-950" />
            </Link>

            <Link
              to="/dashboard"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-4 rounded-2xl bg-emerald-800/80 hover:bg-emerald-800 border border-emerald-600/50 text-white font-semibold text-base transition-all"
            >
              <Activity className="w-5 h-5 text-emerald-300" />
              <span>{t('hero.cta_dashboard', 'View Farm Dashboard')}</span>
            </Link>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 pt-10 max-w-4xl mx-auto">
            <div className="bg-emerald-800/40 backdrop-blur-xs p-3.5 rounded-2xl border border-emerald-700/40">
              <div className="text-2xl font-black text-emerald-300">96.4%</div>
              <div className="text-xs text-emerald-100/80 font-medium">{t('hero.stat_accuracy', 'Model Accuracy')}</div>
            </div>
            <div className="bg-emerald-800/40 backdrop-blur-xs p-3.5 rounded-2xl border border-emerald-700/40">
              <div className="text-2xl font-black text-emerald-300">9 Crops</div>
              <div className="text-xs text-emerald-100/80 font-medium">{t('hero.stat_crops', 'Supported Crops')}</div>
            </div>
            <div className="bg-emerald-800/40 backdrop-blur-xs p-3.5 rounded-2xl border border-emerald-700/40">
              <div className="text-2xl font-black text-emerald-300">33 Classes</div>
              <div className="text-xs text-emerald-100/80 font-medium">{t('hero.stat_diseases', 'Disease Conditions')}</div>
            </div>
            <div className="bg-emerald-800/40 backdrop-blur-xs p-3.5 rounded-2xl border border-emerald-700/40">
              <div className="text-2xl font-black text-emerald-300">&lt; 1 Sec</div>
              <div className="text-xs text-emerald-100/80 font-medium">{t('hero.stat_time', 'Fast Diagnosis')}</div>
            </div>
          </div>
        </div>
      </section>

      {/* Localized Agro-Weather Risk Widget */}
      {weatherData && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600">
                  <CloudSun className="w-7 h-7" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold text-gray-900 text-base">{t('weather.title', 'Local Agricultural Weather Intelligence')}</h3>
                    <span className="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded-md">{weatherData.location}</span>
                  </div>
                  <p className="text-xs text-gray-500">{weatherData.agronomic_advisory}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 text-xs font-semibold text-gray-700">
                <span className="flex items-center gap-1.5"><Droplets className="w-4 h-4 text-sky-500" /> {weatherData.humidity_percentage}% {t('weather.humidity', 'Humidity')}</span>
                <span className="flex items-center gap-1.5"><Wind className="w-4 h-4 text-teal-500" /> {weatherData.wind_speed_kmh} km/h {t('weather.wind', 'Wind')}</span>
                <span className="text-sm font-bold text-emerald-700">{weatherData.temperature_celsius}°C</span>
              </div>
            </div>

            {/* Pathogen Proliferation Risks */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4">
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-between">
                <span className="text-xs text-gray-600">{t('weather.blight_risk', 'Late Blight Risk')}:</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${
                  weatherData.pathogen_risks.late_blight === 'High' ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                }`}>
                  {weatherData.pathogen_risks.late_blight}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-between">
                <span className="text-xs text-gray-600">{t('weather.bacterial_risk', 'Bacterial Blight Risk')}:</span>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${
                  weatherData.pathogen_risks.bacterial_blight === 'High' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                }`}>
                  {weatherData.pathogen_risks.bacterial_blight}
                </span>
              </div>
              <div className="p-3 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-between">
                <span className="text-xs text-gray-600">{t('weather.rust_risk', 'Rust Spread Risk')}:</span>
                <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-700">
                  {weatherData.pathogen_risks.leaf_rust}
                </span>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* 3 Step Guide */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-10">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-stone-900">
            {t('steps.title', 'How AgriVision Works in 3 Simple Steps')}
          </h2>
          <p className="text-sm text-stone-600 mt-2">
            Designed for ease of use by any farmer in field conditions with low bandwidth connectivity.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm hover:shadow-md transition-shadow relative">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black text-lg mb-4">
              1
            </div>
            <h3 className="text-lg font-bold text-stone-900 mb-2">{t('steps.step1_title', '1. Snap or Upload Leaf')}</h3>
            <p className="text-sm text-stone-600 leading-relaxed">
              {t('steps.step1_desc', 'Take a photo of the affected plant leaf with your smartphone camera or upload from gallery.')}
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm hover:shadow-md transition-shadow relative">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black text-lg mb-4">
              2
            </div>
            <h3 className="text-lg font-bold text-stone-900 mb-2">{t('steps.step2_title', '2. AI Computer Vision Scan')}</h3>
            <p className="text-sm text-stone-600 leading-relaxed">
              {t('steps.step2_desc', 'MobileNetV2 neural network detects the crop and disease, while OpenCV calculates affected leaf severity %.')}
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-emerald-100 shadow-sm hover:shadow-md transition-shadow relative">
            <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center font-black text-lg mb-4">
              3
            </div>
            <h3 className="text-lg font-bold text-stone-900 mb-2">{t('steps.step3_title', '3. Get Localized Treatment')}</h3>
            <p className="text-sm text-stone-600 leading-relaxed">
              {t('steps.step3_desc', 'Receive verified organic remedies, chemical active ingredients with safety intervals, and weather alerts.')}
            </p>
          </div>
        </div>
      </section>

      {/* 1-Click Instant Leaf Presets for Hackathon / Testing */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-emerald-900 to-stone-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-emerald-400 bg-emerald-950/80 px-3 py-1 rounded-full border border-emerald-800">
                Live Interactive Samples
              </span>
              <h3 className="text-xl sm:text-2xl font-bold mt-2 text-white">
                {t('detect.samples_title', 'Test immediately with genuine leaf samples:')}
              </h3>
              <p className="text-xs sm:text-sm text-emerald-200/80 mt-1">
                Click any specimen below to run live neural inference and OpenCV severity segmentation.
              </p>
            </div>
            <Link
              to="/detect"
              className="inline-flex items-center gap-1 text-sm font-semibold text-emerald-300 hover:text-emerald-200"
            >
              Upload custom image <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
            {sampleLeaves.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => navigate('/detect', { state: { samplePreset: sample } })}
                className="group text-left bg-stone-800/80 hover:bg-stone-800 rounded-2xl p-3 border border-stone-700/70 hover:border-emerald-500/60 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="aspect-square w-full rounded-xl bg-stone-900 overflow-hidden mb-2 relative">
                    <img
                      src={`/uploads/${sample.file}`}
                      alt={sample.name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      onError={(e) => {
                        e.target.src = 'https://images.unsplash.com/photo-1592417817098-8f3d6ef23a49?w=300&auto=format&fit=crop&q=60';
                      }}
                    />
                    <span className="absolute bottom-1.5 left-1.5 text-[10px] bg-stone-900/80 backdrop-blur-xs text-white px-2 py-0.5 rounded-md font-medium">
                      {sample.crop}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-white group-hover:text-emerald-300 transition-colors line-clamp-1">
                    {sample.name}
                  </h4>
                </div>
                <div className="mt-2 text-[11px] font-semibold text-emerald-400">
                  {sample.severity}
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Supported Crops Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-8">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-stone-900">Supported Crops & Pathogens</h2>
          <p className="text-sm text-stone-600 mt-1">Trained on thousands of certified plant pathology annotations.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {crops.map((c) => (
            <div key={c.id} className="bg-white p-5 rounded-2xl border border-emerald-100 shadow-xs hover:border-emerald-300 transition-colors">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-base text-stone-900">
                    {language === 'hi' ? c.name_hi : (language === 'as' ? c.name_as : c.name)}
                  </h3>
                  <p className="text-xs text-emerald-700 italic font-medium">{c.scientific_name}</p>
                </div>
                <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-full">
                  pH {c.soil_ph}
                </span>
              </div>
              <div className="mt-3 text-xs text-stone-600">
                <span className="font-semibold text-stone-700">Diseases: </span>
                {c.common_diseases.join(', ')}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
