import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, PhoneCall, AlertTriangle, ShieldCheck, Heart } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export default function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-emerald-950 text-emerald-100/80 border-t border-emerald-900 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          {/* Brand & Mission */}
          <div className="md:col-span-1 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-700 flex items-center justify-center text-emerald-200">
                <Sprout className="w-5 h-5 text-emerald-300" />
              </div>
              <span className="font-extrabold text-white text-lg tracking-tight">
                {t('app_name', 'AgriVision AI')}
              </span>
            </div>
            <p className="text-xs text-emerald-300/70 leading-relaxed">
              Empowering farmers across India with immediate computer vision plant diagnostics, disease severity quantification, and regionally adapted agro-chemical prescriptions.
            </p>
            <div className="pt-2 flex items-center gap-2 text-xs text-emerald-400">
              <PhoneCall className="w-4 h-4 text-emerald-400" />
              <span>Kisan Call Center: <strong>1800-180-1551</strong> (Toll Free)</span>
            </div>
          </div>

          {/* Supported Crops */}
          <div>
            <h4 className="font-semibold text-white text-sm mb-3">Supported Crops</h4>
            <ul className="text-xs space-y-1.5 text-emerald-200/80">
              <li>• Tomato (Solanum lycopersicum)</li>
              <li>• Potato (Solanum tuberosum)</li>
              <li>• Rice / Paddy (Oryza sativa)</li>
              <li>• Corn / Maize (Zea mays)</li>
              <li>• Wheat (Triticum aestivum)</li>
              <li>• Cotton (Gossypium hirsutum)</li>
              <li>• Apple, Grape & Pepper</li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-white text-sm mb-3">Quick Navigation</h4>
            <ul className="text-xs space-y-2">
              <li><Link to="/detect" className="hover:text-white transition-colors">Diagnose Diseased Leaf</Link></li>
              <li><Link to="/dashboard" className="hover:text-white transition-colors">Farmer Health Dashboard</Link></li>
              <li><Link to="/history" className="hover:text-white transition-colors">Past Diagnosis Records</Link></li>
              <li><Link to="/treatments" className="hover:text-white transition-colors">Organic & Chemical Treatments</Link></li>
              <li><Link to="/resources" className="hover:text-white transition-colors">Farmer Educational Guides</Link></li>
            </ul>
          </div>

          {/* Agronomic Disclaimer */}
          <div>
            <h4 className="font-semibold text-white text-sm mb-3 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Field Advisory Notice
            </h4>
            <p className="text-xs text-emerald-300/70 leading-relaxed bg-emerald-900/40 p-3 rounded-xl border border-emerald-800">
              This system provides computer vision assisted early detection. Pesticide dosages must strictly comply with product labels and Central Insecticides Board (CIBRC) regulations. Always wear personal protective equipment (PPE).
            </p>
          </div>
        </div>

        <div className="pt-6 border-t border-emerald-900 flex flex-col sm:flex-row items-center justify-between text-xs text-emerald-400/70 gap-3">
          <p>© {new Date().getFullYear()} AgriVision AI (TAH-015). Precision Agriculture & Crop Disease Predictor.</p>
          <p className="flex items-center gap-1">
            Built with PyTorch, MobileNetV2, OpenCV & React
          </p>
        </div>
      </div>
    </footer>
  );
}
