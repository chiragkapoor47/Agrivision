import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Settings, Globe, Cpu, Database, Check } from 'lucide-react';

export default function SettingsPage() {
  const { language, setLanguage, t } = useLanguage();

  const languages = [
    { code: 'en', name: 'English', native: 'English', desc: 'Standard international terminology & scientific names' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी', desc: 'उत्तर और मध्य भारत के किसानों के लिए हिंदी अनुवाद' },
    { code: 'as', name: 'Assamese', native: 'অসমীয়া', desc: 'অসম আৰু উত্তৰ-পূৰ্বাঞ্চলৰ কৃষকসকলৰ বাবে অসমীয়া ভাষা' }
  ];

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <div className="border-b border-stone-200 pb-4">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight flex items-center gap-2">
          <Settings className="w-7 h-7 text-emerald-700" />
          {t('nav.settings', 'Settings & Language Selection')}
        </h1>
        <p className="text-sm text-stone-600 mt-1">
          Customize UI language, regional agricultural profiles, and inspect deep learning model parameters.
        </p>
      </div>

      {/* Language Selection Section */}
      <div className="bg-white rounded-3xl border border-stone-200 shadow-sm p-6 sm:p-8 space-y-4">
        <h2 className="text-base sm:text-lg font-bold text-stone-900 flex items-center gap-2">
          <Globe className="w-5 h-5 text-emerald-600" />
          Application Language (বহুভাষিক সমৰ্থন / बहुभाषी प्रणाली)
        </h2>
        <p className="text-xs text-stone-500">
          Translates navigation, symptoms, organic/chemical treatments, and preventive instructions.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
          {languages.map((l) => (
            <button
              key={l.code}
              onClick={() => setLanguage(l.code)}
              className={`p-4 rounded-2xl border text-left transition-all ${
                language === l.code
                  ? 'border-emerald-600 bg-emerald-50/60 ring-2 ring-emerald-500/20'
                  : 'border-stone-200 hover:border-stone-300 bg-white'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-extrabold text-stone-900 text-base">{l.native}</span>
                {language === l.code && <Check className="w-5 h-5 text-emerald-600" />}
              </div>
              <span className="text-xs font-semibold text-emerald-800 block">{l.name}</span>
              <p className="text-[11px] text-stone-500 mt-2 leading-relaxed">{l.desc}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Model & Architecture Specifications */}
      <div className="bg-white rounded-3xl border border-stone-200 shadow-sm p-6 sm:p-8 space-y-4">
        <h2 className="text-base sm:text-lg font-bold text-stone-900 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-emerald-600" />
          AI & Computer Vision Architecture (TAH-015 Specs)
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs sm:text-sm">
          <div className="p-3.5 rounded-xl bg-stone-50 border border-stone-200">
            <span className="font-bold text-stone-700 block">Classifier Architecture:</span>
            <span className="text-stone-900">MobileNetV2 (Transfer Learning, 33 classes)</span>
          </div>

          <div className="p-3.5 rounded-xl bg-stone-50 border border-stone-200">
            <span className="font-bold text-stone-700 block">Severity Quantification:</span>
            <span className="text-stone-900">OpenCV HSV/LAB Segmentation & Morphological Masking</span>
          </div>

          <div className="p-3.5 rounded-xl bg-stone-50 border border-stone-200">
            <span className="font-bold text-stone-700 block">Confidence Threshold:</span>
            <span className="text-stone-900">40.0% (Uncertainty rejection boundary)</span>
          </div>

          <div className="p-3.5 rounded-xl bg-stone-50 border border-stone-200">
            <span className="font-bold text-stone-700 block">Severity Thresholds:</span>
            <span className="text-stone-900">Low (&lt;20%), Moderate (20-50%), Severe (&gt;50%)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
