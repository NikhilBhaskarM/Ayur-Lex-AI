import React, { useState } from 'react';
import {
  ShieldCheck,
  Leaf,
  Search,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  FileCheck2,
} from 'lucide-react';

const ABSCompliance: React.FC = () => {
  const [material, setMaterial] = useState('');
  const [purpose, setPurpose] = useState('');
  const [analyzed, setAnalyzed] = useState(false);

  const handleAnalyze = () => {
    if (!material.trim()) return;
    setAnalyzed(true);
  };

  return (
    <div className="space-y-6">

      {/* Hero */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-teal-950 to-emerald-900 p-8 text-white shadow-xl">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 text-emerald-300 text-sm font-semibold mb-3">
              <ShieldCheck size={18} />
              BIODIVERSITY • ABS COMPLIANCE
            </div>

            <h1 className="text-3xl lg:text-4xl font-bold tracking-tight">
              Access & Benefit-Sharing
            </h1>

            <p className="mt-3 max-w-2xl text-slate-300 leading-relaxed">
              Assess whether your Ayurvedic research, formulation or commercial
              activity may trigger biodiversity and benefit-sharing requirements.
            </p>
          </div>

          <div className="hidden lg:flex h-20 w-20 rounded-2xl bg-white/10 border border-white/10 items-center justify-center">
            <Leaf size={40} className="text-emerald-300" />
          </div>
        </div>
      </section>

      {/* Input */}
      <section className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-700">
            <Search size={22} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">
              Biodiversity Assessment
            </h2>
            <p className="text-sm text-slate-500">
              Describe the biological resource or activity.
            </p>
          </div>
        </div>

        <div className="space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Biological resource / ingredient
            </label>

            <textarea
              value={material}
              onChange={(e) => setMaterial(e.target.value)}
              placeholder="Example: Ashwagandha roots sourced from Karnataka..."
              rows={4}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Intended purpose
            </label>

            <input
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              placeholder="Research, product development, commercialisation..."
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
            />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!material.trim()}
            className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <ShieldCheck size={18} />
            Assess ABS Requirements
            <ArrowRight size={17} />
          </button>
        </div>
      </section>

      {/* Result */}
      {analyzed && (
        <section className="space-y-5">

          <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
            <div className="flex gap-4">
              <AlertTriangle className="text-amber-600 shrink-0" size={24} />

              <div>
                <h3 className="font-bold text-amber-900">
                  Preliminary ABS assessment
                </h3>

                <p className="text-sm text-amber-800 mt-1">
                  The described activity may involve India's biodiversity
                  access and benefit-sharing framework. Further factual and
                  jurisdictional verification is recommended.
                </p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-5">

            <div className="card">
              <CheckCircle2 className="text-emerald-600 mb-4" size={26} />
              <h3 className="font-bold text-slate-900">
                Resource Identified
              </h3>
              <p className="text-sm text-slate-500 mt-2">
                Biological material has been identified for compliance review.
              </p>
            </div>

            <div className="card">
              <FileCheck2 className="text-blue-600 mb-4" size={26} />
              <h3 className="font-bold text-slate-900">
                Documentation
              </h3>
              <p className="text-sm text-slate-500 mt-2">
                Maintain sourcing, purpose and utilisation records for review.
              </p>
            </div>

            <div className="card">
              <ShieldCheck className="text-purple-600 mb-4" size={26} />
              <h3 className="font-bold text-slate-900">
                Compliance Review
              </h3>
              <p className="text-sm text-slate-500 mt-2">
                Verify applicable approvals and benefit-sharing obligations.
              </p>
            </div>

          </div>

          <div className="card">
            <h3 className="font-bold text-slate-900 mb-4">
              Recommended next steps
            </h3>

            <div className="space-y-3">
              {[
                'Confirm the source and nature of the biological resource.',
                'Determine the purpose of access and intended commercial use.',
                'Check applicable biodiversity authority requirements.',
                'Maintain evidence and documentation for compliance review.',
              ].map((step, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-50"
                >
                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-teal-100 text-teal-700 text-sm font-bold">
                    {index + 1}
                  </span>

                  <p className="text-sm text-slate-600 pt-1">
                    {step}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </section>
      )}

      <p className="text-xs text-slate-400 text-center px-4">
        AI-generated assessment for informational purposes only. Verify
        applicable laws, regulations and official requirements before acting.
      </p>
    </div>
  );
};

export default ABSCompliance;