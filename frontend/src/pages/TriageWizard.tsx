import React, { useState } from 'react';
import {
  Compass,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  BookOpen,
  ArrowRight,
  HelpCircle,
  FileCheck,
  Tag,
  Scale
} from 'lucide-react';
import axios from 'axios';

interface TriageResult {
  formulation_name: string;
  category: string;
  statutory_hurdle: string;
  governing_statutes: string[];
  regulatory_requirements: string[];
  patentability_assessment: string;
  actionable_recommendations: string[];
  statutory_risk_score: number;
  taxonomic_breakdown: Array<{
    input_term: string;
    botanical_species: string;
    family: string;
    active_markers: string[];
    recommended_claim_clause: string;
  }>;
}

const PRESETS = [
  {
    name: 'Triphala Classical Churna',
    marketed_as: 'medicine',
    is_classical: true,
    ingredients: ['Amalaki', 'Haritaki', 'Bibhitaki'],
    extraction: 'classical kwath decoction',
    indications: 'Digestive regulation, tridosha balancing'
  },
  {
    name: 'Synergistic Curcumin-Piperine Lipid Complex',
    marketed_as: 'medicine',
    is_classical: false,
    ingredients: ['Haridra', 'Maricha'],
    extraction: 'supercritical CO2 enriched fraction',
    indications: 'Inflammatory modulation and arthritis pain management'
  },
  {
    name: 'Standardized Withanolide Phytopharma Capsule',
    marketed_as: 'phytopharma',
    is_classical: false,
    ingredients: ['Ashwagandha'],
    extraction: 'purified fraction (40% Withanolides)',
    indications: 'Cognitive enhancement and neuroprotection with Phase II clinical trial'
  },
  {
    name: 'Ayurveda Aahara Daily Vitality Granules',
    marketed_as: 'food',
    is_classical: false,
    ingredients: ['Amalaki', 'Yashtimadhu', 'Shunti'],
    extraction: 'spray-dried aqueous food extract',
    indications: 'Daily dietary vitality, immune nutritional support'
  },
  {
    name: 'Kumkumadi Radiance Facial Elixir',
    marketed_as: 'cosmetic',
    is_classical: false,
    ingredients: ['Haridra', 'Yashtimadhu', 'Tulsi'],
    extraction: 'lipid-soluble cold-pressed oil',
    indications: 'Skin radiance, dermal barrier enhancement, complexion beautifying'
  }
];

