import React, { useState } from 'react';
import {
  ShieldCheck,
  Leaf,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  FileCheck2,
  Download,
  Copy,
  Globe,
  Building,
  Scale
} from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

interface ABSResponse {
  applicant_classification: string;
  governing_section: string;
  approval_authority: string;
  is_section_3_2_entity: boolean;
  mandatory_statutory_actions: string[];
  benefit_sharing_obligation: string;
  penal_provisions: string;
  nba_form_iii_prefill: any;
  compliance_status: string;
}

const ABSCompliance: React.FC = () => {
  const [applicantName, setApplicantName] = useState('Herbal Innovations India Pvt. Ltd.');
  const [applicantType, setApplicantType] = useState('company');
  const [hasForeignEquity, setHasForeignEquity] = useState(false);
  const [foreignEquityPct, setForeignEquityPct] = useState(0);
  const [country, setCountry] = useState('India');
  const [biologicalResources, setBiologicalResources] = useState('Withania somnifera, Curcuma longa, Piper nigrum');
  const [sourceState, setSourceState] = useState('Karnataka');
  const [patentTitle, setPatentTitle] = useState('Synergistic Polyherbal Anti-Inflammatory Composition');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ABSResponse | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const resourcesList = biologicalResources
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);

      const response = await axios.post('/api/compliance/abs-check', {
        applicant_name: applicantName,
        applicant_type: applicantType,
        has_foreign_shareholding_or_directors: hasForeignEquity,
        foreign_equity_percentage: foreignEquityPct,
        country_of_incorporation: country,
        biological_resources: resourcesList,
        geographical_source_state: sourceState,
        patent_application_title: patentTitle,
        is_for_patent_filing: true
      });
      setResult(response.data);
      toast.success('ABS evaluation complete & Form III generated');
    } catch (err) {
      console.error('ABS check failed:', err);
      // Local fallback
      setResult({
        applicant_classification: hasForeignEquity
          ? 'Section 3(2) Non-Indian Entity / Foreign-Participated Enterprise'
          : 'Section 7 Domestic Indian Entity',
        governing_section: hasForeignEquity
          ? 'Biological Diversity Act, 2002 — Section 3(2) & Section 6'
          : 'Biological Diversity Act, 2002 — Section 7 & Section 6(1)',
        approval_authority: hasForeignEquity
          ? 'National Biodiversity Authority (NBA), Chennai'
          : `State Biodiversity Board (${sourceState} SBB) + NBA Form III`,
        is_section_3_2_entity: hasForeignEquity,
        mandatory_statutory_actions: [
          'Submit mandatory Form III application to NBA prior to patent grant.',
          'Execute Access & Benefit-Sharing (ABS) agreement for royalty sharing.'
        ],
        benefit_sharing_obligation: '0.1% to 0.5% of annual gross ex-factory sale price.',
        penal_provisions: 'Section 55 BD Act: Up to 5 years imprisonment or fine up to 10 lakh rupees.',
        nba_form_iii_prefill: {
          form: 'FORM III',
          applicant: applicantName,
          state: sourceState,
          resources: biologicalResources.split(',').map(s => s.trim()),
          title: patentTitle
        },
        compliance_status: 'ACTION_REQUIRED_PRIOR_TO_PATENT_GRANT'
      });
    } finally {
      setLoading(false);
    }
  };

  const copyFormJSON = () => {
    if (!result?.nba_form_iii_prefill) return;
    navigator.clipboard.writeText(JSON.stringify(result.nba_form_iii_prefill, null, 2));
    toast.success('NBA Form III JSON copied to clipboard!');
  };

  const downloadFormJSON = () => {
    if (!result?.nba_form_iii_prefill) return;
    const blob = new Blob([JSON.stringify(result.nba_form_iii_prefill, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `NBA_FORM_III_${applicantName.replace(/\s+/g, '_')}.json`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Downloaded NBA Form III prefilled dataset');
  };

  return (
    <div className="space-y-8 pb-16">
      {/* HERO */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-teal-950 to-emerald-900 p-8 text-white shadow-xl border border-teal-800/30">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 text-emerald-300 text-xs font-bold uppercase tracking-widest mb-3">
              <ShieldCheck className="h-4 w-4" />
              BIODIVERSITY ACT 2002 • NBA FORM AUTO-COPILOT
            </div>
            <h1 className="text-3xl lg:text-4xl font-bold tracking-tight">
              Access & Benefit-Sharing (ABS)
            </h1>
            <p className="mt-3 max-w-2xl text-slate-300 text-sm leading-relaxed">
              Verify your statutory standing under Section 3(2) (Foreign shareholding) versus Section 7 (Domestic Indian entity)
              and auto-prefill mandatory National Biodiversity Authority (NBA) Form III datasets.
            </p>
          </div>

          <div className="hidden lg:flex h-20 w-20 rounded-2xl bg-white/10 border border-white/10 items-center justify-center">
            <Leaf className="h-10 w-10 text-emerald-300" />
          </div>
        </div>
      </section>

      {/* INPUT FORM */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-6">
        <div className="border-b border-slate-100 pb-4">
          <h2 className="text-lg font-bold text-slate-900">
            Entity & Biological Resource Compliance Parameters
          </h2>
          <p className="text-xs text-slate-500">
            The Biological Diversity Act applies different legal tests depending on foreign shareholding and biological origin.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* SECTION 3(2) ENTITY TOGGLE */}
          <div className="md:col-span-2 p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wider">
              Entity Ownership & Foreign Shareholding Status (Section 3(2) Test) *
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => {
                  setHasForeignEquity(false);
                  setForeignEquityPct(0);
                  setCountry('India');
                }}
                className={`p-4 rounded-xl border text-left transition flex items-start gap-3 ${
                  !hasForeignEquity
                    ? 'border-emerald-500 bg-emerald-50/70 text-emerald-950 ring-1 ring-emerald-500'
                    : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Building className="h-5 w-5 text-emerald-600 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs font-bold">100% Domestic Indian Entity (Section 7)</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Indian citizens or company with zero non-Indian equity or directors.
                  </p>
                </div>
              </button>

              <button
                type="button"
                onClick={() => {
                  setHasForeignEquity(true);
                  if (foreignEquityPct === 0) setForeignEquityPct(15);
                }}
                className={`p-4 rounded-xl border text-left transition flex items-start gap-3 ${
                  hasForeignEquity
                    ? 'border-purple-500 bg-purple-50/70 text-purple-950 ring-1 ring-purple-500'
                    : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Globe className="h-5 w-5 text-purple-600 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs font-bold">Foreign / NRI / Non-Indian Equity (Section 3(2))</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Any non-Indian shareholding, foreign investor, NRI director, or foreign entity.
                  </p>
                </div>
              </button>
            </div>

            {hasForeignEquity && (
              <div className="pt-2 flex items-center gap-4">
                <div className="flex-1">
                  <label className="block text-[11px] font-bold text-slate-600 mb-1">
                    Foreign / NRI Equity Percentage (%):
                  </label>
                  <input
                    type="number"
                    min="0.1"
                    max="100"
                    step="0.1"
                    value={foreignEquityPct}
                    onChange={(e) => setForeignEquityPct(parseFloat(e.target.value) || 0)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium"
                  />
                </div>
                <div className="flex-1">
                  <label className="block text-[11px] font-bold text-slate-600 mb-1">
                    Country of Incorporation:
                  </label>
                  <input
                    type="text"
                    value={country}
                    onChange={(e) => setCountry(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-xs font-medium"
                  />
                </div>
              </div>
            )}
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Applicant Entity Name
            </label>
            <input
              type="text"
              value={applicantName}
              onChange={(e) => setApplicantName(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-emerald-500 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Indian State of Biological Collection
            </label>
            <select
              value={sourceState}
              onChange={(e) => setSourceState(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-emerald-500 outline-none transition"
            >
              <option value="Karnataka">Karnataka (Western Ghats Belt)</option>
              <option value="Kerala">Kerala (Malabar / Silent Valley)</option>
              <option value="Rajasthan">Rajasthan (Thar / Nagori Belt)</option>
              <option value="Madhya Pradesh">Madhya Pradesh (Central Tribal Forest)</option>
              <option value="Uttarakhand">Uttarakhand (Himalayan Belt)</option>
              <option value="Himachal Pradesh">Himachal Pradesh</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Assam">Assam (North-East Bio-Hotspot)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Biological Resources / Plant Species
            </label>
            <input
              type="text"
              value={biologicalResources}
              onChange={(e) => setBiologicalResources(e.target.value)}
              placeholder="e.g. Withania somnifera, Curcuma longa"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-emerald-500 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Proposed Patent Application Title
            </label>
            <input
              type="text"
              value={patentTitle}
              onChange={(e) => setPatentTitle(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-emerald-500 outline-none transition"
            />
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading || !applicantName.trim()}
          className="w-full py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-950/20 transition flex items-center justify-center gap-2"
        >
          {loading ? 'Evaluating Section 3(2) vs Section 7 Statutory Mandates...' : (
            <>
              <ShieldCheck className="h-4 w-4" />
              Execute ABS Evaluation & Generate NBA Form III
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>
      </section>

      {/* RESULT SECTION */}
      {result && (
        <section className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-md space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-100 pb-5">
              <div>
                <span className={`text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full border ${
                  result.is_section_3_2_entity
                    ? 'text-purple-700 bg-purple-50 border-purple-200'
                    : 'text-emerald-700 bg-emerald-50 border-emerald-200'
                }`}>
                  {result.applicant_classification}
                </span>
                <h3 className="text-xl font-bold text-slate-900 mt-2">
                  Authority: {result.approval_authority}
                </h3>
                <p className="text-xs text-slate-600 mt-1">
                  Governing Provision: <span className="font-semibold text-slate-800">{result.governing_section}</span>
                </p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={copyFormJSON}
                  className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-xl border border-slate-200 bg-white text-slate-700 hover:bg-slate-50 transition"
                >
                  <Copy className="h-3.5 w-3.5" />
                  Copy JSON
                </button>
                <button
                  onClick={downloadFormJSON}
                  className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-xl bg-emerald-600 text-white hover:bg-emerald-500 transition shadow-sm"
                >
                  <Download className="h-3.5 w-3.5" />
                  Download Form III JSON
                </button>
              </div>
            </div>

            {/* MANDATORY ACTIONS */}
            <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200 space-y-2">
              <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wider flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                Mandatory Statutory Action Plan
              </h4>
              <ul className="space-y-1.5">
                {result.mandatory_statutory_actions.map((act, i) => (
                  <li key={i} className="text-xs text-amber-900 flex items-start gap-2">
                    <span className="font-bold">•</span>
                    <span>{act}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* BENEFIT SHARING & PENAL */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Scale className="h-4 w-4 text-teal-600" />
                  Benefit-Sharing Obligations
                </h4>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {result.benefit_sharing_obligation}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-rose-50/50 border border-rose-200">
                <h4 className="text-xs font-bold text-rose-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <AlertTriangle className="h-4 w-4 text-rose-600" />
                  Penal Non-Compliance Provisions
                </h4>
                <p className="text-xs text-rose-800 leading-relaxed">
                  {result.penal_provisions}
                </p>
              </div>
            </div>

            {/* PREFILLED FORM III VIEWER */}
            <div>
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
                  <FileCheck2 className="h-4 w-4 text-emerald-600" />
                  Auto-Prefilled NBA Form III JSON Dataset
                </h4>
                <span className="text-[11px] text-slate-400">
                  Ready for official e-filing at nbaindia.org
                </span>
              </div>
              <pre className="p-5 rounded-2xl bg-slate-900 text-emerald-400 font-mono text-xs whitespace-pre-wrap leading-relaxed overflow-x-auto border border-slate-800">
                {JSON.stringify(result.nba_form_iii_prefill, null, 2)}
              </pre>
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default ABSCompliance;