import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { dashboardApi } from '../services/api';
import SeverityBadge from '../components/SeverityBadge';
import { 
  Activity, ShieldCheck, AlertTriangle, AlertOctagon, Camera, 
  ArrowRight, RefreshCw, BarChart2, PieChart as PieIcon, Calendar, CheckCircle2 
} from 'lucide-react';
import { 
  ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend 
} from 'recharts';

export default function DashboardPage() {
  const { t } = useLanguage();
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        setLoading(true);
        const data = await dashboardApi.getStats();
        setStats(data);
      } catch (err) {
        console.error('Failed to load dashboard statistics:', err);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <RefreshCw className="w-10 h-10 text-emerald-600 animate-spin mx-auto mb-3" />
        <p className="text-sm text-stone-600 font-semibold">Aggregating Farm Health Telemetry...</p>
      </div>
    );
  }

  const PIE_COLORS = ['#10b981', '#84cc16', '#f59e0b', '#ef4444'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-stone-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-stone-900 tracking-tight">
            {t('dashboard.title', 'Farmer Diagnostic Intelligence Dashboard')}
          </h1>
          <p className="text-sm text-stone-600 mt-1">
            {user ? `Farm portfolio of ${user.full_name} (${user.village}, ${user.district})` : t('dashboard.subtitle', 'Overview of crop health, disease frequencies, and severe infestation alerts across your fields.')}
          </p>
        </div>

        <Link
          to="/detect"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm transition-all shadow-md shadow-emerald-600/20 active:scale-95"
        >
          <Camera className="w-4 h-4" />
          <span>New Leaf Diagnosis</span>
        </Link>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Diagnoses */}
        <div className="bg-white p-5 rounded-3xl border border-stone-200 shadow-xs flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-black text-stone-900">{stats?.total_diagnoses || 0}</div>
            <div className="text-xs font-semibold text-stone-500">{t('dashboard.total_scans', 'Total Diagnoses')}</div>
          </div>
        </div>

        {/* Healthy Crops */}
        <div className="bg-white p-5 rounded-3xl border border-stone-200 shadow-xs flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-black text-emerald-700">{stats?.healthy_count || 0}</div>
            <div className="text-xs font-semibold text-stone-500">{t('dashboard.healthy_crops', 'Healthy Crops')}</div>
          </div>
        </div>

        {/* Infected Crops */}
        <div className="bg-white p-5 rounded-3xl border border-stone-200 shadow-xs flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-black text-amber-700">{stats?.infected_count || 0}</div>
            <div className="text-xs font-semibold text-stone-500">{t('dashboard.infected_crops', 'Infected Crops')}</div>
          </div>
        </div>

        {/* Severe Alerts */}
        <div className="bg-white p-5 rounded-3xl border border-stone-200 shadow-xs flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-700 flex items-center justify-center shrink-0">
            <AlertOctagon className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl sm:text-3xl font-black text-red-600">{stats?.severe_alert_count || 0}</div>
            <div className="text-xs font-semibold text-stone-500">{t('dashboard.severe_alerts', 'Severe Alerts')}</div>
          </div>
        </div>
      </div>

      {/* Visual Recharts Section: Severity Distribution + Crop Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Severity Pie Chart */}
        <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-base text-stone-900 flex items-center gap-2">
              <PieIcon className="w-4 h-4 text-emerald-600" />
              {t('dashboard.severity_breakdown', 'Severity Level Distribution')}
            </h3>
            <span className="text-xs text-stone-500">Affected leaf area ratio</span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.severity_distribution || []}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                  label={({ name, percent }) => percent > 0 ? `${(percent * 100).toFixed(0)}%` : ''}
                >
                  {(stats?.severity_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color || PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Crops Diagnosed Bar Chart */}
        <div className="bg-white p-6 rounded-3xl border border-stone-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-base text-stone-900 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-emerald-600" />
              {t('dashboard.crop_breakdown', 'Diagnoses by Crop Species')}
            </h3>
            <span className="text-xs text-stone-500">Sample count per crop</span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats?.crop_distribution || []}>
                <XAxis dataKey="crop" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#059669" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Frequently Detected Diseases Table */}
      <div className="bg-white rounded-3xl p-6 border border-stone-200 shadow-sm space-y-4">
        <h3 className="font-bold text-base text-stone-900">
          {t('dashboard.frequent_diseases', 'Most Frequently Detected Diseases')}
        </h3>
        
        {stats?.frequently_detected_diseases?.length === 0 ? (
          <p className="text-xs text-stone-500 italic py-4">No diseased foliage detected yet. All scanned crops are healthy.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {stats?.frequently_detected_diseases?.map((dis, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-stone-50 border border-stone-100 flex items-center justify-between">
                <div>
                  <h4 className="font-bold text-sm text-stone-900">{dis.disease}</h4>
                  <span className="text-xs text-emerald-700 font-medium">{dis.crop}</span>
                </div>
                <div className="text-right">
                  <span className="text-base font-extrabold text-stone-800">{dis.occurrences}</span>
                  <span className="text-[10px] text-stone-500 block">cases</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent Leaf Diagnoses Table */}
      <div className="bg-white rounded-3xl p-6 border border-stone-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-base text-stone-900">
            {t('dashboard.recent_scans', 'Recent Leaf Diagnoses')}
          </h3>
          <Link to="/history" className="text-xs font-bold text-emerald-700 hover:underline flex items-center gap-1">
            {t('dashboard.view_all', 'View Full History')} <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {stats?.recent_diagnoses?.length === 0 ? (
          <div className="py-8 text-center text-stone-500 text-sm">
            No previous scans found.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-stone-50 text-stone-600 font-bold uppercase tracking-wider border-b border-stone-200">
                <tr>
                  <th className="py-3 px-4">Leaf Preview</th>
                  <th className="py-3 px-4">Crop</th>
                  <th className="py-3 px-4">Detected Disease</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-100 font-medium text-stone-800">
                {stats?.recent_diagnoses?.map((r) => (
                  <tr key={r.id} className="hover:bg-emerald-50/40 transition-colors">
                    <td className="py-2.5 px-4">
                      <div className="w-10 h-10 rounded-lg overflow-hidden bg-stone-900">
                        <img
                          src={r.overlay_url || r.image_url}
                          alt={r.disease}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.src = 'https://images.unsplash.com/photo-1592417817098-8f3d6ef23a49?w=100&auto=format&fit=crop&q=60';
                          }}
                        />
                      </div>
                    </td>
                    <td className="py-2.5 px-4 font-bold text-stone-900">{r.crop}</td>
                    <td className="py-2.5 px-4">{r.disease}</td>
                    <td className="py-2.5 px-4">
                      <SeverityBadge level={r.severity_level} percentage={r.affected_area_percentage} size="sm" />
                    </td>
                    <td className="py-2.5 px-4 font-bold text-emerald-700">{r.confidence_score}%</td>
                    <td className="py-2.5 px-4 text-stone-500">{r.created_at}</td>
                    <td className="py-2.5 px-4 text-right">
                      <Link
                        to={`/diagnosis/${r.id}`}
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold transition-colors"
                      >
                        Report <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