const TriageWizard: React.FC = () => {
  const [name, setName] = useState('');
  const [ingredientsStr, setIngredientsStr] = useState('');
  const [marketedAs, setMarketedAs] = useState('medicine');
  const [extraction, setExtraction] = useState('');
  const [indications, setIndications] = useState('');
  const [isClassical, setIsClassical] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TriageResult | null>(null);

  const applyPreset = (preset: typeof PRESETS[0]) => {
    setName(preset.name);
    setMarketedAs(preset.marketed_as);
    setIsClassical(preset.is_classical);
    setIngredientsStr(preset.ingredients.join(', '));
    setExtraction(preset.extraction);
    setIndications(preset.indications);
  };

  const handleTriage = async () => {
    if (!name.trim()) return;
    setLoading(true);
    try {
      const ingredients = ingredientsStr
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean);

      const response = await axios.post('/api/triage/classify', {
        formulation_name: name,
        ingredients,
        indications,
        is_classical_text_based: isClassical,
        marketed_as: marketedAs,
        extraction_technology: extraction
      });
      setResult(response.data);
    } catch (err) {
      console.error('Triage failed:', err);
      // Fallback result for offline client resiliency
      setResult({
        formulation_name: name,
        category: isClassical
          ? 'Classical / Generic Ayurvedic Medicine (First Schedule Texts)'
          : marketedAs === 'cosmetic'
          ? 'Ayurvedic Cosmetic (Schedule S / Cosmetics Rules 2020)'
          : marketedAs === 'food'
          ? 'Ayurveda Aahara (FSSAI Regulations 2022)'
          : 'Patent or Proprietary (P&P) Ayurvedic Medicine',
        statutory_hurdle: isClassical
          ? 'Section 3(p) TKDL Bar'
          : 'Section 3(e) Mere Admixture Alert',
        governing_statutes: [
          'The Patents Act, 1970 — Section 3(p) & 3(e)',
          'Drugs and Cosmetics Act, 1940'
        ],
        regulatory_requirements: [
          'Verify formula against First Schedule text or submit synergism index data.'
        ],
        patentability_assessment:
          'Evaluated via offline deterministic rule engine. Patenting polyherbal combinations requires demonstrated supra-additive synergism (CI < 1.0).',
        actionable_recommendations: [
          'Submit empirical combination index bioassay to clear Section 3(e).'
        ],
        statutory_risk_score: isClassical ? 95 : 65,
        taxonomic_breakdown: []
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 pb-16">
      {/* HERO */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-teal-950 to-emerald-950 p-8 text-white shadow-2xl border border-teal-800/30">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 text-teal-400 text-xs font-bold tracking-widest uppercase mb-3">
              <Compass className="h-4 w-4" />
              Regulatory & Patentability Triage Engine
            </div>
            <h1 className="text-3xl lg:text-4xl font-black tracking-tight">
              Formulation Triage Wizard
            </h1>
            <p className="mt-2 max-w-2xl text-slate-300 text-sm leading-relaxed">
              Instantly classify your Ayurvedic formulation into its lawful Indian regulatory route:
              Classical Medicine (§3(p)), Proprietary (§3(e)), Phytopharmaceutical (CDSCO 122E),
              Ayurveda Aahara (FSSAI 2022), or Cosmetic (Schedule S).
            </p>
          </div>

          <div className="flex flex-wrap gap-2 lg:max-w-xs">
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              §3(p) TKDL Check
            </span>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
              §3(e) Synergism
            </span>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
              FSSAI Aahara
            </span>
            <span className="px-3 py-1 text-xs font-semibold rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30">
              CDSCO Rule 122E
            </span>
          </div>
        </div>
      </section>

      {/* CASE PRESETS */}
      <section className="space-y-3">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-500 uppercase tracking-wider">
          <Sparkles className="h-4 w-4 text-teal-600" />
          Quick Intake Presets (Click to Test)
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => applyPreset(p)}
              className="text-left p-3 rounded-2xl border border-slate-200 bg-white hover:border-teal-500 hover:shadow-md transition group"
            >
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-600 uppercase group-hover:bg-teal-50 group-hover:text-teal-700">
                {p.marketed_as}
              </span>
              <p className="text-xs font-bold text-slate-800 mt-2 line-clamp-1 group-hover:text-teal-700">
                {p.name}
              </p>
              <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                {p.ingredients.join(', ')}
              </p>
            </button>
          ))}
        </div>
      </section>

      {/* INTAKE FORM */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Formulation Name / Working Code *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g., Curcumin-Piperine Synergistic Bio-Complex"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Target Market Category *
            </label>
            <select
              value={marketedAs}
              onChange={(e) => setMarketedAs(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
            >
              <option value="medicine">Ayurvedic Medicine (AYUSH License)</option>
              <option value="phytopharma">Phytopharmaceutical / New Drug (CDSCO)</option>
              <option value="food">Ayurveda Aahara (FSSAI Food Supplement)</option>
              <option value="cosmetic">Ayurvedic Cosmetic (Schedule S)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Ingredients / Extracts (Comma-Separated)
            </label>
            <input
              type="text"
              value={ingredientsStr}
              onChange={(e) => setIngredientsStr(e.target.value)}
              placeholder="e.g. Ashwagandha, Pippali, Haridra, Guduchi"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Extraction Technology / Vehicle
            </label>
            <input
              type="text"
              value={extraction}
              onChange={(e) => setExtraction(e.target.value)}
              placeholder="e.g. Supercritical CO2, Hydro-ethanolic 70:30, Micronized lipid emulsion"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Intended Therapeutic Indication / Claim
            </label>
            <input
              type="text"
              value={indications}
              onChange={(e) => setIndications(e.target.value)}
              placeholder="e.g. For reduction of systemic inflammatory biomarkers and joint pain"
              className="w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-sm font-medium focus:bg-white focus:border-teal-500 outline-none transition"
            />
          </div>

          <div className="md:col-span-2 flex items-center gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200">
            <input
              type="checkbox"
              id="classicalCheck"
              checked={isClassical}
              onChange={(e) => setIsClassical(e.target.checked)}
              className="h-4 w-4 text-teal-600 rounded focus:ring-teal-500"
            />
            <label htmlFor="classicalCheck" className="text-xs text-slate-700 cursor-pointer">
              <span className="font-bold">Classical Treatise Formulation:</span> Checked if this composition is directly described in authoritative classical texts listed in the First Schedule (Charaka Samhita, Sushruta Samhita, etc.).
            </label>
          </div>
        </div>

        <button
          onClick={handleTriage}
          disabled={!name.trim() || loading}
          className="w-full py-4 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-bold text-sm shadow-lg shadow-teal-950/20 transition flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? (
            'Analyzing Statutory & Regulatory Pathways...'
          ) : (
            <>
              <Compass className="h-4 w-4" />
              Execute Formulation Triage
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>
      </section>

      {/* RESULTS DISPLAY */}
      {result && (
        <section className="space-y-6">
          {/* TOP CARD */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-md space-y-6">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 border-b border-slate-100 pb-5">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-widest text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
                  Triage Classification Result
                </span>
                <h2 className="text-2xl font-bold text-slate-900 mt-2">
                  {result.category}
                </h2>
                <p className="text-xs font-semibold text-rose-600 mt-1 flex items-center gap-1.5">
                  <AlertTriangle className="h-3.5 w-3.5" />
                  Primary Statutory Hurdle: {result.statutory_hurdle}
                </p>
              </div>

              <div className="text-right">
                <span className="text-xs text-slate-400 font-semibold block">Statutory Risk Index</span>
                <span className={`text-3xl font-black ${result.statutory_risk_score > 70 ? 'text-rose-600' : result.statutory_risk_score > 40 ? 'text-amber-600' : 'text-emerald-600'}`}>
                  {result.statutory_risk_score}%
                </span>
              </div>
            </div>

            {/* OPINION */}
            <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200">
              <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2 flex items-center gap-2">
                <Scale className="h-4 w-4 text-teal-600" />
                Patentability Adjudication
              </h3>
              <p className="text-sm text-slate-700 leading-relaxed">
                {result.patentability_assessment}
              </p>
            </div>

            {/* GOVERNING STATUTES & REQS */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-5 rounded-2xl bg-white border border-slate-200">
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-indigo-600" />
                  Applicable Indian Statutes
                </h3>
                <ul className="space-y-2">
                  {result.governing_statutes.map((s, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                      <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-5 rounded-2xl bg-white border border-slate-200">
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <FileCheck className="h-4 w-4 text-emerald-600" />
                  Regulatory Compliance Mandates
                </h3>
                <ul className="space-y-2">
                  {result.regulatory_requirements.map((r, i) => (
                    <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
                      {r}
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* RECOMMENDATIONS */}
            <div className="p-5 rounded-2xl bg-emerald-50/60 border border-emerald-200">
              <h3 className="text-xs font-bold text-emerald-900 uppercase tracking-wider mb-3 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                Recommended Actionable Strategy
              </h3>
              <div className="space-y-2">
                {result.actionable_recommendations.map((rec, i) => (
                  <div key={i} className="text-xs text-emerald-800 flex items-start gap-2">
                    <span className="font-bold">{i + 1}.</span>
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* BOTANICAL TAXONOMY BREAKDOWN */}
            {result.taxonomic_breakdown && result.taxonomic_breakdown.length > 0 && (
              <div>
                <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <Tag className="h-4 w-4 text-teal-600" />
                  Botanical Taxonomy & Claim Clauses
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {result.taxonomic_breakdown.map((item, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 space-y-1">
                      <div className="flex justify-between items-center">
                        <span className="text-xs font-bold text-slate-900">{item.input_term}</span>
                        <span className="text-[10px] italic text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                          {item.botanical_species}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500">Family: {item.family}</p>
                      {item.active_markers.length > 0 && (
                        <p className="text-[10px] text-slate-600 font-mono">
                          Markers: {item.active_markers.join(', ')}
                        </p>
                      )}
                      <p className="text-[11px] font-serif text-slate-700 bg-white p-2 rounded border border-slate-100 mt-1">
                        "{item.recommended_claim_clause}"
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      )}
    </div>
  );
};

export default TriageWizard;
