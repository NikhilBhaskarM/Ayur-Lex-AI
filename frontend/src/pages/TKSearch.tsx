import React, { useState } from 'react';
import { 
  BookOpen, Search, AlertCircle, ExternalLink, ShieldAlert, 
  CheckCircle2, AlertTriangle, ArrowRight 
} from 'lucide-react';
import { Link } from 'react-router-dom';

const TKSearch: React.FC = () => {
  const [herbName, setHerbName] = useState('');
  const [therapeuticClaim, setTherapeuticClaim] = useState('');
  const [analysisDone, setAnalysisDone] = useState(false);

  const handleAnalyze = (e: React.FormEvent) => {
    e.preventDefault();
    if (!herbName.trim()) return;
    setAnalysisDone(true);
  };

  const knownHerbsMap: Record<string, { classicalUses: string[]; tkrcClass: string; famousPriorArt: string }> = {
    turmeric: {
      classicalUses: ['Vranaropana (wound healing)', 'Kushthaghna (skin diseases)', 'Vishaghna (anti-toxic)', 'Prameha (metabolic/diabetes)'],
      tkrcClass: 'A61K 36/9066 (Zingiberaceae medicinal preparations)',
      famousPriorArt: 'USPTO Patent 5,401,504 (Curcumin wound healing) successfully revoked by CSIR in 1997 based on ancient Ayurvedic Sanskrit texts.',
    },
    haridra: {
      classicalUses: ['Vranaropana (wound healing)', 'Kushthaghna (skin diseases)', 'Vishaghna (anti-toxic)', 'Prameha (metabolic/diabetes)'],
      tkrcClass: 'A61K 36/9066 (Zingiberaceae medicinal preparations)',
      famousPriorArt: 'USPTO Patent 5,401,504 successfully revoked by CSIR in 1997 using Charaka Samhita prior art citations.',
    },
    neem: {
      classicalUses: ['Krimighna (antimicrobial/anthelminthic)', 'Kandughna (anti-pruritic)', 'Vranashodhana (wound cleansing)'],
      tkrcClass: 'A61K 36/58 (Meliaceae / Azadirachta indica)',
      famousPriorArt: 'EPO Patent 436257 (Fungicidal effect of neem) revoked in 2000 after 10-year legal opposition by India establishing extensive prior art.',
    },
    ashwagandha: {
      classicalUses: ['Balya (strength promoting)', 'Rasayana (rejuvenator)', 'Shothahara (anti-inflammatory)', 'Nidrajanana (sleep/adaptogen)'],
      tkrcClass: 'A61K 36/81 (Solanaceae / Withania somnifera)',
      famousPriorArt: 'Extensively documented in Bhavaprakasha Nighantu and Charaka Samhita; prior art routinely cited by patent examiners against ungrounded adaptogenic claims.',
    },
    guggulu: {
      classicalUses: ['Medohara (anti-obesity/anti-hyperlipidemic)', 'Vatarakta (arthritis/joint disorders)', 'Bhagna sandhana (bone healing)'],
      tkrcClass: 'A61K 36/328 (Burseraceae / Commiphora mukul)',
      famousPriorArt: 'Documented in Sushruta Samhita for Medoroga (lipid management); guggulsterone fractions subject to Section 3(d) enhanced efficacy scrutiny.',
    },
  };

  const lowerHerb = herbName.toLowerCase().trim();
  const matchedData = Object.entries(knownHerbsMap).find(([key]) => lowerHerb.includes(key))?.[1];

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-amber-50 rounded-xl">
            <BookOpen className="w-6 h-6 text-amber-600" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Traditional Knowledge & Prior Art Assistant
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Evaluate traditional knowledge overlap, Section 3(p) exclusions, and defensive prior art under the Indian Patents Act.
            </p>
          </div>
        </div>
      </div>

      {/* Mandatory TKDL Disclaimer Banner */}
      <div className="p-4 bg-blue-50/70 border border-blue-200 rounded-xl text-xs sm:text-sm text-blue-900 flex items-start gap-3 shadow-2xs">
        <ShieldAlert className="w-5 h-5 text-[#2c7a7b] shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-[#1a365d]">
            TKDL Database Transparency & Access Disclosure
          </p>
          <p className="text-xs text-blue-800 leading-relaxed">
            The Traditional Knowledge Digital Library (TKDL) contains over 4.4 lakh codified formulations from ancient treatises. In compliance with strict legal ethics, this assistant does NOT claim to possess unauthorized direct API access to non-public TKDL examiner databases. Non-patent office users may access TKDL through the paid subscription scheme approved by the Union Cabinet in August 2022.
          </p>
          <div className="pt-1">
            <a
              href="https://www.tkdl.res.in"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs font-semibold text-[#2c7a7b] hover:underline inline-flex items-center gap-1"
            >
              <span>Visit Official TKDL Portal (CSIR / Ministry of Ayush)</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>

      {/* Input Search Form */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
        <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
          Prior Art & Section 3(p) Pre-Screening
        </h2>

        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Botanical Name / Classical Ayurvedic Herb *
            </label>
            <input
              type="text"
              required
              placeholder="e.g., Haridra / Curcuma longa, Ashwagandha, Neem, or Guggulu"
              value={herbName}
              onChange={(e) => {
                setHerbName(e.target.value);
                setAnalysisDone(false);
              }}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] focus:border-transparent outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Claimed Therapeutic Indication or Novel Use
            </label>
            <input
              type="text"
              placeholder="e.g., Anti-inflammatory joint support, wound dressing, or metabolic enhancement"
              value={therapeuticClaim}
              onChange={(e) => setTherapeuticClaim(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] focus:border-transparent outline-hidden"
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              className="flex items-center gap-2 px-5 py-2.5 bg-[#1a365d] text-white rounded-lg text-xs sm:text-sm font-semibold hover:bg-[#0f2342] transition-colors"
            >
              <Search className="w-4 h-4" />
              <span>Analyze Prior Art Overlap</span>
            </button>
          </div>
        </form>
      </div>

      {/* Analysis Results */}
      {analysisDone && (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
          <div className="border-b border-gray-100 pb-4">
            <span className="text-xs font-bold text-amber-700 uppercase tracking-wider">
              Traditional Knowledge Analysis Report
            </span>
            <h2 className="text-xl font-bold text-[#1a365d] mt-1">
              Preliminary Prior Art Assessment: {herbName}
            </h2>
          </div>

          {/* Section 3(p) Analysis */}
          <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-2">
            <div className="flex items-center gap-2 text-sm font-bold text-amber-900">
              <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0" />
              <span>Section 3(p) Patents Act Risk: High Scrutiny Trigger</span>
            </div>
            <p className="text-xs sm:text-sm text-amber-800 leading-relaxed">
              Under <strong>Section 3(p) of the Patents Act, 1970</strong>, an invention which in effect is traditional knowledge or an aggregation/duplication of known properties of traditionally known components is <strong>statutorily unpatentable</strong> in India.
            </p>
          </div>

          {/* Classical Corroboration */}
          {matchedData && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider">
                Codified Classical Ayurvedic References
              </h3>
              <div className="p-4 bg-gray-50 border border-gray-200 rounded-xl space-y-2.5 text-xs sm:text-sm">
                <div>
                  <span className="font-bold text-gray-600 block">Codified Classical Indications:</span>
                  <div className="flex flex-wrap gap-1.5 mt-1">
                    {matchedData.classicalUses.map((use, idx) => (
                      <span key={idx} className="bg-white border border-gray-200 px-2.5 py-1 rounded-md text-gray-800 font-medium text-xs">
                        {use}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="pt-2 border-t border-gray-200">
                  <span className="font-bold text-gray-600">Traditional Knowledge Resource Classification (TKRC):</span>{' '}
                  <span className="font-mono text-xs text-[#2c7a7b]">{matchedData.tkrcClass}</span>
                </div>
                <div className="pt-2 border-t border-gray-200 text-xs text-gray-600">
                  <span className="font-bold text-gray-700">Precedent Case Note:</span> {matchedData.famousPriorArt}
                </div>
              </div>
            </div>
          )}

          {/* How to Overcome Rejection */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider">
              Legal Strategy: How to Establish Patentability for Herbal Innovations
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div className="p-3.5 bg-white border border-gray-200 rounded-xl shadow-2xs space-y-1">
                <span className="font-bold text-[#1a365d] block text-sm">1. Experimental Synergism (Section 3(e))</span>
                <p className="text-gray-600">
                  If combining multiple herbs, submit laboratory pharmacological assays showing the combined therapeutic effect is statistically superior to the mathematical sum of individual components.
                </p>
              </div>
              <div className="p-3.5 bg-white border border-gray-200 rounded-xl shadow-2xs space-y-1">
                <span className="font-bold text-[#1a365d] block text-sm">2. Enhanced Efficacy (Section 3(d))</span>
                <p className="text-gray-600">
                  For novel fractions, extracts, or polymorphs, provide comparative pharmacological data proving a significant enhancement in therapeutic efficacy over standard classical extracts.
                </p>
              </div>
              <div className="p-3.5 bg-white border border-gray-200 rounded-xl shadow-2xs space-y-1">
                <span className="font-bold text-[#1a365d] block text-sm">3. Novel Extraction Technology</span>
                <p className="text-gray-600">
                  Patent the non-obvious industrial process or novel apparatus rather than the final herbal substance if the substance itself exists in traditional knowledge.
                </p>
              </div>
              <div className="p-3.5 bg-white border border-gray-200 rounded-xl shadow-2xs space-y-1">
                <span className="font-bold text-[#1a365d] block text-sm">4. Novel Non-Obvious Therapeutic Use</span>
                <p className="text-gray-600">
                  A genuinely novel therapeutic indication that has zero precedent or analogy in any classical treatise or folk literature, supported by clinical mechanisms.
                </p>
              </div>
            </div>
          </div>

          {/* Query RAG Assistant Link */}
          <div className="p-4 bg-emerald-50/50 border border-emerald-200 rounded-xl flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-bold text-emerald-900">
                Want to search specific statutory provisions for this herb?
              </p>
              <p className="text-[11px] text-emerald-800">
                Ask our AI assistant to retrieve exact sections from the Patents Act or AYUSH guidelines.
              </p>
            </div>
            <Link
              to="/chat"
              className="flex items-center gap-1.5 px-3.5 py-2 bg-[#1a365d] text-white rounded-lg text-xs font-semibold hover:bg-[#0f2342] shrink-0"
            >
              <span>Ask AI Assistant</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default TKSearch;
