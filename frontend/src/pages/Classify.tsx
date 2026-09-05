import React, { useState } from 'react';
import {
  Sparkles,
  Leaf,
  ShieldCheck,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  RotateCcw,
  FileText,
} from 'lucide-react';

const Classify: React.FC = () => {
  const [formulation, setFormulation] = useState('');
  const [ingredients, setIngredients] = useState('');
  const [purpose, setPurpose] = useState('');
  const [result, setResult] = useState(false);

  const handleAnalyze = () => {
    if (!formulation.trim() || !ingredients.trim()) return;
    setResult(true);
  };

  const handleReset = () => {
    setFormulation('');
    setIngredients('');
    setPurpose('');
    setResult(false);
  };

  return (
    <div className="space-y-6">

      {/* Hero */}
      <div className="overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-teal-900 to-emerald-900 p-6 text-white shadow-lg sm:p-8">
        <div className="flex flex-col justify-between gap-6 lg:flex-row lg:items-center">
          <div className="max-w-2xl">
            <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-1 text-xs font-medium text-teal-100">
              <Sparkles size={13} />
              AI Regulatory Classification
            </div>

            <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
              Formulation Classification
            </h1>

            <p className="mt-3 text-sm leading-6 text-slate-300">
              Analyze an Ayurvedic formulation and understand its likely
              regulatory category, compliance considerations, and next steps.
            </p>
          </div>

          <div className="hidden h-20 w-20 items-center justify-center rounded-2xl bg-white/10 lg:flex">
            <Leaf size={38} className="text-emerald-300" />
          </div>
        </div>
      </div>

      {/* Main */}
      <div className="grid gap-6 lg:grid-cols-5">

        {/* Input panel */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-3">
          <div className="mb-6">
            <h2 className="text-lg font-bold text-slate-900">
              Tell us about your formulation
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              Provide the available details. More information improves the
              assessment.
            </p>
          </div>

          <div className="space-y-5">

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Formulation name
              </label>

              <input
                value={formulation}
                onChange={(e) => setFormulation(e.target.value)}
                placeholder="e.g. Ashwagandha Herbal Capsules"
                className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Ingredients / composition
              </label>

              <textarea
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value)}
                rows={5}
                placeholder="Enter ingredients, quantities, extracts, minerals, plant materials..."
                className="w-full resize-none rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Intended purpose
                <span className="ml-2 font-normal text-slate-400">
                  Optional
                </span>
              </label>

              <textarea
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
                rows={3}
                placeholder="What is the intended use or claimed benefit?"
                className="w-full resize-none rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={!formulation.trim() || !ingredients.trim()}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <Sparkles size={17} />
              Analyze Formulation
              <ArrowRight size={17} />
            </button>

          </div>
        </div>

        {/* Result panel */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">

          {!result ? (
            <div className="flex h-full min-h-[420px] flex-col items-center justify-center text-center">
              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-600">
                <FileText size={28} />
              </div>

              <h3 className="font-bold text-slate-900">
                Assessment ready
              </h3>

              <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                Enter your formulation details and run the AI analysis to see
                the regulatory assessment here.
              </p>

              <div className="mt-6 flex flex-wrap justify-center gap-2">
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                  Classification
                </span>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                  Compliance
                </span>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                  Evidence
                </span>
              </div>
            </div>
          ) : (
            <div>
              <div className="mb-6 flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-teal-600">
                    AI Assessment
                  </p>

                  <h3 className="mt-1 text-xl font-bold text-slate-900">
                    Preliminary Classification
                  </h3>
                </div>

                <button
                  onClick={handleReset}
                  className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50"
                  title="Reset"
                >
                  <RotateCcw size={15} />
                </button>
              </div>

              {/* Classification */}
              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 text-emerald-600">
                    <CheckCircle2 size={20} />
                  </div>

                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-emerald-700">
                      Likely category
                    </p>

                    <p className="mt-1 text-lg font-bold text-emerald-900">
                      Ayurvedic / Traditional Medicine Product
                    </p>

                    <p className="mt-2 text-xs leading-5 text-emerald-800">
                      Preliminary AI classification based on the information
                      provided.
                    </p>
                  </div>
                </div>
              </div>

              {/* Confidence */}
              <div className="mt-5">
                <div className="mb-2 flex justify-between">
                  <span className="text-xs font-semibold text-slate-600">
                    AI confidence
                  </span>
                  <span className="text-xs font-bold text-teal-700">
                    86%
                  </span>
                </div>

                <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full w-[86%] rounded-full bg-teal-600" />
                </div>
              </div>

              {/* Checks */}
              <div className="mt-6 space-y-3">
                <div className="flex items-center gap-3 rounded-xl border border-slate-200 p-3">
                  <ShieldCheck size={18} className="text-emerald-600" />
                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Regulatory review
                    </p>
                    <p className="text-xs text-slate-500">
                      Further verification recommended
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-xl border border-slate-200 p-3">
                  <Leaf size={18} className="text-teal-600" />
                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Traditional knowledge
                    </p>
                    <p className="text-xs text-slate-500">
                      Check TK and prior-art considerations
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 p-3">
                  <AlertTriangle size={18} className="text-amber-600" />
                  <div>
                    <p className="text-sm font-semibold text-amber-900">
                      Professional verification
                    </p>
                    <p className="text-xs text-amber-700">
                      AI output is not a legal determination
                    </p>
                  </div>
                </div>
              </div>

              <button className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700 transition hover:bg-teal-100">
                View detailed assessment
                <ArrowRight size={16} />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Bottom trust section */}
      <div className="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100">
            <ShieldCheck size={17} className="text-slate-600" />
          </div>

          <div>
            <p className="text-sm font-semibold text-slate-800">
              Evidence-backed intelligence
            </p>
            <p className="text-xs text-slate-500">
              Results should be reviewed against applicable laws and official
              regulatory sources.
            </p>
          </div>
        </div>

        <span className="text-xs font-medium text-slate-400">
          AyurLegal AI
        </span>
      </div>
    </div>
  );
};

export default Classify;