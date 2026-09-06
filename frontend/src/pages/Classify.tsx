import React, { useState } from 'react';
import { 
  Layers, ArrowRight, ArrowLeft, CheckCircle2, AlertTriangle, 
  HelpCircle, Shield, FileText, Leaf, Scale, RefreshCw, Send
} from 'lucide-react';
import toast from 'react-hot-toast';
import { classificationApi } from '@/api/classification';
import { useAuthStore } from '@/store/authStore';
import ConfidenceBadge from '@/components/common/ConfidenceBadge';
import type { ClassificationResponse } from '@/types';

const Classify: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);

  // Form State
  const [step, setStep] = useState(1);
  const [formulationName, setFormulationName] = useState('');
  const [description, setDescription] = useState('');
  const [ingredientsText, setIngredientsText] = useState('');
  const [intendedUse, setIntendedUse] = useState('');
  const [isClassical, setIsClassical] = useState<boolean | undefined>(undefined);
  const [hasBeenModified, setHasBeenModified] = useState<boolean | undefined>(undefined);
  const [marketedAs, setMarketedAs] = useState('Medicine');
  const [hasBiologicalResources, setHasBiologicalResources] = useState<boolean | undefined>(true);
  const [isPubliclyDisclosed, setIsPubliclyDisclosed] = useState<boolean | undefined>(false);

  // Loading & Result State
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResponse | null>(null);

  const handleClassify = async () => {
    if (!formulationName.trim()) {
      toast.error('Please provide a formulation name');
      return;
    }

    const ingredients = ingredientsText
      .split(/[,;\n]+/)
      .map((i) => i.trim())
      .filter(Boolean);

    setIsLoading(true);
    setResult(null);

    try {
      const response = await classificationApi.classify({
        formulation_name: formulationName,
        description,
        ingredients: ingredients.length > 0 ? ingredients : [formulationName],
        intended_use: intendedUse || 'General therapeutic or wellness indication',
        is_classical_text_based: isClassical,
        has_been_modified: hasBeenModified,
        marketed_as: marketedAs,
        jurisdiction: jurisdiction,
        biological_resources_involved: hasBiologicalResources,
      });

      setResult(response);
      setStep(4); // Move to results step
      toast.success('Classification completed');
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Classification engine failed';
      toast.error(detail);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setStep(1);
    setFormulationName('');
    setDescription('');
    setIngredientsText('');
    setIntendedUse('');
    setIsClassical(undefined);
    setHasBeenModified(undefined);
    setMarketedAs('Medicine');
    setHasBiologicalResources(true);
    setIsPubliclyDisclosed(false);
    setResult(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-[#1a365d]/10 rounded-xl">
            <Layers className="w-6 h-6 text-[#1a365d]" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Formulation Classification Engine
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Determine statutory category: Classical Medicine, Patent/Proprietary (P&P), Phytopharmaceutical, Ayurveda-Aahar (Food), or Cosmetic.
            </p>
          </div>
        </div>

        {/* Wizard Step Indicators */}
        <div className="grid grid-cols-4 gap-2 mt-6 pt-6 border-t border-gray-100 text-xs font-medium text-center">
          <div className={`p-2 rounded-lg ${step === 1 ? 'bg-[#1a365d] text-white' : 'bg-gray-50 text-gray-600'}`}>
            1. Formulation Info
          </div>
          <div className={`p-2 rounded-lg ${step === 2 ? 'bg-[#1a365d] text-white' : 'bg-gray-50 text-gray-600'}`}>
            2. Classical Lineage
          </div>
          <div className={`p-2 rounded-lg ${step === 3 ? 'bg-[#1a365d] text-white' : 'bg-gray-50 text-gray-600'}`}>
            3. Regulatory Intent
          </div>
          <div className={`p-2 rounded-lg ${step === 4 ? 'bg-[#1a365d] text-white' : 'bg-gray-50 text-gray-600'}`}>
            4. Classification Report
          </div>
        </div>
      </div>

      {/* Step 1: Formulation Basics */}
      {step === 1 && (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-5">
          <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
            Step 1: Formulation Details
          </h2>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Formulation or Product Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g., Haridra-Guggulu Extract Compound or Classical Triphala Churna"
              value={formulationName}
              onChange={(e) => setFormulationName(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-[#2c7a7b] focus:border-transparent outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Ingredients (Botanical / Classical Names, separated by commas or lines)
            </label>
            <textarea
              rows={3}
              placeholder="e.g., Curcuma longa (Haridra), Commiphora mukul (Guggulu), Piper nigrum (Maricha)"
              value={ingredientsText}
              onChange={(e) => setIngredientsText(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-[#2c7a7b] focus:border-transparent outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Intended Use / Indication
            </label>
            <input
              type="text"
              placeholder="e.g., Joint inflammation relief, metabolic health support, or daily rasayana"
              value={intendedUse}
              onChange={(e) => setIntendedUse(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-[#2c7a7b] focus:border-transparent outline-hidden"
            />
          </div>

          <div className="flex justify-end pt-4 border-t border-gray-100">
            <button
              type="button"
              disabled={!formulationName.trim()}
              onClick={() => setStep(2)}
              className="flex items-center gap-2 px-5 py-2.5 bg-[#1a365d] text-white rounded-lg text-sm font-medium hover:bg-[#0f2342] disabled:opacity-40 transition-colors"
            >
              <span>Next: Classical Lineage</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Classical Lineage */}
      {step === 2 && (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
          <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
            Step 2: Classical Text Lineage & Modifications
          </h2>

          <div className="space-y-3">
            <label className="block text-xs sm:text-sm font-medium text-gray-700">
              Is this formulation directly described in an authoritative classical Ayurvedic text listed in Schedule 1 of Drugs & Cosmetics Act?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setIsClassical(true)}
                className={`p-3.5 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                  isClassical === true
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="font-semibold">Yes — Direct Classical Text</div>
                <div className="text-xs text-gray-500 mt-1">E.g., Charaka, Sushruta, AFI, Bhavaprakasha</div>
              </button>
              <button
                type="button"
                onClick={() => setIsClassical(false)}
                className={`p-3.5 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                  isClassical === false
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="font-semibold">No — Novel or Proprietary</div>
                <div className="text-xs text-gray-500 mt-1">New formulation, non-classical ratio, or modern extract</div>
              </button>
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-xs sm:text-sm font-medium text-gray-700">
              Has the classical formula or extraction process been modified?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setHasBeenModified(false)}
                className={`p-3.5 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                  hasBeenModified === false
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="font-semibold">No — Authentic Process</div>
                <div className="text-xs text-gray-500 mt-1">Prepared strictly per classical methodology</div>
              </button>
              <button
                type="button"
                onClick={() => setHasBeenModified(true)}
                className={`p-3.5 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                  hasBeenModified === true
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                <div className="font-semibold">Yes — Modified Format</div>
                <div className="text-xs text-gray-500 mt-1">Supercritical CO2 extract, modern dosage form, excipients</div>
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Methodology / Processing Description (Optional)
            </label>
            <textarea
              rows={2}
              placeholder="Describe any novel extraction, standardized markers, or classical bhavana process..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3.5 py-2 border border-gray-300 rounded-lg text-sm outline-hidden"
            />
          </div>

          <div className="flex justify-between pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="flex items-center gap-1.5 px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <button
              type="button"
              onClick={() => setStep(3)}
              className="flex items-center gap-2 px-5 py-2.5 bg-[#1a365d] text-white rounded-lg text-sm font-medium hover:bg-[#0f2342] transition-colors"
            >
              <span>Next: Regulatory Intent</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Marketing & Regulatory Parameters */}
      {step === 3 && (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
          <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
            Step 3: Commercial Intent & Biodiversity Factors
          </h2>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-2">
              Intended Marketing Category
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {['Medicine', 'Ayurveda-Aahar (Food)', 'Cosmetic', 'Nutraceutical'].map((cat) => (
                <button
                  key={cat}
                  type="button"
                  onClick={() => setMarketedAs(cat)}
                  className={`p-3 border rounded-xl text-center text-xs font-semibold transition-all ${
                    marketedAs === cat
                      ? 'border-[#2c7a7b] bg-[#e6fffa]/50 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                      : 'border-gray-200 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-xs sm:text-sm font-medium text-gray-700">
              Are Indian biological resources (raw herbs, plants, minerals, microbial cultures) utilized?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setHasBiologicalResources(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium ${
                  hasBiologicalResources === true
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                Yes — Indian Biological Resources Involved
              </button>
              <button
                type="button"
                onClick={() => setHasBiologicalResources(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium ${
                  hasBiologicalResources === false
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                No — Purely Synthetic or Non-Indian
              </button>
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-xs sm:text-sm font-medium text-gray-700">
              Has this formulation already been publicly disclosed or published anywhere?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setIsPubliclyDisclosed(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium ${
                  isPubliclyDisclosed === false
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                No — Confidential / Undisclosed
              </button>
              <button
                type="button"
                onClick={() => setIsPubliclyDisclosed(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium ${
                  isPubliclyDisclosed === true
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50 text-gray-700'
                }`}
              >
                Yes — Publicly Marketed or Published
              </button>
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={() => setStep(2)}
              className="flex items-center gap-1.5 px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <button
              type="button"
              disabled={isLoading}
              onClick={handleClassify}
              className="flex items-center gap-2 px-6 py-2.5 bg-[#2c7a7b] text-white rounded-lg text-sm font-semibold hover:bg-[#235e5f] disabled:opacity-50 transition-colors shadow-2xs"
            >
              {isLoading ? (
                <span>Classifying with RAG Evidence...</span>
              ) : (
                <>
                  <span>Run Legal Classification</span>
                  <Send className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Step 4: Classification Results Report */}
      {step === 4 && result && (
        <div className="space-y-6">
          {/* Main Classification Card */}
          <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-5">
            <div className="flex flex-wrap items-start justify-between gap-4 border-b border-gray-100 pb-4">
              <div>
                <span className="text-xs font-semibold text-[#2c7a7b] uppercase tracking-wider">
                  Official Statutory Classification
                </span>
                <h2 className="text-xl sm:text-2xl font-bold text-[#1a365d] mt-1">
                  {result.classification}
                </h2>
                <p className="text-xs text-gray-500 mt-0.5">
                  Formulation: {formulationName} • Jurisdiction: {jurisdiction}
                </p>
              </div>
              {result.confidence && <ConfidenceBadge level={result.confidence.level} score={result.confidence.score} />}
            </div>

            {/* Statutory Reasoning */}
            <div>
              <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Scale className="w-4 h-4 text-[#1a365d]" />
                <span>Statutory Reasoning & Legal Grounds</span>
              </h3>
              <div className="p-4 bg-gray-50 rounded-xl text-xs sm:text-sm text-gray-800 leading-relaxed border border-gray-100">
                {result.reasoning}
              </div>
            </div>

            {/* Evidence & Citations */}
            {result.evidence && result.evidence.length > 0 && (
              <div>
                <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-[#2c7a7b]" />
                  <span>Authoritative Legal Evidence</span>
                </h3>
                <ul className="space-y-1.5">
                  {result.evidence.map((ev, i) => (
                    <li key={i} className="text-xs sm:text-sm text-gray-700 flex items-start gap-2 bg-white border border-gray-100 p-2.5 rounded-lg">
                      <CheckCircle2 className="w-4 h-4 text-[#2c7a7b] shrink-0 mt-0.5" />
                      <span>{ev}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Detailed Implications Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Regulatory Implications */}
            <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-5 space-y-3">
              <h3 className="text-xs font-bold text-[#1a365d] uppercase tracking-wider flex items-center gap-1.5 border-b border-gray-100 pb-2">
                <Shield className="w-4 h-4 text-[#1a365d]" />
                <span>Regulatory Regime</span>
              </h3>
              <ul className="space-y-2">
                {result.regulatory_implications?.map((item, i) => (
                  <li key={i} className="text-xs text-gray-700 flex items-start gap-1.5">
                    <span className="text-[#1a365d] font-bold">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* IPR Implications */}
            <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-5 space-y-3">
              <h3 className="text-xs font-bold text-[#2c7a7b] uppercase tracking-wider flex items-center gap-1.5 border-b border-gray-100 pb-2">
                <Scale className="w-4 h-4 text-[#2c7a7b]" />
                <span>IP & Patentability</span>
              </h3>
              <ul className="space-y-2">
                {result.ip_implications?.map((item, i) => (
                  <li key={i} className="text-xs text-gray-700 flex items-start gap-1.5">
                    <span className="text-[#2c7a7b] font-bold">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* ABS Implications */}
            <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-5 space-y-3">
              <h3 className="text-xs font-bold text-emerald-800 uppercase tracking-wider flex items-center gap-1.5 border-b border-gray-100 pb-2">
                <Leaf className="w-4 h-4 text-emerald-600" />
                <span>ABS & Biodiversity</span>
              </h3>
              <ul className="space-y-2">
                {result.abs_implications?.map((item, i) => (
                  <li key={i} className="text-xs text-gray-700 flex items-start gap-1.5">
                    <span className="text-emerald-600 font-bold">•</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Recommended Next Steps & Missing Info */}
          <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
            <h3 className="text-xs font-bold text-gray-800 uppercase tracking-wider">
              Recommended Statutory Next Steps
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.recommended_next_steps?.map((step, i) => (
                <div key={i} className="p-3 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-800 flex items-start gap-2">
                  <span className="font-bold text-[#1a365d]">{i + 1}.</span>
                  <span>{step}</span>
                </div>
              ))}
            </div>

            {result.missing_information && result.missing_information.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-100">
                <h4 className="text-xs font-semibold text-amber-800 flex items-center gap-1.5 mb-2">
                  <HelpCircle className="w-3.5 h-3.5 text-amber-600" />
                  <span>Missing Information for Conclusive Determination:</span>
                </h4>
                <ul className="list-disc list-inside text-xs text-amber-900 space-y-1">
                  {result.missing_information.map((info, i) => (
                    <li key={i}>{info}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Disclaimer Banner */}
            <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-800 flex items-start gap-2 mt-4">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                <strong>Non-Binding Assessment:</strong> {result.disclaimer || 'This classification is generated based on algorithmic analysis of regulatory texts and does not constitute a legally binding ruling by the State Licensing Authority or AYUSH Ministry.'}
              </span>
            </div>

            <div className="flex justify-end gap-3 pt-4 border-t border-gray-100">
              <button
                type="button"
                onClick={resetForm}
                className="flex items-center gap-1.5 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-xs font-medium hover:bg-gray-50"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Classify Another Formulation</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Classify;
