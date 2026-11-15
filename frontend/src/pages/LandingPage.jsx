import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Sprout, 
  UploadCloud, 
  Cpu, 
  FileText, 
  ShieldCheck, 
  CheckCircle2, 
  ArrowRight, 
  Layers, 
  Activity, 
  Database,
  BarChart3,
  Leaf
} from 'lucide-react';

export default function LandingPage() {
  const supportedCrops = [
    { name: 'Tomato', count: '3 Conditions', color: 'from-red-500/20 to-orange-500/10 text-red-700 border-red-200' },
    { name: 'Potato', count: '3 Conditions', color: 'from-amber-500/20 to-yellow-500/10 text-amber-800 border-amber-200' },
    { name: 'Corn (Maize)', count: '3 Conditions', color: 'from-yellow-500/20 to-amber-500/10 text-yellow-800 border-yellow-200' },
    { name: 'Apple', count: '3 Conditions', color: 'from-emerald-500/20 to-green-500/10 text-emerald-800 border-emerald-200' },
    { name: 'Grape', count: '2 Conditions', color: 'from-purple-500/20 to-indigo-500/10 text-purple-800 border-purple-200' },
  ];

  const steps = [
    {
      num: '01',
      title: 'Upload Foliage Photo',
      desc: 'Capture or drag-and-drop a close-up image of a plant leaf showing visible symptoms or healthy foliage.',
      icon: UploadCloud,
    },
    {
      num: '02',
      title: 'Neural Feature Extraction',
      desc: 'Our Deep CNN inspects lesions, discoloration patterns, and fungal pustules across 128x128 feature layers.',
      icon: Cpu,
    },
    {
      num: '03',
      title: 'Actionable Pathology Plan',
      desc: 'Receive immediate confidence metrics, organic bio-treatments, chemical fungicides, and prevention protocols.',
      icon: ShieldCheck,
    },
  ];

  const capabilities = [
    {
      title: 'Convolutional Deep Learning',
      desc: 'Trained using multi-layer 2D Convolutions, Batch Normalization, and Dropout to classify foliar pathogens accurately.',
      icon: Layers,
    },
    {
      title: 'Agronomic Treatment Protocols',
      desc: 'Every diagnosis provides dual recommendations: organic biological controls and licensed chemical interventions.',
      icon: Leaf,
    },
    {
      title: 'Persistent Outbreak Tracking',
      desc: 'Securely catalog every detection with time-stamped visual records, confidence scores, and crop trend charts.',
      icon: Database,
    },
    {
      title: 'Low-Confidence Safeguards',
      desc: 'Autonomous threshold verification flags ambiguous photos or non-leaf objects rather than producing false diagnoses.',
      icon: CheckCircle2,
    },
  ];

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-emerald-50/70 via-white to-slate-50 pt-16 pb-20 lg:pt-24 lg:pb-28 border-b border-emerald-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-100/80 border border-emerald-300/60 text-emerald-800 text-xs font-semibold tracking-wide shadow-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              AI-Powered Agricultural Diagnostics
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Detect Plant Diseases <br className="hidden sm:inline" />
              <span className="bg-gradient-to-r from-emerald-600 via-teal-600 to-green-700 bg-clip-text text-transparent">
                Instantly with Deep Learning
              </span>
            </h1>

            <p className="text-base sm:text-lg text-slate-600 leading-relaxed font-normal">
              PlantCare AI leverages Convolutional Neural Networks to diagnose crop foliar diseases from ordinary photos. Protect harvest yields with instantaneous, scientifically backed agronomic management plans.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
              <Link
                to="/detect"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-base shadow-lg shadow-emerald-200 transition-all hover:-translate-y-0.5"
              >
                <Sprout className="w-5 h-5" />
                Diagnose Leaf Now
                <ArrowRight className="w-4 h-4 ml-1" />
              </Link>
              <Link
                to="/dashboard"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-semibold text-base border border-slate-200 shadow-sm transition-colors"
              >
                <BarChart3 className="w-5 h-5 text-emerald-600" />
                View Analytics
              </Link>
            </div>

            {/* Supported Crops Badges */}
            <div className="pt-6">
              <span className="text-xs uppercase font-semibold text-slate-400 tracking-wider block mb-3">
                Supported Agricultural Crops
              </span>
              <div className="flex flex-wrap justify-center gap-2">
                {supportedCrops.map((crop) => (
                  <span
                    key={crop.name}
                    className={`px-3 py-1 rounded-lg text-xs font-medium border bg-gradient-to-r ${crop.color}`}
                  >
                    {crop.name} • <span className="opacity-75">{crop.count}</span>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-white border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-xs font-bold text-emerald-600 uppercase tracking-widest mb-2">Workflow Pipeline</h2>
            <p className="text-3xl font-extrabold text-slate-900 tracking-tight">How PlantCare AI Operates</p>
            <p className="text-slate-500 text-sm mt-2">From raw mobile leaf snapshot to integrated treatment protocol in 3 steps.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            {steps.map((step, idx) => (
              <div
                key={step.num}
                className="relative bg-slate-50/70 rounded-2xl p-7 border border-slate-200/80 hover:border-emerald-300 hover:shadow-md transition-all group"
              >
                <div className="flex items-center justify-between mb-5">
                  <div className="w-12 h-12 rounded-xl bg-emerald-100/80 text-emerald-700 flex items-center justify-center group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                    <step.icon className="w-6 h-6" />
                  </div>
                  <span className="text-2xl font-black text-slate-300 group-hover:text-emerald-500/50 transition-colors">
                    {step.num}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{step.title}</h3>
                <p className="text-sm text-slate-600 leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="py-20 bg-slate-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-xs font-bold text-emerald-600 uppercase tracking-widest mb-2">Deep Tech Architecture</h2>
            <p className="text-3xl font-extrabold text-slate-900 tracking-tight">Enterprise-Grade Plant Pathology</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {capabilities.map((cap, i) => (
              <div key={i} className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm space-y-3">
                <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
                  <cap.icon className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-slate-900 text-base">{cap.title}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{cap.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology & Frameworks Banner */}
      <section className="py-14 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-slate-900 via-emerald-950 to-slate-900 rounded-3xl p-8 sm:p-12 text-white shadow-xl relative overflow-hidden">
            <div className="relative z-10 max-w-2xl space-y-4">
              <span className="text-xs font-bold uppercase tracking-widest text-emerald-400">Robust Tech Stack</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                Designed for Field Performance & College-Level Demonstration
              </h2>
              <p className="text-sm text-slate-300 leading-relaxed">
                Constructed using React 19, Tailwind CSS, Flask REST API, TensorFlow/Keras CNNs, and dual-mode Firebase / SQLite persistence.
              </p>
              <div className="pt-2 flex flex-wrap gap-3">
                <Link
                  to="/detect"
                  className="px-5 py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-sm transition-colors"
                >
                  Start Diagnosing
                </Link>
                <Link
                  to="/model-info"
                  className="px-5 py-2.5 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold text-sm transition-colors border border-white/10"
                >
                  View Model Architecture
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

