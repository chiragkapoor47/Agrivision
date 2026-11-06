import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { agriApi } from '../services/api';
import { 
  Pill, Search, Leaf, FlaskConical, ShieldCheck, 
  Clock, AlertTriangle, ShieldAlert, Sparkles 
} from 'lucide-react';

export default function TreatmentsPage() {
  const { t, language } = useLanguage();
  const [diseases, setDiseases] = useState([]);
  const [selectedDisease, setSelectedDisease] = useState(null);
  const [treatmentDetails, setTreatmentDetails] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const data = await agriApi.getDiseases();
        setDiseases(data);
        if (data.length > 0) {
          setSelectedDisease(data[0]);
          loadTreatmentFor(data[0].id);
        }
      } catch (err) {
        console.error('Failed to load diseases:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const loadTreatmentFor = async (diseaseKey) => {
    try {
      const plan = await agriApi.getTreatments({ disease: diseaseKey, language });
      setTreatmentDetails(plan);
    } catch (e) {
      console.warn('Failed to load treatment plan:', e);
    }
  };

  const handleSelectDisease = (dis) => {
    setSelectedDisease(dis);
    loadTreatmentFor(dis.id);
  };

  const filteredDiseases = diseases.filter(d => 
    d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.crop.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div className="border-b border-stone-200 pb-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold mb-2">
          <Pill className="w-3.5 h-3.5 text-emerald-700" />
          <span>Scientifically Verified Agricultural Prescriptions</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight">
          Crop Disease Treatment Reference Manual
        </h1>
        <p className="text-sm text-stone-600 mt-1">
          Explore certified organic bio-fungicides, chemical active ingredients, PPE protocols, and Pre-Harvest Intervals (PHI).
        </p>
      </div>

      {/* Main Split Layout: Disease List Sidebar + Full Prescription Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Sidebar list */}
        <div className="lg:col-span-4 bg-white p-4 rounded-3xl border border-stone-200 shadow-xs space-y-3">
          <div className="relative">
            <Search className="w-4 h-4 text-stone-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search crop or disease..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-stone-50 border border-stone-200 rounded-xl pl-9 pr-3 py-2 text-xs sm:text-sm focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="space-y-1.5 max-h-[580px] overflow-y-auto pr-1">
            {filteredDiseases.map((d) => (
              <button
                key={d.id}
                onClick={() => handleSelectDisease(d)}
                className={`w-full text-left p-3 rounded-2xl transition-all border ${
                  selectedDisease?.id === d.id
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-950 font-bold shadow-2xs'
                    : 'bg-white border-transparent text-stone-700 hover:bg-stone-50'
                }`}
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-extrabold text-stone-900">{d.crop}</span>
                  <span className="text-[10px] bg-stone-100 text-stone-600 px-2 py-0.5 rounded-full">{d.pathogen_type}</span>
                </div>
                <div className="text-xs sm:text-sm mt-0.5">{d.name}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Prescription Details Panel */}
        <div className="lg:col-span-8 space-y-6">
          {treatmentDetails ? (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-stone-200 shadow-md space-y-6">
              {/* Header */}
              <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-stone-100">
                <div>
                  <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider bg-emerald-50 px-2.5 py-1 rounded-md">
                    {treatmentDetails.crop}
                  </span>
                  <h2 className="text-2xl font-extrabold text-stone-900 mt-1">
                    {treatmentDetails.disease}
                  </h2>
                  <p className="text-xs text-stone-500 italic mt-0.5">
                    Pathogen: {treatmentDetails.pathogen}
                  </p>
                </div>
              </div>

              {/* Symptoms */}
              <div>
                <h3 className="font-bold text-sm text-stone-800 uppercase tracking-wider mb-2">
                  Visible Symptoms
                </h3>
                <ul className="space-y-1.5 text-xs sm:text-sm text-stone-700">
                  {treatmentDetails.symptoms?.map((s, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 mt-2 shrink-0"></span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Organic Treatment */}
              <div className="bg-emerald-50/60 p-5 rounded-2xl border border-emerald-100 space-y-3">
                <div className="flex items-center gap-2 text-emerald-900 font-bold text-sm">
                  <Leaf className="w-4 h-4 text-emerald-600" />
                  <h4>{treatmentDetails.organic_treatment?.title}</h4>
                </div>
                <ul className="space-y-2 text-xs sm:text-sm text-stone-800">
                  {treatmentDetails.organic_treatment?.remedies?.map((r, i) => (
                    <li key={i} className="flex items-start gap-2.5">
                      <span className="w-5 h-5 rounded-md bg-emerald-200 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0">
                        {i + 1}
                      </span>
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Chemical Treatment */}
              <div className="bg-amber-50/50 p-5 rounded-2xl border border-amber-200/80 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-amber-950 font-bold text-sm">
                    <FlaskConical className="w-4 h-4 text-amber-600" />
                    <h4>{treatmentDetails.chemical_treatment?.title}</h4>
                  </div>
                  {treatmentDetails.chemical_treatment?.pre_harvest_interval_days > 0 && (
                    <span className="text-xs bg-amber-100 text-amber-900 font-bold px-3 py-1 rounded-full border border-amber-300 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      PHI: {treatmentDetails.chemical_treatment?.pre_harvest_interval_days} days
                    </span>
                  )}
                </div>

                <div className="space-y-2 text-xs sm:text-sm">
                  <div>
                    <span className="font-semibold text-stone-700">Active Ingredients: </span>
                    <span className="font-bold text-amber-900">
                      {treatmentDetails.chemical_treatment?.active_ingredients?.join(', ')}
                    </span>
                  </div>
                  <div>
                    <span className="font-semibold text-stone-700">Application: </span>
                    <span className="text-stone-800">{treatmentDetails.chemical_treatment?.application_method}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-red-50 text-red-900 text-xs flex items-start gap-2 border border-red-200">
                    <ShieldAlert className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                    <span>{treatmentDetails.chemical_treatment?.safety_precautions}</span>
                  </div>
                </div>
              </div>

              {/* Preventive Measures */}
              <div className="bg-sky-50/50 p-5 rounded-2xl border border-sky-100 space-y-2">
                <div className="flex items-center gap-2 text-sky-950 font-bold text-sm">
                  <ShieldCheck className="w-4 h-4 text-sky-600" />
                  <h4>Preventive Cultural Measures</h4>
                </div>
                <ul className="space-y-1.5 text-xs sm:text-sm text-stone-700">
                  {treatmentDetails.preventive_measures?.map((p, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-sky-600 mt-2 shrink-0"></span>
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-3xl p-12 text-center text-stone-500 border border-stone-200">
              Select a disease from the list to view full treatment recommendations.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
