import React from 'react';
import { 
  Sprout, 
  BookOpen, 
  Cpu, 
  Database, 
  ShieldCheck, 
  Award, 
  CheckCircle,
  ExternalLink
} from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="py-10 bg-slate-50 min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
        {/* Title */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-semibold">
            <BookOpen className="w-3.5 h-3.5 text-emerald-600" />
            Project Documentation
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            About PlantCare AI
          </h1>
          <p className="text-sm text-slate-500 max-w-xl mx-auto">
            Intelligent Plant Disease Detection System using Deep Convolutional Neural Networks and Integrated Agronomic Pest Management.
          </p>
        </div>

        {/* Section 1: Motivation & Problem Statement */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-emerald-700 font-bold text-base">
            <Sprout className="w-5 h-5" />
            <h3>Project Motivation & Agricultural Impact</h3>
          </div>
          <p className="text-sm text-slate-600 leading-relaxed">
            Foliar plant diseases caused by fungal, oomycete, bacterial, and viral pathogens result in an estimated 20% to 40% reduction in global crop yields annually. In traditional farming communities, access to professional plant pathologists is often limited, leading to delayed disease identification or inappropriate chemical applications.
          </p>
          <p className="text-sm text-slate-600 leading-relaxed">
            <strong>PlantCare AI</strong> addresses this challenge by providing instantaneous, automated, and accurate pathological classification from ordinary mobile leaf photographs. Furthermore, the platform bridges the gap between diagnosis and action by delivering dual management recommendations: environmentally friendly biological controls and targeted chemical treatments.
          </p>
        </div>

        {/* Section 2: Deep Learning Methodology */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-emerald-700 font-bold text-base">
            <Cpu className="w-5 h-5" />
            <h3>Deep Learning Methodology</h3>
          </div>
          <p className="text-sm text-slate-600 leading-relaxed">
            The core diagnostic engine implements a Convolutional Neural Network (CNN) architecture designed specifically for microscopic and macroscopic lesion pattern recognition:
          </p>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-700">
            <li className="p-3 bg-slate-50 rounded-lg border border-slate-100 space-y-1">
              <span className="font-bold text-slate-900 block">Feature Extraction</span>
              <span>Hierarchical 2D convolutions with 32, 64, and 128 feature channels extract edges, textures, and concentric rings.</span>
            </li>
            <li className="p-3 bg-slate-50 rounded-lg border border-slate-100 space-y-1">
              <span className="font-bold text-slate-900 block">Batch Normalization</span>
              <span>Stabilizes intermediate activation distributions, preventing vanishing gradients and speeding convergence.</span>
            </li>
            <li className="p-3 bg-slate-50 rounded-lg border border-slate-100 space-y-1">
              <span className="font-bold text-slate-900 block">Dropout & Regularization</span>
              <span>35% stochastic dropout prevents neuron co-adaptation, ensuring robust generalization to unconstrained field photos.</span>
            </li>
            <li className="p-3 bg-slate-50 rounded-lg border border-slate-100 space-y-1">
              <span className="font-bold text-slate-900 block">Low-Confidence Gating</span>
              <span>Threshold-based validation flags ambiguous images or non-leaf objects rather than producing false diagnoses.</span>
            </li>
          </ul>
        </div>

        {/* Section 3: Dataset Benchmark */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center gap-2 text-emerald-700 font-bold text-base">
            <Database className="w-5 h-5" />
            <h3>PlantVillage Dataset Benchmark</h3>
          </div>
          <p className="text-sm text-slate-600 leading-relaxed">
            The system benchmarks against the internationally recognized <strong>PlantVillage</strong> dataset (Hughes & Salathé, Penn State University). Images undergo a rigorous preparation pipeline:
          </p>
          <div className="space-y-2 text-xs text-slate-600">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              <span><strong>Deduplication Guard:</strong> MD5 perceptual hashes filter duplicate or near-identical images to prevent train-test data leakage.</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              <span><strong>Reproducible Split:</strong> Strict 70% training, 15% validation, and 15% testing splits generated with fixed random seeds.</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-emerald-600" />
              <span><strong>Standardized Resizing:</strong> Resampling to 128x128 pixels preserves pathological lesion morphology while ensuring ultra-low inference latency (&lt;50ms).</span>
            </div>
          </div>
        </div>

        {/* Section 4: Academic Demonstration Guidelines */}
        <div className="bg-gradient-to-tr from-slate-900 to-emerald-950 rounded-2xl p-6 sm:p-8 text-white space-y-4">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-base">
            <Award className="w-5 h-5" />
            <h3>Academic Mini-Project Demonstration Guide</h3>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            This project is engineered to provide an end-to-end demonstrable machine learning web application suitable for academic project defense and evaluation:
          </p>
          <ol className="list-decimal list-inside space-y-1.5 text-xs text-slate-200 font-medium">
            <li><strong>Live Foliar Diagnosis:</strong> Navigate to <em>Diagnose Leaf</em> and upload sample leaf photos across various crops.</li>
            <li><strong>Agronomic Prescriptions:</strong> Observe organic bio-fungicides and chemical treatments populated dynamically.</li>
            <li><strong>Interactive Visualizations:</strong> Inspect the <em>Analytics Dashboard</em> for live epidemic distribution charts.</li>
            <li><strong>Model Benchmarks:</strong> Review the <em>Model Info</em> page for layer architectures and regularizer comparison tables.</li>
            <li><strong>Audit Logging:</strong> Inspect <em>History</em> for time-stamped visual audit trails and SQLite/Firebase persistence.</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

