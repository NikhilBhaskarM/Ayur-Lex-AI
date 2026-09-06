import React, { useState } from 'react';
import {
  Activity,
  Calculator,
  FileText,
  AlertTriangle,
  CheckCircle2,
  Copy,
  Download,
  Plus,
  Trash2,
  ArrowRight,
  Scale,
  Sparkles
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface ComponentInput {
  name: string;
  dose_in_combination: number;
  dose_alone: number;
  unit: string;
}

interface SynergyResult {
  formulation_name: string;
  combination_index: number;
  classification: string;
  section_3e_status: string;
  patentability_adjudication: string;
  pharmacological_explanation: string;
  recommended_claim_clause: string;
  isobologram_coordinates: Array<{
    component: string;
    d_combination: number;
    d_alone: number;
    ratio_fraction: number;
    unit: string;
  }>;
  statutory_precedents: string[];
}

interface FERResult {
  application_number: string;
  detected_objections: Array<{
    statute: string;
    objection_type: string;
    severity: string;
    grounds: string;
  }>;
  statutory_summary: string;
  formal_written_rebuttal: string;
  proposed_claim_amendments: string[];
  case_law_authorities: string[];
}

const SAMPLE_FER_TEXT = `The claims 1 to 8 lack inventive step and are non-patentable.
Objection 1: The claimed formulation comprising Curcuma longa and Piper nigrum falls within the statutory bar of Section 3(p) of the Patents Act, 1970, being an aggregation of traditional knowledge documented in classical texts and TKDL.
Objection 2: The claims fall under Section 3(e) as being a mere admixture of known substances resulting only in the aggregation of the properties of the components thereof. The applicant has failed to provide experimental comparative synergy data.
Objection 3: The application lacks permission on Form III from the National Biodiversity Authority under Section 6 of the Biological Diversity Act, 2002.`;

const SynergyCalculator: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'synergy' | 'fer'>('synergy');

  // Synergy state
  const [formulationName, setFormulationName] = useState('Curcumin + Piperine Bio-Enhanced Complex');
  const [components, setComponents] = useState<ComponentInput[]>([
    { name: 'Curcumin (Curcuma longa extract)', dose_in_combination: 50, dose_alone: 200, unit: 'mg/kg' },
    { name: 'Piperine (Piper nigrum bio-enhancer)', dose_in_combination: 5, dose_alone: 50, unit: 'mg/kg' }
  ]);
  const [synergyLoading, setSynergyLoading] = useState(false);
  const [synergyResult, setSynergyResult] = useState<SynergyResult | null>(null);

  // FER state
  const [ferText, setFerText] = useState(SAMPLE_FER_TEXT);
  const [appNumber, setAppNumber] = useState('202441012345');
  const [applicantName, setApplicantName] = useState('Herbal Bio-Pharma Pvt. Ltd.');
  const [ferLoading, setFerLoading] = useState(false);
  const [ferResult, setFerResult] = useState<FERResult | null>(null);

  const addComponent = () => {
    setComponents([
      ...components,
      { name: '', dose_in_combination: 10, dose_alone: 50, unit: 'mg/kg' }
    ]);
  };

  const removeComponent = (idx: number) => {
    if (components.length <= 2) {
      toast.error('Minimum 2 components required for combination index');
      return;
    }
    setComponents(components.filter((_, i) => i !== idx));
  };

  const updateComponent = (idx: number, field: keyof ComponentInput, value: any) => {
    const updated = [...components];
    updated[idx] = { ...updated[idx], [field]: value };
    setComponents(updated);
  };

  const handleCalculateSynergy = async () => {
    setSynergyLoading(true);
    try {
      const response = await axios.post('/api/analytics/synergy-check', {
        formulation_name: formulationName,
        components
      });
      setSynergyResult(response.data);
      toast.success(`CI = ${response.data.combination_index} calculated`);
    } catch (err) {
      console.error('Synergy calculation failed:', err);
      // Client-side fallback calculation
      const ci = components.reduce((sum, c) => sum + (c.dose_in_combination / c.dose_alone), 0);
      const roundedCI = Math.round(ci * 1000) / 1000;
      setSynergyResult({
        formulation_name: formulationName,
        combination_index: roundedCI,
        classification: roundedCI < 0.85 ? 'Strong Synergism (Supra-Additive Interaction)' : 'Additive Effect (Mere Admixture Risk)',
        section_3e_status: roundedCI < 0.85 ? 'CLEARED / LOW REJECTION RISK' : 'HIGH SECTION 3(e) REJECTION RISK',
        patentability_adjudication: roundedCI < 0.85
          ? `Combination Index CI = ${roundedCI} proves supra-additive synergism overcoming Section 3(e).`
          : `Combination Index CI = ${roundedCI} indicates simple additivity subject to Section 3(e) mere admixture bar.`,
        pharmacological_explanation: 'Calculated using Chou-Talalay median-effect equation under Section 3(e) standards.',
        recommended_claim_clause: `A synergistic composition of ${components.map(c => c.name).join(' and ')} characterized by CI < 1.0.`,
        isobologram_coordinates: components.map(c => ({
          component: c.name,
          d_combination: c.dose_in_combination,
          d_alone: c.dose_alone,
          ratio_fraction: c.dose_in_combination / c.dose_alone,
          unit: c.unit
        })),
        statutory_precedents: ['The Patents Act, 1970 — Section 3(e)', 'Biswanath Prasad Radhey Shyam v. Hindustan Metal Industries (1979)']
      });
    } finally {
      setSynergyLoading(false);
    }
  };

  const handleParseFER = async () => {
    if (!ferText.trim()) return;
    setFerLoading(true);
    try {
      const response = await axios.post('/api/fer/parse-and-counter', {
        fer_text: ferText,
        application_number: appNumber,
        applicant_name: applicantName,
        combination_index: synergyResult?.combination_index || 0.65
      });
      setFerResult(response.data);
      toast.success('FER parsed and formal rebuttal generated');
    } catch (err) {
      console.error('FER parsing failed:', err);
      toast.error('Could not connect to FER endpoint. Check server status.');
    } finally {
      setFerLoading(false);
    }
  };

  const copyToClipboard = (text: string, msg = 'Copied to clipboard!') => {
    navigator.clipboard.writeText(text);
    toast.success(msg);
  };

  return (
    <div className="space-y-8 pb-16">
      {/* HERO */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-teal-950 to-indigo-950 p-8 text-white shadow-2xl border border-teal-800/30">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 text-xs font-bold tracking-widest uppercase mb-3">
              <Activity className="h-4 w-4" />
              Quantitative Section 3(e) Pharmacology & Rebuttal Suite
            </div>
            <h1 className="text-3xl lg:text-4xl font-black tracking-tight">
              Synergy Calculator & FER Rebuttal
            </h1>
            <p className="mt-2 max-w-2xl text-slate-300 text-sm leading-relaxed">
              Scientifically calculate the Chou-Talalay Combination Index (CI &lt; 1.0) to defeat Section 3(e)
              mere admixture rejections, and auto-generate courtroom-grade written submissions to Indian Patent Office FERs.
            </p>
          </div>

          <div className="flex rounded-2xl bg-white/10 p-1.5 backdrop-blur border border-white/10">
            <button
              onClick={() => setActiveTab('synergy')}
              className={`flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl transition ${
                activeTab === 'synergy'
                  ? 'bg-teal-500 text-white shadow-lg'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <Calculator className="h-4 w-4" />
              Chou-Talalay Calculator
            </button>
            <button
              onClick={() => setActiveTab('fer')}
              className={`flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl transition ${
                activeTab === 'fer'
                  ? 'bg-teal-500 text-white shadow-lg'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              <FileText className="h-4 w-4" />
              FER Rebuttal Parser
            </button>
          </div>
        </div>
      </section>

      {/* TAB 1: CHOU-TALALAY SYNERGY CALCULATOR */}
      {activeTab === 'synergy' && (
        <section className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-100 pb-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900">
                  Combination Index ($CI$) Formulation Inputs
                </h2>
                <p className="text-xs text-slate-500">
                  Input single-agent doses ($D_x$) versus doses in combination ($D$) to establish supra-additivity.
                </p>
              </div>

              <button
                onClick={addComponent}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-teal-200 bg-teal-50 text-teal-700 text-xs font-bold hover:bg-teal-100 transition"
              >
                <Plus className="h-3.5 w-3.5" />
                Add Botanical Component
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Formulation Title
              </label>
              <input
                type="text"
                value={formulationName}
                onChange={(e) => setFormulationName(e.target.value)}
                className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
              />
            </div>

            {/* COMPONENTS LIST */}
            <div className="space-y-4">
              {components.map((comp, idx) => (
                <div key={idx} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/60 grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
                  <div className="md:col-span-4">
                    <label className="block text-[11px] font-bold text-slate-600 mb-1">
                      Component {idx + 1} Name / Marker
                    </label>
                    <input
                      type="text"
                      value={comp.name}
                      onChange={(e) => updateComponent(idx, 'name', e.target.value)}
                      placeholder="Herb or extract name"
                      className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium outline-none"
                    />
                  </div>

                  <div className="md:col-span-3">
                    <label className="block text-[11px] font-bold text-slate-600 mb-1">
                      Dose in Combination ($D$)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={comp.dose_in_combination}
                      onChange={(e) => updateComponent(idx, 'dose_in_combination', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium outline-none"
                    />
                  </div>

                  <div className="md:col-span-3">
                    <label className="block text-[11px] font-bold text-slate-600 mb-1">
                      Dose Alone for Same Effect ($D_x$)
                    </label>
                    <input
                      type="number"
                      step="any"
                      value={comp.dose_alone}
                      onChange={(e) => updateComponent(idx, 'dose_alone', parseFloat(e.target.value) || 0)}
                      className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium outline-none"
                    />
                  </div>

                  <div className="md:col-span-1">
                    <label className="block text-[11px] font-bold text-slate-600 mb-1">
                      Unit
                    </label>
                    <input
                      type="text"
                      value={comp.unit}
                      onChange={(e) => updateComponent(idx, 'unit', e.target.value)}
                      className="w-full px-2 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium text-center outline-none"
                    />
                  </div>

                  <div className="md:col-span-1 flex justify-end">
                    <button
                      onClick={() => removeComponent(idx)}
                      className="p-2 text-slate-400 hover:text-rose-600 rounded-lg transition"
                      title="Remove component"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleCalculateSynergy}
              disabled={synergyLoading}
              className="w-full py-4 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-sm shadow-lg shadow-teal-950/20 transition flex items-center justify-center gap-2"
            >
              {synergyLoading ? 'Executing Chou-Talalay Equation...' : (
                <>
                  <Calculator className="h-4 w-4" />
                  Calculate Section 3(e) Combination Index
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>

          {/* SYNERGY RESULT CARD */}
          {synergyResult && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-md space-y-6">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-100 pb-5">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-widest text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
                    Chou-Talalay Analysis
                  </span>
                  <h3 className="text-xl font-bold text-slate-900 mt-2">
                    {synergyResult.classification}
                  </h3>
                  <p className="text-xs font-semibold text-slate-600 mt-1">
                    Status: <span className={synergyResult.combination_index < 1.0 ? 'text-emerald-600' : 'text-rose-600'}>{synergyResult.section_3e_status}</span>
                  </p>
                </div>

                <div className="text-right">
                  <span className="text-xs text-slate-400 font-semibold block">Combination Index ($CI$)</span>
                  <span className={`text-4xl font-black ${synergyResult.combination_index < 0.85 ? 'text-emerald-600' : synergyResult.combination_index <= 1.15 ? 'text-amber-600' : 'text-rose-600'}`}>
                    {synergyResult.combination_index}
                  </span>
                  <span className="text-[10px] text-slate-400 block mt-0.5 font-mono">
                    {synergyResult.combination_index < 1.0 ? 'CI < 1.0 (SYNERGY)' : 'CI >= 1.0 (NON-SYNERGY)'}
                  </span>
                </div>
              </div>

              {/* STATUTORY OPINION */}
              <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                  <Scale className="h-4 w-4 text-teal-600" />
                  Section 3(e) Legal Adjudication
                </h4>
                <p className="text-sm text-slate-700 leading-relaxed">
                  {synergyResult.patentability_adjudication}
                </p>
                <p className="text-xs text-slate-500 italic mt-1">
                  {synergyResult.pharmacological_explanation}
                </p>
              </div>

              {/* RECOMMENDED CLAIM CLAUSE */}
              <div className="p-5 rounded-2xl bg-teal-50/60 border border-teal-200 space-y-3">
                <div className="flex justify-between items-center">
                  <h4 className="text-xs font-bold text-teal-900 uppercase tracking-wider flex items-center gap-2">
                    <Sparkles className="h-4 w-4 text-teal-600" />
                    Recommended Patent Claim Phrasing
                  </h4>
                  <button
                    onClick={() => copyToClipboard(synergyResult.recommended_claim_clause, 'Claim clause copied!')}
                    className="flex items-center gap-1 text-xs font-bold text-teal-700 hover:text-teal-900 transition"
                  >
                    <Copy className="h-3.5 w-3.5" />
                    Copy Claim
                  </button>
                </div>
                <p className="text-xs font-serif text-slate-800 bg-white p-3 rounded-xl border border-teal-100 leading-relaxed">
                  "{synergyResult.recommended_claim_clause}"
                </p>
              </div>

              {/* RATIO CONTRIBUTIONS */}
              <div>
                <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
                  Individual Component Fractional Contributions
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {synergyResult.isobologram_coordinates.map((coord, i) => (
                    <div key={i} className="p-3 rounded-xl border border-slate-200 bg-slate-50 flex justify-between items-center">
                      <div>
                        <p className="text-xs font-bold text-slate-800">{coord.component}</p>
                        <p className="text-[11px] text-slate-500">
                          {coord.d_combination} / {coord.d_alone} {coord.unit}
                        </p>
                      </div>
                      <span className="text-xs font-mono font-bold text-teal-700 bg-teal-50 px-2 py-1 rounded border border-teal-200">
                        Fraction: {coord.ratio_fraction}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </section>
      )}

      {/* TAB 2: FER PARSER & REBUTTAL DRAFTER */}
      {activeTab === 'fer' && (
        <section className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <h2 className="text-lg font-bold text-slate-900">
                First Examination Report (FER) Parser & Counter-Argument Drafter
              </h2>
              <p className="text-xs text-slate-500">
                Paste objections from the Indian Patent Office to auto-generate a formal response under Rule 28.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Application Number
                </label>
                <input
                  type="text"
                  value={appNumber}
                  onChange={(e) => setAppNumber(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs font-medium outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Applicant Entity Name
                </label>
                <input
                  type="text"
                  value={applicantName}
                  onChange={(e) => setApplicantName(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-xs font-medium outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Pasted FER / Hearing Notice Objections *
              </label>
              <textarea
                rows={7}
                value={ferText}
                onChange={(e) => setFerText(e.target.value)}
                placeholder="Paste the Examiner's objections regarding Section 3(p), Section 3(e), etc..."
                className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 font-mono text-xs focus:bg-white focus:border-teal-500 outline-none transition"
              />
            </div>

            <button
              onClick={handleParseFER}
              disabled={ferLoading || !ferText.trim()}
              className="w-full py-4 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-sm shadow-lg shadow-teal-950/20 transition flex items-center justify-center gap-2"
            >
              {ferLoading ? 'Parsing Objections & Synthesizing Legal Brief...' : (
                <>
                  <FileText className="h-4 w-4" />
                  Parse FER & Draft Formal Written Rebuttal
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>

          {/* FER RESULTS */}
          {ferResult && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-md space-y-6">
              <div>
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">
                  Detected Statutory Objections ({ferResult.detected_objections.length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {ferResult.detected_objections.map((obj, i) => (
                    <div key={i} className="p-3.5 rounded-xl border border-rose-200 bg-rose-50/50 space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-xs font-bold text-rose-900">{obj.statute}</span>
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-700">
                          {obj.severity}
                        </span>
                      </div>
                      <p className="text-xs font-semibold text-slate-800">{obj.objection_type}</p>
                      <p className="text-[11px] text-slate-600">{obj.grounds}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* FORMAL REBUTTAL SUBMISSION */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                    <Scale className="h-4 w-4 text-teal-600" />
                    Formal Written Submission for the Controller of Patents
                  </h3>
                  <button
                    onClick={() => copyToClipboard(ferResult.formal_written_rebuttal, 'Written Submission copied!')}
                    className="flex items-center gap-1.5 text-xs font-bold text-teal-700 hover:text-teal-900 transition bg-teal-50 px-3 py-1.5 rounded-lg border border-teal-200"
                  >
                    <Copy className="h-3.5 w-3.5" />
                    Copy Rebuttal Brief
                  </button>
                </div>

                <pre className="p-5 rounded-2xl bg-slate-900 text-slate-100 font-mono text-xs whitespace-pre-wrap leading-relaxed overflow-x-auto border border-slate-800">
                  {ferResult.formal_written_rebuttal}
                </pre>
              </div>

              {/* PROPOSED AMENDMENTS */}
              <div className="p-5 rounded-2xl bg-emerald-50/60 border border-emerald-200">
                <h4 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-2">
                  Proposed Claim Amendments to Advance to Grant
                </h4>
                <ul className="space-y-2">
                  {ferResult.proposed_claim_amendments.map((amend, i) => (
                    <li key={i} className="text-xs text-emerald-800 flex items-start gap-2">
                      <span className="font-bold">{i + 1}.</span>
                      <span>{amend}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
};

export default SynergyCalculator;
