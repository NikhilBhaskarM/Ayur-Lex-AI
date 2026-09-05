import React, { useState } from 'react';
import {
  Sparkles,
  ShieldCheck,
  FileText,
  Lightbulb,
  Search,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  RotateCcw,
  Scale,
  Brain,
} from 'lucide-react';

const IPAssessment: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [innovation, setInnovation] = useState('');
  const [assessed, setAssessed] = useState(false);

  const handleAssess = () => {
    if (!title.trim() || !description.trim()) return;
    setAssessed(true);
  };

  const reset = () => {
    setTitle('');
    setDescription('');
    setInnovation('');
    setAssessed(false);
  };

  return (
    <div className="space-y-6 pb-10">

      {/* HERO */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-teal-950 to-emerald-900 p-7 sm:p-9 text-white shadow-xl">
        <div className="absolute -right-20 -top-24 h-72 w-72 rounded-full bg-teal-400/10 blur-3xl" />
        <div className="absolute -bottom-24 right-20 h-56 w-56 rounded-full bg-emerald-400/10 blur-3xl" />

        <div className="relative max-w-4xl">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-1.5 text-xs font-semibold text-teal-200">
            <Sparkles size={14} />
            AI-POWERED IP INTELLIGENCE
          </div>

          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Patent & IP Assessment
          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
            Evaluate your Ayurvedic innovation for potential intellectual
            property protection, prior-art considerations and documentation
            requirements.
          </p>

          <div className="mt-6 flex flex-wrap gap-2">
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-slate-200">
              Patentability
            </span>
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-slate-200">
              Prior Art
            </span>
            <span className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-slate-200">
              Traditional Knowledge
            </span>
          </div>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-5">

        {/* FORM */}
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-3">

          <div className="mb-7 flex items-start gap-3">
            <div className="rounded-xl bg-teal-50 p-3 text-teal-700">
              <FileText size={22} />
            </div>

            <div>
              <h2 className="text-xl font-bold text-slate-900">
                Describe your innovation
              </h2>
              <p className="mt-1 text-sm text-slate-500">
                Provide enough detail for a meaningful preliminary assessment.
              </p>
            </div>
          </div>

          <div className="space-y-5">

            {/* TITLE */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                Innovation / invention title
              </label>

              <input
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Novel herbal formulation for..."
                className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            {/* DESCRIPTION */}
            <div>
              <div className="mb-2 flex items-center justify-between">
                <label className="block text-sm font-semibold text-slate-700">
                  Invention description
                </label>

                <span className="text-[11px] text-slate-400">
                  Required
                </span>
              </div>

              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={7}
                placeholder="Describe the formulation, process, composition, technology or method..."
                className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            {/* INNOVATION */}
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">
                What is innovative about it?
                <span className="ml-2 font-normal text-slate-400">
                  Optional
                </span>
              </label>

              <textarea
                value={innovation}
                onChange={(e) => setInnovation(e.target.value)}
                rows={4}
                placeholder="Explain what makes this different from existing solutions..."
                className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
              />
            </div>

            <button
              onClick={handleAssess}
              disabled={!title.trim() || !description.trim()}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 px-5 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <Sparkles size={17} />
              Run IP Assessment
              <ArrowRight size={17} />
            </button>

          </div>
        </section>

        {/* RESULT */}
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">

          {!assessed ? (
            <div className="flex min-h-[500px] flex-col items-center justify-center text-center">

              <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-600">
                <Brain size={30} />
              </div>

              <h3 className="text-lg font-bold text-slate-900">
                IP assessment workspace
              </h3>

              <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                Enter your innovation details to generate a preliminary
                IP assessment.
              </p>

              <div className="mt-7 grid w-full grid-cols-2 gap-3 text-left">

                {[
                  {
                    icon: Search,
                    title: 'Prior Art',
                    color: 'text-teal-600',
                    bg: 'bg-teal-50',
                  },
                  {
                    icon: ShieldCheck,
                    title: 'Protection',
                    color: 'text-emerald-600',
                    bg: 'bg-emerald-50',
                  },
                  {
                    icon: FileText,
                    title: 'Evidence',
                    color: 'text-blue-600',
                    bg: 'bg-blue-50',
                  },
                  {
                    icon: Lightbulb,
                    title: 'Novelty',
                    color: 'text-amber-500',
                    bg: 'bg-amber-50',
                  },
                ].map((item) => {
                  const Icon = item.icon;

                  return (
                    <div
                      key={item.title}
                      className="rounded-xl border border-slate-100 bg-slate-50 p-3"
                    >
                      <div className={`inline-flex rounded-lg p-2 ${item.bg}`}>
                        <Icon size={17} className={item.color} />
                      </div>

                      <p className="mt-2 text-xs font-semibold text-slate-700">
                        {item.title}
                      </p>
                    </div>
                  );
                })}

              </div>
            </div>
          ) : (
            <div>

              <div className="mb-6 flex items-start justify-between">
                <div>
                  <p className="text-xs font-bold uppercase tracking-widest text-teal-600">
                    Preliminary Assessment
                  </p>

                  <h3 className="mt-1 text-xl font-bold text-slate-900">
                    IP Protection Analysis
                  </h3>
                </div>

                <button
                  onClick={reset}
                  title="Start again"
                  className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-500 transition hover:bg-slate-50 hover:text-slate-800"
                >
                  <RotateCcw size={15} />
                </button>
              </div>

              {/* RESULT */}
              <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
                <div className="flex items-start gap-3">
                  <CheckCircle2
                    size={22}
                    className="mt-0.5 shrink-0 text-emerald-600"
                  />

                  <div>
                    <p className="text-xs font-bold uppercase tracking-wide text-emerald-700">
                      Preliminary result
                    </p>

                    <p className="mt-1 text-lg font-bold text-emerald-900">
                      Potential IP protection identified
                    </p>

                    <p className="mt-2 text-xs leading-5 text-emerald-800">
                      The innovation may warrant further patentability and
                      prior-art analysis.
                    </p>
                  </div>
                </div>
              </div>

              {/* SCORE */}
              <div className="mt-5 rounded-2xl border border-slate-200 p-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-slate-700">
                    Preliminary IP strength
                  </span>

                  <span className="text-lg font-bold text-teal-700">
                    78%
                  </span>
                </div>

                <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full w-[78%] rounded-full bg-teal-600" />
                </div>

                <p className="mt-2 text-[11px] text-slate-400">
                  Indicative UI score — not a legal or patentability
                  determination.
                </p>
              </div>

              {/* ANALYSIS */}
              <div className="mt-5 space-y-3">

                <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
                  <Search
                    size={19}
                    className="mt-0.5 shrink-0 text-teal-600"
                  />

                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Prior-art search
                    </p>

                    <p className="mt-1 text-xs leading-5 text-slate-500">
                      Search relevant patent databases and existing
                      publications before filing.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-xl border border-slate-200 p-4">
                  <ShieldCheck
                    size={19}
                    className="mt-0.5 shrink-0 text-emerald-600"
                  />

                  <div>
                    <p className="text-sm font-semibold text-slate-800">
                      Patent considerations
                    </p>

                    <p className="mt-1 text-xs leading-5 text-slate-500">
                      Evaluate novelty, inventive step and applicable
                      exclusions.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4">
                  <AlertTriangle
                    size={19}
                    className="mt-0.5 shrink-0 text-amber-600"
                  />

                  <div>
                    <p className="text-sm font-semibold text-amber-900">
                      Traditional knowledge check
                    </p>

                    <p className="mt-1 text-xs leading-5 text-amber-700">
                      Determine whether the knowledge or formulation has
                      existing traditional-use documentation.
                    </p>
                  </div>
                </div>

              </div>

              <button className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-teal-200 bg-teal-50 px-4 py-3 text-sm font-semibold text-teal-700 transition hover:bg-teal-100">
                <Scale size={16} />
                View detailed IP report
                <ArrowRight size={16} />
              </button>

            </div>
          )}

        </section>
      </div>

      {/* DISCLAIMER */}
      <div className="flex items-start gap-3 rounded-2xl border border-amber-100 bg-white p-5 shadow-sm">
        <AlertTriangle
          size={18}
          className="mt-0.5 shrink-0 text-amber-500"
        />

        <div>
          <p className="text-sm font-semibold text-slate-800">
            Important
          </p>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            This assessment provides preliminary AI-assisted intelligence and
            does not constitute a legal opinion, patentability determination,
            or professional legal advice.
          </p>
        </div>
      </div>

    </div>
  );
};

export default IPAssessment;