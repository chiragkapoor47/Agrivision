import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { resourcesApi } from '../services/api';
import { 
  BookOpen, Clock, Tag, ChevronDown, ChevronUp, 
  CheckCircle2, Sparkles, Filter 
} from 'lucide-react';

export default function EducationalResourcesPage() {
  const { t, language } = useLanguage();
  const [resources, setResources] = useState([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [expandedId, setExpandedId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadResources() {
      try {
        setLoading(true);
        const data = await resourcesApi.getResources({ category: activeCategory, language });
        setResources(data);
      } catch (err) {
        console.error('Failed to load educational resources:', err);
      } finally {
        setLoading(false);
      }
    }
    loadResources();
  }, [activeCategory, language]);

  const categories = [
    { id: 'all', label: 'All Resources' },
    { id: 'disease_identification', label: 'Disease Identification' },
    { id: 'organic_farming', label: 'Organic Farming' },
    { id: 'preventive_practices', label: 'Preventive Practices' },
    { id: 'crop_care', label: 'Crop Care Guides' }
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="border-b border-stone-200 pb-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-2">
          <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
          <span>Agricultural Extension Knowledge Base</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight">
          Farmer Educational Learning Center
        </h1>
        <p className="text-sm text-stone-600 mt-1">
          Practical manuals, organic pesticide preparation, and disease mitigation strategies.
        </p>
      </div>

      {/* Category Filter Pills */}
      <div className="flex flex-wrap items-center gap-2">
        {categories.map((c) => (
          <button
            key={c.id}
            onClick={() => setActiveCategory(c.id)}
            className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
              activeCategory === c.id
                ? 'bg-emerald-700 text-white shadow-xs'
                : 'bg-white text-stone-700 border border-stone-200 hover:bg-stone-50'
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Resource Cards */}
      <div className="space-y-4">
        {resources.map((item) => {
          const isExpanded = expandedId === item.id;
          const title = language === 'hi' ? item.title_hi : (language === 'as' ? item.title_as : item.title);
          const summary = language === 'hi' ? item.summary_hi : (language === 'as' ? item.summary_as : item.summary);

          return (
            <div
              key={item.id}
              className="bg-white rounded-3xl border border-stone-200 shadow-xs hover:border-emerald-300 transition-all overflow-hidden"
            >
              <div
                onClick={() => setExpandedId(isExpanded ? null : item.id)}
                className="p-6 cursor-pointer flex items-start justify-between gap-4"
              >
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-800 px-2.5 py-0.5 rounded-full border border-emerald-200">
                      {item.badge}
                    </span>
                    <span className="text-xs text-stone-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" /> {item.read_time_mins} min read
                    </span>
                  </div>
                  <h3 className="text-base sm:text-lg font-bold text-stone-900">
                    {title}
                  </h3>
                  <p className="text-xs sm:text-sm text-stone-600 leading-relaxed">
                    {summary}
                  </p>
                </div>

                <div className="p-2 rounded-xl bg-stone-50 text-stone-500 shrink-0 mt-1">
                  {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                </div>
              </div>

              {/* Expanded Guide Steps */}
              {isExpanded && (
                <div className="px-6 pb-6 pt-2 border-t border-stone-100 bg-stone-50/50 space-y-3">
                  <h4 className="text-xs font-bold text-stone-700 uppercase tracking-wider">
                    Recommended Implementation Protocol:
                  </h4>
                  <div className="space-y-2">
                    {item.steps_or_points.map((pt, idx) => (
                      <div key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-stone-800 bg-white p-3 rounded-xl border border-stone-100">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                        <span className="leading-relaxed">{pt}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
