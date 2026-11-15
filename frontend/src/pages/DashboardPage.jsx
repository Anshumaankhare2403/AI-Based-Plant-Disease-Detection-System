import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  BarChart2, 
  PieChart, 
  Activity, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Sprout, 
  ArrowRight, 
  RefreshCw,
  TrendingUp,
  Layers
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  PieChart as RechartsPieChart, 
  Pie, 
  Cell, 
  Legend 
} from 'recharts';
import { apiService } from '../services/api';

const COLORS = ['#16a34a', '#22c55e', '#eab308', '#f97316', '#ef4444', '#8b5cf6', '#06b6d4', '#64748b'];

export default function DashboardPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiService.getDashboardStats();
      if (res.success && res.data) {
        setStats(res.data);
      } else {
        setError(res.error || 'Failed to fetch analytics.');
      }
    } catch (err) {
      setError(err.message || 'Unable to connect to analytics service.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const healthData = stats ? [
    { name: 'Healthy', value: stats.healthy_count },
    { name: 'Diseased', value: stats.diseased_count },
  ] : [];

  return (
    <div className="py-8 bg-slate-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Pathology & Outbreak Analytics
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Field intelligence and epidemiological distribution of identified plant pathogens.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={fetchStats}
              disabled={loading}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-sm transition-colors"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              Refresh Data
            </button>
            <Link
              to="/detect"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-md shadow-emerald-200 transition-colors"
            >
              <Sprout className="w-3.5 h-3.5" />
              New Scan
            </Link>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex justify-between items-center">
            <span>{error}</span>
            <button onClick={fetchStats} className="underline font-semibold">Retry</button>
          </div>
        )}

        {/* Metric Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Total Predictions */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Total Scans</span>
              <p className="text-2xl font-black text-slate-900">{stats?.total_predictions ?? 0}</p>
              <span className="text-[11px] text-emerald-600 font-medium">Archived foliar records</span>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Activity className="w-6 h-6" />
            </div>
          </div>

          {/* Healthy Foliage */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Healthy Foliage</span>
              <p className="text-2xl font-black text-emerald-600">{stats?.healthy_count ?? 0}</p>
              <span className="text-[11px] text-slate-500 font-medium">{stats?.healthy_percentage ?? 0}% healthy ratio</span>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100/60 text-emerald-700 flex items-center justify-center">
              <CheckCircle2 className="w-6 h-6" />
            </div>
          </div>

          {/* Pathological Outbreaks */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Infected Samples</span>
              <p className="text-2xl font-black text-amber-600">{stats?.diseased_count ?? 0}</p>
              <span className="text-[11px] text-amber-700 font-medium">Requiring active treatment</span>
            </div>
            <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
              <AlertTriangle className="w-6 h-6" />
            </div>
          </div>

          {/* Deep CNN Models */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex items-center justify-between">
            <div className="space-y-1">
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Model Status</span>
              <p className="text-base font-bold text-slate-800">14 Classes</p>
              <span className="text-[11px] text-emerald-600 font-medium">Inference: &lt;50ms</span>
            </div>
            <div className="w-12 h-12 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center">
              <Layers className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Disease Distribution Bar Chart */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-emerald-600" />
                Prevalent Pathologies
              </h3>
              <span className="text-[11px] text-slate-400">By frequency</span>
            </div>
            <div className="h-64 w-full">
              {stats?.disease_distribution && stats.disease_distribution.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={stats.disease_distribution} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                    <XAxis 
                      dataKey="name" 
                      angle={-25} 
                      textAnchor="end" 
                      interval={0} 
                      tick={{ fontSize: 10, fill: '#64748b' }} 
                    />
                    <YAxis tick={{ fontSize: 10, fill: '#64748b' }} allowDecimals={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                    />
                    <Bar dataKey="count" fill="#16a34a" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-400 text-xs">
                  <BarChart2 className="w-8 h-8 mb-2 opacity-50" />
                  No diagnosis records available yet.
                </div>
              )}
            </div>
          </div>

          {/* Crop Breakdown Chart */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
                <PieChart className="w-4 h-4 text-emerald-600" />
                Crop Category Distribution
              </h3>
              <span className="text-[11px] text-slate-400">Total by crop</span>
            </div>
            <div className="h-64 w-full">
              {stats?.crop_distribution && stats.crop_distribution.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <RechartsPieChart>
                    <Pie
                      data={stats.crop_distribution}
                      dataKey="count"
                      nameKey="crop"
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      labelLine={false}
                    >
                      {stats.crop_distribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                    />
                  </RechartsPieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-slate-400 text-xs">
                  <PieChart className="w-8 h-8 mb-2 opacity-50" />
                  Scan leaves to visualize crop breakdown.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recent Diagnoses Table */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden space-y-4 p-6">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <Clock className="w-4 h-4 text-emerald-600" />
              Recent Field Scans
            </h3>
            <Link to="/history" className="text-xs text-emerald-600 hover:text-emerald-700 font-semibold flex items-center gap-1">
              View All History <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-400 uppercase text-[10px] font-semibold border-y border-slate-200">
                <tr>
                  <th className="py-2.5 px-3">Thumbnail</th>
                  <th className="py-2.5 px-3">Crop</th>
                  <th className="py-2.5 px-3">Diagnosed Pathology</th>
                  <th className="py-2.5 px-3">Confidence</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-normal">
                {stats?.recent_predictions && stats.recent_predictions.length > 0 ? (
                  stats.recent_predictions.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50/70 transition-colors">
                      <td className="py-2.5 px-3">
                        {p.image_base64 ? (
                          <img
                            src={p.image_base64}
                            alt="Leaf"
                            className="w-9 h-9 rounded-lg object-cover border border-slate-200"
                          />
                        ) : (
                          <div className="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                            <Sprout className="w-4 h-4" />
                          </div>
                        )}
                      </td>
                      <td className="py-2.5 px-3 font-semibold text-slate-800">{p.plant}</td>
                      <td className="py-2.5 px-3 text-emerald-700 font-medium">{p.disease}</td>
                      <td className="py-2.5 px-3 font-mono font-bold text-slate-900">{p.confidence}%</td>
                      <td className="py-2.5 px-3">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            p.status === 'Healthy'
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {p.status}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-slate-400">
                        {p.created_at ? new Date(p.created_at).toLocaleDateString() : 'Just now'}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="py-8 text-center text-slate-400">
                      No records found. Run your first diagnosis from the Diagnose Leaf page!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

