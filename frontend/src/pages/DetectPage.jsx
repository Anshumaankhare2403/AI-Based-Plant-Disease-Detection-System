import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  UploadCloud, 
  FileImage, 
  AlertCircle, 
  CheckCircle2, 
  ArrowRight, 
  RefreshCw, 
  Leaf, 
  ShieldAlert, 
  Sparkles,
  Info,
  Clock,
  ExternalLink
} from 'lucide-react';
import { apiService } from '../services/api';

export default function DetectPage() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileSelection = (selectedFile) => {
    if (!selectedFile) return;

    // Validate type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Please upload a valid image (JPEG, PNG, or WebP).');
      return;
    }

    // Validate size (10 MB max)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('Image file is too large. Maximum size allowed is 10MB.');
      return;
    }

    setError(null);
    setResult(null);
    setFile(selectedFile);

    const reader = new FileReader();
    reader.onload = (e) => setPreviewUrl(e.target.result);
    reader.readAsDataURL(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select or drop a plant leaf image first.');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingStep('Uploading foliar image to server...');

    try {
      setTimeout(() => setLoadingStep('Extracting morphological features (128x128)...'), 300);
      setTimeout(() => setLoadingStep('Evaluating Convolutional layers & Softmax...'), 600);

      const response = await apiService.predictImage(file, (progressEvent) => {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        setUploadProgress(percent);
      });

      if (response.success && response.data) {
        setResult(response.data);
      } else {
        setError(response.error || 'Failed to complete diagnosis.');
      }
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.message || err.message || 'An error occurred during diagnosis.';
      setError(msg);
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="py-10 bg-slate-50 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Page Header */}
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
            AI Pathology Scanner
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Diagnose Foliar Plant Disease
          </h1>
          <p className="text-sm text-slate-500">
            Upload a clear photograph of a single leaf to identify potential fungal, bacterial, or environmental infections.
          </p>
        </div>

        {/* Upload Card */}
        {!result && (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden p-6 sm:p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Dropzone */}
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all ${
                  isDragging
                    ? 'border-emerald-500 bg-emerald-50/70 scale-[0.99]'
                    : previewUrl
                    ? 'border-emerald-300 bg-emerald-50/20'
                    : 'border-slate-300 hover:border-emerald-400 bg-slate-50/50 hover:bg-slate-50'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  onChange={(e) => handleFileSelection(e.target.files[0])}
                  className="hidden"
                />

                {previewUrl ? (
                  <div className="space-y-4">
                    <div className="relative inline-block mx-auto rounded-xl overflow-hidden shadow-md border-2 border-white ring-1 ring-emerald-200">
                      <img
                        src={previewUrl}
                        alt="Leaf preview"
                        className="max-h-64 max-w-full object-contain mx-auto"
                      />
                    </div>
                    <div className="flex items-center justify-center gap-2 text-xs text-slate-600 font-medium">
                      <FileImage className="w-4 h-4 text-emerald-600" />
                      <span>{file?.name}</span>
                      <span className="text-slate-400">({(file?.size / (1024 * 1024)).toFixed(2)} MB)</span>
                    </div>
                    <p className="text-xs text-emerald-600 font-medium">
                      Click or drag a new photo to replace
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
                      <UploadCloud className="w-8 h-8" />
                    </div>
                    <div className="space-y-1">
                      <p className="text-base font-semibold text-slate-700">
                        Drop your leaf photograph here, or <span className="text-emerald-600 underline">browse</span>
                      </p>
                      <p className="text-xs text-slate-400">
                        Supports JPEG, PNG, WebP up to 10MB
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 rounded-xl bg-red-50 border border-red-200 flex items-start gap-3 text-red-700 text-sm">
                  <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <p className="font-semibold">Diagnostic Error</p>
                    <p className="text-xs text-red-600 mt-0.5">{error}</p>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3 justify-end items-center pt-2">
                {file && (
                  <button
                    type="button"
                    onClick={handleReset}
                    disabled={loading}
                    className="w-full sm:w-auto px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 text-sm font-medium transition-colors"
                  >
                    Clear Photo
                  </button>
                )}
                <button
                  type="submit"
                  disabled={!file || loading}
                  className={`w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-xl font-semibold text-sm text-white shadow-md transition-all ${
                    !file || loading
                      ? 'bg-slate-300 cursor-not-allowed shadow-none'
                      : 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-200 hover:-translate-y-0.5'
                  }`}
                >
                  {loading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Analyzing Foliage...
                    </>
                  ) : (
                    <>
                      <Leaf className="w-4 h-4" />
                      Run CNN Diagnosis
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </>
                  )}
                </button>
              </div>

              {/* Progress feedback */}
              {loading && (
                <div className="pt-2 space-y-2">
                  <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 rounded-full animate-pulse w-3/4"></div>
                  </div>
                  <p className="text-xs text-center text-slate-500 font-medium">{loadingStep}</p>
                </div>
              )}
            </form>
          </div>
        )}

        {/* Diagnostic Results Presentation */}
        {result && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden p-6 sm:p-8 space-y-6">
              {/* Header with status badge */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
                <div>
                  <span className="text-xs uppercase font-bold tracking-wider text-slate-400">Diagnosis Report</span>
                  <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2 mt-1">
                    {result.plant} — <span className="text-emerald-700">{result.disease}</span>
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wide inline-flex items-center gap-1.5 ${
                      result.status === 'Healthy'
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                        : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}
                  >
                    {result.status === 'Healthy' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <ShieldAlert className="w-4 h-4 text-amber-600" />
                    )}
                    {result.status}
                  </span>
                  <span className="px-3 py-1.5 rounded-full text-xs font-bold bg-slate-100 text-slate-700 border border-slate-200">
                    Severity: {result.severity}
                  </span>
                </div>
              </div>

              {/* Confidence Alert if below threshold */}
              {result.confidence_warning && (
                <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3 text-amber-800 text-xs">
                  <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 text-amber-600" />
                  <div>
                    <span className="font-bold">Caution: Low Confidence Prediction</span>
                    <p className="mt-0.5 text-amber-700">{result.confidence_warning}</p>
                  </div>
                </div>
              )}

              {/* Image & Confidence Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
                {/* Uploaded Leaf Thumbnail */}
                <div className="rounded-xl overflow-hidden border border-slate-200 bg-slate-50 p-2 text-center">
                  <img
                    src={previewUrl}
                    alt="Analyzed leaf"
                    className="rounded-lg max-h-56 w-full object-contain mx-auto"
                  />
                  <div className="mt-2 text-[11px] text-slate-400 flex items-center justify-center gap-2">
                    <Clock className="w-3 h-3" />
                    <span>Inference: {result.meta?.latency_ms}ms</span>
                    <span>•</span>
                    <span>Input: {result.meta?.processed_dimensions}</span>
                  </div>
                </div>

                {/* Probability & Pathology Metrics */}
                <div className="md:col-span-2 space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-1 text-sm font-semibold">
                      <span className="text-slate-700">Classification Confidence</span>
                      <span className="text-emerald-700 font-bold">{result.confidence}%</span>
                    </div>
                    <div className="h-3 w-full bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-700 ${
                          result.confidence >= 80
                            ? 'bg-emerald-600'
                            : result.confidence >= 60
                            ? 'bg-amber-500'
                            : 'bg-red-500'
                        }`}
                        style={{ width: `${result.confidence}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Biological Pathogen */}
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-slate-400 block font-medium">Pathogen / Cause</span>
                      <span className="font-semibold text-slate-800 mt-0.5 block">{result.pathogen}</span>
                    </div>
                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-slate-400 block font-medium">Dataset Class Identifier</span>
                      <span className="font-mono text-[11px] text-slate-700 mt-0.5 block truncate" title={result.raw_class}>
                        {result.raw_class}
                      </span>
                    </div>
                  </div>

                  {/* Description */}
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Pathology Overview</h4>
                    <p className="text-sm text-slate-600 leading-relaxed bg-slate-50/50 p-3 rounded-lg border border-slate-100">
                      {result.description}
                    </p>
                  </div>
                </div>
              </div>

              {/* Symptoms */}
              {result.symptoms && result.symptoms.length > 0 && (
                <div className="space-y-2 pt-2">
                  <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
                    <Info className="w-4 h-4 text-emerald-600" />
                    Observed Diagnostic Symptoms
                  </h3>
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-600">
                    {result.symptoms.map((sym, idx) => (
                      <li key={idx} className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                        <span className="text-emerald-600 font-bold">•</span>
                        <span>{sym}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Integrated Pest Management Recommendations */}
              <div className="space-y-4 pt-4 border-t border-slate-100">
                <h3 className="text-base font-bold text-slate-900">Recommended Agronomic Management Protocols</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Organic Treatment */}
                  <div className="bg-emerald-50/60 rounded-xl p-4 border border-emerald-200/80 space-y-2">
                    <span className="text-xs font-bold uppercase text-emerald-800 tracking-wider flex items-center gap-1.5">
                      <Leaf className="w-4 h-4 text-emerald-600" /> Organic Controls
                    </span>
                    <ul className="text-xs text-slate-700 space-y-1.5">
                      {result.recommendations?.organic_treatment?.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-1.5">
                          <span className="text-emerald-600 font-bold">✓</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Chemical Treatment */}
                  <div className="bg-amber-50/60 rounded-xl p-4 border border-amber-200/80 space-y-2">
                    <span className="text-xs font-bold uppercase text-amber-900 tracking-wider flex items-center gap-1.5">
                      <ShieldAlert className="w-4 h-4 text-amber-700" /> Chemical Fungicides
                    </span>
                    <ul className="text-xs text-slate-700 space-y-1.5">
                      {result.recommendations?.chemical_treatment?.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-1.5">
                          <span className="text-amber-600 font-bold">✓</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Prevention */}
                  <div className="bg-blue-50/60 rounded-xl p-4 border border-blue-200/80 space-y-2">
                    <span className="text-xs font-bold uppercase text-blue-900 tracking-wider flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-blue-600" /> Cultural Prevention
                    </span>
                    <ul className="text-xs text-slate-700 space-y-1.5">
                      {result.recommendations?.prevention?.map((item, idx) => (
                        <li key={idx} className="flex items-start gap-1.5">
                          <span className="text-blue-600 font-bold">✓</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Top 3 Alternative Candidates */}
              {result.top_3 && result.top_3.length > 1 && (
                <div className="pt-4 border-t border-slate-100">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                    Alternative Model Hypotheses
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                    {result.top_3.map((cand, idx) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 text-xs flex justify-between items-center">
                        <span className="text-slate-700 font-medium truncate max-w-[180px]">
                          {cand.plant} - {cand.disease}
                        </span>
                        <span className="font-bold text-slate-900">{cand.confidence}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Reset Action */}
              <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row justify-between gap-3 items-center">
                <span className="text-xs text-slate-400">
                  Diagnosis recorded to database ID: <code className="font-mono text-slate-600">{result.id}</code>
                </span>
                <div className="flex gap-3">
                  <button
                    onClick={handleReset}
                    className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm transition-all shadow-md shadow-emerald-200"
                  >
                    Diagnose Another Leaf
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

