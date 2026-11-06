import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate, Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { diagnosisApi } from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import { 
  Sparkles, ShieldCheck, AlertTriangle, AlertCircle, Droplets, 
  Leaf, FlaskConical, Calendar, MapPin, Printer, ArrowLeft, 
  RotateCcw, Eye, Layers, Clock, ShieldAlert, CheckCircle2
} from 'lucide-react';

export default function DiagnosisResultPage() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const { t, language } = useLanguage();

  const [diagnosis, setDiagnosis] = useState(location.state?.diagnosisResult || null);
  const [loading, setLoading] = useState(!diagnosis);
  const [error, setError] = useState(null);
  const [showOverlay, setShowOverlay] = useState(true);
  const [activeTab, setActiveTab] = useState('organic'); // 'organic' | 'chemical' | 'preventive'

  useEffect(() => {
    if (!diagnosis && id) {
      async function fetchRecord() {
        try {
          setLoading(true);
          const data = await diagnosisApi.getDetail(id);
          setDiagnosis(data);
        } catch (err) {
          setError(err.message || 'Could not load diagnosis report.');
        } finally {
          setLoading(false);
        }
      }
      fetchRecord();
    }
  }, [id, diagnosis]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="w-16 h-16 rounded-full border-4 border-emerald-200 border-t-emerald-600 animate-spin mx-auto mb-4"></div>
        <h3 className="text-lg font-bold text-stone-800">Retrieving Diagnostic Prescription...</h3>
      </div>
    );
  }

  if (error || !diagnosis) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 text-center space-y-4">
        <AlertCircle className="w-16 h-16 text-red-500 mx-auto" />
        <h2 className="text-xl font-bold text-stone-900">Diagnosis Report Unavailable</h2>
        <p className="text-sm text-stone-600">{error || 'Record could not be loaded.'}</p>
        <Link
          to="/detect"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-600 text-white font-semibold"
        >
          <RotateCcw className="w-4 h-4" /> Scan a New Leaf
        </Link>
      </div>
    );
  }

  const isHealthy = diagnosis.is_healthy;
  const severity = diagnosis.severity;
  const organic = diagnosis.organic_treatment;
  const chemical = diagnosis.chemical_treatment;
  const preventive = diagnosis.preventive_measures || [];
  const regional = diagnosis.regional_advisory;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Navigation & Action Buttons */}
      <div className="flex flex-wrap items-center justify-between gap-4 print:hidden">
        <Link
          to="/detect"
          className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-800 hover:text-emerald-950"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{t('results.btn_diagnose_another', 'Diagnose Another Leaf')}</span>
        </Link>

        <div className="flex items-center gap-2">
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white border border-stone-300 hover:bg-stone-50 text-stone-700 text-sm font-semibold transition-colors shadow-2xs"
          >
            <Printer className="w-4 h-4 text-stone-600" />
            <span>{t('results.btn_print', 'Print Prescription')}</span>
          </button>
          <Link
            to="/history"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-sm font-semibold transition-colors shadow-2xs"
          >
            {t('results.btn_view_history', 'View in History')}
          </Link>
        </div>
      </div>

      {/* Main Diagnostic Header Card */}
      <div className={`p-6 sm:p-8 rounded-3xl border shadow-md relative overflow-hidden ${
        isHealthy ? 'bg-gradient-to-br from-emerald-50 to-white border-emerald-200' : 'bg-white border-stone-200'
      }`}>
        <div className="flex flex-col md:flex-row items-start justify-between gap-6">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs uppercase font-extrabold tracking-wider bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">
                {diagnosis.crop}
              </span>
              <SeverityBadge level={severity.level} percentage={severity.affected_area_percentage} size="md" />
              {diagnosis.is_uncertain && (
                <span className="text-xs font-semibold bg-amber-100 text-amber-800 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" /> Low Confidence Alert
                </span>
              )}
            </div>

            <h1 className="text-3xl sm:text-4xl font-extrabold text-stone-900 tracking-tight">
              {diagnosis.disease}
            </h1>
            {diagnosis.pathogen && (
              <p className="text-sm font-medium text-emerald-800 italic">
                Pathogen: {diagnosis.pathogen}
              </p>
            )}
          </div>

          {/* Confidence Meter Badge */}
          <div className="bg-stone-50 p-4 rounded-2xl border border-stone-200/80 text-center shrink-0 min-w-[170px]">
            <div className="text-xs font-semibold text-stone-500 uppercase tracking-wider mb-1">
              {t('results.confidence', 'AI Confidence')}
            </div>
            <div className="text-3xl font-black text-emerald-700">
              {diagnosis.confidence_score}%
            </div>
            <div className="text-[11px] text-stone-500 mt-1">
              {diagnosis.confidence_status}
            </div>
          </div>
        </div>

        {/* Severity Explanation Banner */}
        <div className="mt-6 p-4 rounded-2xl bg-stone-50 border border-stone-200/70 flex items-start gap-3">
          <div className="p-2 rounded-xl bg-white shadow-2xs text-emerald-700 mt-0.5">
            <Activity className="w-5 h-5" />
          </div>
          <div className="text-xs sm:text-sm text-stone-700">
            <span className="font-bold text-stone-900 block mb-0.5">
              Severity Quantification: {severity.level} ({severity.affected_area_percentage}% Leaf Area Affected)
            </span>
            <p className="leading-relaxed">{severity.explanation}</p>
          </div>
        </div>
      </div>

      {/* Visual Image Inspection Grid: Original vs. Severity Mask Overlay */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Original Captured Image */}
        <div className="bg-white rounded-3xl p-5 border border-stone-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-sm text-stone-800 flex items-center gap-2">
              <Eye className="w-4 h-4 text-emerald-600" />
              {t('results.original_image', 'Captured Leaf Photograph')}
            </h3>
            <span className="text-xs text-stone-500">Camera / Gallery Input</span>
          </div>
          <div className="relative aspect-4/3 rounded-2xl overflow-hidden bg-stone-950 border border-stone-200">
            <img
              src={diagnosis.image_url}
              alt="Original leaf input"
              className="w-full h-full object-contain"
            />
          </div>
        </div>

        {/* Computer Vision Severity Mask Overlay */}
        <div className="bg-white rounded-3xl p-5 border border-stone-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-sm text-stone-800 flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-600" />
              {t('results.overlay_image', 'OpenCV Lesion Mask Overlay')}
            </h3>
            <span className="text-xs bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded-md">
              {severity.affected_area_percentage}% Necrotic Tissue
            </span>
          </div>
          <div className="relative aspect-4/3 rounded-2xl overflow-hidden bg-stone-950 border border-stone-200">
            <img
              src={diagnosis.overlay_url || diagnosis.image_url}
              alt="Computer vision lesion overlay"
              className="w-full h-full object-contain"
            />
            <div className="absolute bottom-2 left-2 right-2 bg-stone-900/80 backdrop-blur-xs text-white text-[11px] p-2 rounded-xl flex items-center justify-between">
              <span>Red highlights indicate active fungal/bacterial lesions</span>
              <span className="font-semibold text-emerald-400">Green: Leaf Margin</span>
            </div>
          </div>
        </div>
      </div>

      {/* Symptoms Identification */}
      {diagnosis.symptoms && diagnosis.symptoms.length > 0 && (
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-stone-200 shadow-sm space-y-3">
          <h3 className="font-bold text-base sm:text-lg text-stone-900 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            {t('results.symptoms_title', 'Identified Field Symptoms')}
          </h3>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-2.5 pt-2">
            {diagnosis.symptoms.map((symptom, idx) => (
              <li key={idx} className="flex items-start gap-2.5 p-3 rounded-xl bg-stone-50 border border-stone-100 text-xs sm:text-sm text-stone-700">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-2 shrink-0"></span>
                <span>{symptom}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Scientific Treatments & Prescription Tabs */}
      <div className="bg-white rounded-3xl border border-stone-200 shadow-md overflow-hidden">
        {/* Treatment Tabs Header */}
        <div className="flex border-b border-stone-200 bg-stone-50/70 p-2 gap-2">
          <button
            type="button"
            onClick={() => setActiveTab('organic')}
            className={`flex-1 py-3 px-4 rounded-2xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all ${
              activeTab === 'organic'
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/20'
                : 'text-stone-600 hover:bg-stone-100'
            }`}
          >
            <Leaf className="w-4 h-4" />
            <span>{t('results.organic_title', 'Organic Treatments')}</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('chemical')}
            className={`flex-1 py-3 px-4 rounded-2xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all ${
              activeTab === 'chemical'
                ? 'bg-amber-600 text-white shadow-md shadow-amber-600/20'
                : 'text-stone-600 hover:bg-stone-100'
            }`}
          >
            <FlaskConical className="w-4 h-4" />
            <span>{t('results.chemical_title', 'Chemical Treatments')}</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('preventive')}
            className={`flex-1 py-3 px-4 rounded-2xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 transition-all ${
              activeTab === 'preventive'
                ? 'bg-sky-600 text-white shadow-md shadow-sky-600/20'
                : 'text-stone-600 hover:bg-stone-100'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{t('results.preventive_title', 'Preventive Practices')}</span>
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-6 sm:p-8">
          {activeTab === 'organic' && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-emerald-100">
                <Leaf className="w-5 h-5 text-emerald-600" />
                <h4 className="font-bold text-base text-stone-900">{organic.title}</h4>
              </div>
              <p className="text-xs text-stone-500">
                Bio-pesticides and natural formulations safe for soil microbiology and beneficial pollinators.
              </p>
              <div className="grid grid-cols-1 gap-3 pt-2">
                {organic.remedies.map((remedy, i) => (
                  <div key={i} className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-100/80 flex items-start gap-3">
                    <span className="w-6 h-6 rounded-lg bg-emerald-200 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0">
                      {i + 1}
                    </span>
                    <p className="text-xs sm:text-sm text-stone-800 leading-relaxed font-medium">{remedy}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'chemical' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between pb-2 border-b border-amber-100">
                <div className="flex items-center gap-2">
                  <FlaskConical className="w-5 h-5 text-amber-600" />
                  <h4 className="font-bold text-base text-stone-900">{chemical.title}</h4>
                </div>
                {chemical.pre_harvest_interval_days > 0 && (
                  <span className="text-xs bg-amber-100 text-amber-900 font-extrabold px-3 py-1 rounded-full border border-amber-300 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5" />
                    PHI: {chemical.pre_harvest_interval_days} {t('results.days', 'days')}
                  </span>
                )}
              </div>

              {/* Active Ingredients Badges */}
              <div>
                <label className="block text-xs font-bold text-stone-500 uppercase tracking-wider mb-2">
                  {t('results.active_ingredients', 'Approved Active Ingredients')}
                </label>
                <div className="flex flex-wrap gap-2">
                  {chemical.active_ingredients.map((ing, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 font-bold text-xs sm:text-sm">
                      {ing}
                    </span>
                  ))}
                </div>
              </div>

              {/* Application Method */}
              <div className="p-4 rounded-2xl bg-stone-50 border border-stone-200">
                <h5 className="text-xs font-bold text-stone-700 uppercase tracking-wider mb-1">
                  {t('results.application_method', 'Recommended Application Method')}
                </h5>
                <p className="text-xs sm:text-sm text-stone-800 leading-relaxed">{chemical.application_method}</p>
              </div>

              {/* Safety Precautions & PPE */}
              <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-900">
                <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider mb-1">
                  <ShieldAlert className="w-4 h-4 text-red-600" />
                  <span>{t('results.safety_precautions', 'Mandatory Safety Precautions & PPE')}</span>
                </div>
                <p className="text-xs sm:text-sm leading-relaxed">{chemical.safety_precautions}</p>
              </div>
            </div>
          )}

          {activeTab === 'preventive' && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-sky-100">
                <ShieldCheck className="w-5 h-5 text-sky-600" />
                <h4 className="font-bold text-base text-stone-900">
                  {t('results.preventive_title', 'Preventive Cultural Practices')}
                </h4>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                {preventive.map((prev, i) => (
                  <div key={i} className="p-4 rounded-2xl bg-sky-50/50 border border-sky-100 flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-sky-600 shrink-0 mt-0.5" />
                    <p className="text-xs sm:text-sm text-stone-800 leading-relaxed font-medium">{prev}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Regional Agro-Climatic Advisory */}
      {regional && (
        <div className="bg-gradient-to-r from-emerald-900 to-teal-950 text-white rounded-3xl p-6 sm:p-7 shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-emerald-800 pb-3">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-emerald-400" />
              <h3 className="font-bold text-base text-white">
                {t('results.regional_title', 'Regional Agricultural Advisory')}
              </h3>
            </div>
            <span className="text-xs bg-emerald-800 text-emerald-200 font-semibold px-3 py-1 rounded-full border border-emerald-700">
              {regional.zone}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs sm:text-sm">
            <div className="bg-emerald-900/40 p-4 rounded-2xl border border-emerald-800/80">
              <span className="font-bold text-emerald-300 block mb-1">Local Microclimate Context:</span>
              <p className="text-emerald-100/90 leading-relaxed">{regional.climate_notes}</p>
            </div>
            <div className="bg-emerald-900/40 p-4 rounded-2xl border border-emerald-800/80">
              <span className="font-bold text-emerald-300 block mb-1">Seasonal Crop Care Advisory:</span>
              <p className="text-emerald-100/90 leading-relaxed">{regional.seasonal_care}</p>
            </div>
          </div>
        </div>
      )}

      {/* Agronomic Disclaimer */}
      <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/80 text-amber-900 text-xs flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          {diagnosis.disclaimer}
        </p>
      </div>
    </div>
  );
}
