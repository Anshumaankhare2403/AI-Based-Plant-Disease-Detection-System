import React, { useState, useEffect } from 'react';
import { 
  History, 
  Search, 
  Filter, 
  RefreshCw, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  X, 
  Leaf, 
  ShieldAlert, 
  ExternalLink 
} from 'lucide-react';
import { apiService } from '../services/api';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [selectedItem, setSelectedItem] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await apiService.getHistory(100);
      if (res.success && res.data) {
        setHistory(res.data);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const filteredHistory = history.filter((item) => {
    const matchesSearch = 
      item.plant?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.disease?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.raw_class?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = 
      statusFilter === 'ALL' || 
      item.status?.toUpperCase() === statusFilter;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="py-8 bg-slate-50 min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Foliar Diagnosis History
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Audit trail of uploaded leaf samples, CNN classification confidences, and recommended agronomic actions.
            </p>
          </div>
          <button
            onClick={fetchHistory}
            disabled={loading}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-sm transition-colors self-start sm:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Filter Controls */}
        <div className="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search by crop, disease, or class..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <Filter className="w-4 h-4 text-slate-400" />
            <div className="flex rounded-lg border border-slate-200 p-0.5 bg-slate-50 text-xs">
              {['ALL', 'HEALTHY', 'DISEASED'].map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1 rounded-md font-medium transition-colors ${
                    statusFilter === st
                      ? 'bg-white text-emerald-700 font-bold shadow-xs'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {st.charAt(0) + st.slice(1).toLowerCase()}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* History Table */}
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-400 uppercase text-[10px] font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">Sample</th>
                  <th className="py-3 px-4">Crop</th>
                  <th className="py-3 px-4">Diagnosed Condition</th>
                  <th className="py-3 px-4">Confidence</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Logged At</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-normal">
                {filteredHistory.length > 0 ? (
                  filteredHistory.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-3 px-4">
                        {item.image_base64 ? (
                          <img
                            src={item.image_base64}
                            alt="Leaf sample"
                            className="w-10 h-10 rounded-lg object-cover border border-slate-200 cursor-pointer hover:scale-105 transition-transform"
                            onClick={() => setSelectedItem(item)}
                          />
                        ) : (
                          <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                            <Leaf className="w-5 h-5" />
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 font-bold text-slate-900">{item.plant}</td>
                      <td className="py-3 px-4 text-emerald-700 font-semibold">{item.disease}</td>
                      <td className="py-3 px-4 font-mono font-bold text-slate-800">{item.confidence}%</td>
                      <td className="py-3 px-4">{item.severity || 'N/A'}</td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                            item.status === 'Healthy'
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {item.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-slate-400">
                        {item.created_at ? new Date(item.created_at).toLocaleString() : 'N/A'}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button
                          onClick={() => setSelectedItem(item)}
                          className="px-2.5 py-1 rounded bg-slate-100 hover:bg-emerald-50 hover:text-emerald-700 text-slate-600 font-medium transition-colors"
                        >
                          Details
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="8" className="py-12 text-center text-slate-400">
                      {loading ? (
                        <div className="flex items-center justify-center gap-2">
                          <RefreshCw className="w-4 h-4 animate-spin text-emerald-600" />
                          Loading foliar history...
                        </div>
                      ) : (
                        'No detection records match your current filters.'
                      )}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal for Details */}
        {selectedItem && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-xs p-4">
            <div className="bg-white rounded-2xl max-w-xl w-full p-6 space-y-4 shadow-xl border border-slate-200 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-start border-b border-slate-100 pb-3">
                <div>
                  <span className="text-[10px] uppercase font-bold text-slate-400">Record Inspection</span>
                  <h3 className="text-xl font-bold text-slate-900 mt-0.5">
                    {selectedItem.plant} - {selectedItem.disease}
                  </h3>
                </div>
                <button
                  onClick={() => setSelectedItem(null)}
                  className="p-1 rounded-lg text-slate-400 hover:bg-slate-100 text-slate-600"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {selectedItem.image_base64 && (
                <div className="rounded-xl overflow-hidden bg-slate-100 max-h-56 flex items-center justify-center border border-slate-200">
                  <img
                    src={selectedItem.image_base64}
                    alt="Sample preview"
                    className="max-h-56 object-contain"
                  />
                </div>
              )}

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-slate-400 font-medium block">Confidence</span>
                  <span className="text-base font-bold text-emerald-700">{selectedItem.confidence}%</span>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <span className="text-slate-400 font-medium block">Severity Level</span>
                  <span className="text-base font-bold text-slate-800">{selectedItem.severity}</span>
                </div>
              </div>

              {selectedItem.recommendations && (
                <div className="space-y-3 pt-2 text-xs">
                  <h4 className="font-bold text-slate-900">Agronomic Actions Prescribed:</h4>
                  {selectedItem.recommendations.organic_treatment && (
                    <div className="p-3 bg-emerald-50 rounded-lg border border-emerald-100">
                      <span className="font-bold text-emerald-900 block mb-1">Organic Management</span>
                      <ul className="list-disc list-inside text-emerald-950 space-y-0.5">
                        {selectedItem.recommendations.organic_treatment.map((t, i) => (
                          <li key={i}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {selectedItem.recommendations.chemical_treatment && (
                    <div className="p-3 bg-amber-50 rounded-lg border border-amber-100">
                      <span className="font-bold text-amber-900 block mb-1">Chemical Fungicides</span>
                      <ul className="list-disc list-inside text-amber-950 space-y-0.5">
                        {selectedItem.recommendations.chemical_treatment.map((t, i) => (
                          <li key={i}>{t}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              <div className="pt-3 border-t border-slate-100 flex justify-end">
                <button
                  onClick={() => setSelectedItem(null)}
                  className="px-4 py-2 rounded-lg bg-slate-900 text-white text-xs font-semibold"
                >
                  Close Inspection
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

