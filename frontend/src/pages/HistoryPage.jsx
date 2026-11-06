import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { diagnosisApi, agriApi } from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import { 
  History as HistoryIcon, Trash2, Eye, Filter, 
  RefreshCw, Camera, AlertCircle, ArrowRight 
} from 'lucide-react';

export default function HistoryPage() {
  const { t } = useLanguage();
  const [records, setRecords] = useState([]);
  const [crops, setCrops] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('');
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);

  const fetchRecords = async () => {
    try {
      setLoading(true);
      const params = {};
      if (selectedCrop && selectedCrop !== 'all') params.crop = selectedCrop;
      if (selectedSeverity && selectedSeverity !== 'all') params.severity = selectedSeverity;

      const [historyData, cropsData] = await Promise.all([
        diagnosisApi.getHistory(params),
        agriApi.getCrops()
      ]);
      setRecords(historyData);
      setCrops(cropsData);
    } catch (err) {
      console.error('Failed to load diagnosis history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, [selectedCrop, selectedSeverity]);

  const handleDelete = async (id, e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!window.confirm(`Are you sure you want to delete diagnosis record #${id}?`)) {
      return;
    }
    try {
      setDeletingId(id);
      await diagnosisApi.deleteRecord(id);
      setRecords(records.filter(r => r.id !== id));
    } catch (err) {
      alert(err.message || 'Failed to delete record.');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-stone-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight flex items-center gap-2">
            <HistoryIcon className="w-7 h-7 text-emerald-700" />
            {t('history.title', 'Diagnosis History & Records')}
          </h1>
          <p className="text-sm text-stone-600 mt-1">
            {t('history.subtitle', 'Review previous crop scans, track disease spread, and inspect treatment recommendations.')}
          </p>
        </div>

        <Link
          to="/detect"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm transition-all shadow-md shadow-emerald-600/20"
        >
          <Camera className="w-4 h-4" />
          <span>New Leaf Scan</span>
        </Link>
      </div>

      {/* Filter Controls */}
      <div className="bg-white p-4 rounded-2xl border border-stone-200 shadow-xs flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2 text-xs font-bold text-stone-500 uppercase tracking-wider">
          <Filter className="w-4 h-4 text-emerald-600" />
          <span>Filter Records:</span>
        </div>

        {/* Filter by Crop */}
        <select
          value={selectedCrop}
          onChange={(e) => setSelectedCrop(e.target.value)}
          className="bg-stone-50 border border-stone-200 rounded-xl px-3 py-1.5 text-xs sm:text-sm font-medium text-stone-800 focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
        >
          <option value="">{t('history.all_crops', 'All Crops')}</option>
          {crops.map((c) => (
            <option key={c.id} value={c.name}>{c.name}</option>
          ))}
        </select>

        {/* Filter by Severity */}
        <select
          value={selectedSeverity}
          onChange={(e) => setSelectedSeverity(e.target.value)}
          className="bg-stone-50 border border-stone-200 rounded-xl px-3 py-1.5 text-xs sm:text-sm font-medium text-stone-800 focus:outline-hidden focus:ring-2 focus:ring-emerald-500"
        >
          <option value="">{t('history.all_severities', 'All Severities')}</option>
          <option value="None / Healthy">None / Healthy (0%)</option>
          <option value="Low">Low (&lt;20%)</option>
          <option value="Moderate">Moderate (20-50%)</option>
          <option value="Severe">Severe (&gt;50%)</option>
        </select>

        <span className="text-xs text-stone-500 ml-auto">
          Showing <strong>{records.length}</strong> diagnoses
        </span>
      </div>

      {/* Records Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <RefreshCw className="w-8 h-8 text-emerald-600 animate-spin mx-auto mb-2" />
          <p className="text-sm text-stone-600">Loading previous records...</p>
        </div>
      ) : records.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-stone-200 shadow-xs space-y-4 max-w-md mx-auto">
          <AlertCircle className="w-12 h-12 text-stone-400 mx-auto" />
          <h3 className="font-bold text-base text-stone-800">
            {t('history.empty_state', 'No diagnosis records found. Start by scanning your first leaf!')}
          </h3>
          <Link
            to="/detect"
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-600 text-white font-semibold text-sm"
          >
            <Camera className="w-4 h-4" /> {t('history.btn_scan', 'Start First Scan')}
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {records.map((r) => (
            <div
              key={r.id}
              className="bg-white rounded-3xl border border-stone-200/90 shadow-sm hover:shadow-md transition-shadow overflow-hidden flex flex-col justify-between group"
            >
              <div>
                {/* Image preview with severity banner */}
                <div className="relative aspect-16/10 bg-stone-950 overflow-hidden">
                  <img
                    src={r.overlay_url || r.image_url}
                    alt={r.disease}
                    className="w-full h-full object-cover group-hover:scale-102 transition-transform duration-300"
                    onError={(e) => {
                      e.target.src = 'https://images.unsplash.com/photo-1592417817098-8f3d6ef23a49?w=400&auto=format&fit=crop&q=60';
                    }}
                  />
                  <div className="absolute top-2.5 left-2.5">
                    <span className="text-[11px] font-extrabold bg-stone-900/80 backdrop-blur-xs text-white px-2.5 py-1 rounded-lg">
                      {r.crop}
                    </span>
                  </div>
                  <div className="absolute top-2.5 right-2.5">
                    <SeverityBadge level={r.severity_level} percentage={r.affected_area_percentage} size="sm" />
                  </div>
                </div>

                {/* Card Content */}
                <div className="p-4 space-y-2">
                  <h3 className="font-bold text-base text-stone-900 line-clamp-1">
                    {r.disease}
                  </h3>
                  <div className="flex items-center justify-between text-xs text-stone-500">
                    <span>Confidence: <strong className="text-emerald-700">{r.confidence_score}%</strong></span>
                    <span>{new Date(r.created_at).toLocaleDateString()}</span>
                  </div>
                  <p className="text-[11px] text-stone-500 truncate">
                    📍 {r.location_summary}
                  </p>
                </div>
              </div>

              {/* Bottom Actions */}
              <div className="p-4 pt-0 flex items-center justify-between border-t border-stone-100 mt-2">
                <Link
                  to={`/diagnosis/${r.id}`}
                  className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-700 hover:text-emerald-900"
                >
                  <Eye className="w-4 h-4" />
                  <span>{t('history.btn_view', 'View Report')}</span>
                </Link>

                <button
                  type="button"
                  onClick={(e) => handleDelete(r.id, e)}
                  disabled={deletingId === r.id}
                  className="p-1.5 rounded-lg text-stone-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                  title="Delete record"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
