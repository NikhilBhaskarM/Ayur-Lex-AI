import React, { useState } from 'react';
import { 
  BookOpen, Search, ExternalLink, ShieldAlert, 
  CheckCircle2, AlertTriangle, ArrowRight, RefreshCw, FileText
} from 'lucide-react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { tkApi, type TKSearchResponse, type HerbPriorArtResult } from '../api/tk';

const defaultFallbackHerbs: Record<string, HerbPriorArtResult> = {
  turmeric: {
    herb_name: 'Turmeric',
    sanskrit_name: 'Haridra / Nisha',
    botanical_name: 'Curcuma longa L.',
    family: 'Zingiberaceae',
    tkrc_class: 'A61K 36/9066 (Zingiberaceae medicinal preparations)',
    classical_treatises: [
      {
        treatise: 'Charaka Samhita',
        verse_or_chapter: 'Sutra Sthana Ch. 4 (Kushthaghna Mahakashaya)',
        indications: ['Vranaropana (wound healing)', 'Kushthaghna (skin diseases)', 'Vishaghna (anti-toxic)', 'Prameha (metabolic/diabetes)'],
        sanskrit_sloka: 'हरिद्रा कटुतिक्तोष्णा कफपित्तविनाशिनी । त्वग्दोषहन्त्री प्रमेहाणां नाशिनी व्रणरोपणी ॥',
      },
    ],
    famous_revocation_case: {
      patent_number: 'US 5,401,504',
      patent_office: 'USPTO',
      applicant: 'University of Mississippi Medical Center',
      disputed_claims: 'Use of turmeric in powder form to promote wound healing.',
      outcome: 'REVOKED in 1997 based on ancient Ayurvedic Sanskrit texts.',
      key_prior_art_cited: 'Charaka Samhita and 1953 Indian Medical Association papers.',
    },
    section_3p_rejection_risk: 'CRITICAL (Near 100%) for direct wound healing without quantitative synergistic data.',
    defensive_search_guidance: 'Search TKDL database under A61K 36/9066. Must establish combination index CI < 1.0 with novel delivery carriers.',
  },
};

const TKSearch: React.FC = () => {
  const [herbName, setHerbName] = useState('');
  const [therapeuticClaim, setTherapeuticClaim] = useState('');
  const [loading, setLoading] = useState(false);
  const [searchResponse, setSearchResponse] = useState<TKSearchResponse | null>(null);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!herbName.trim()) {
      toast.error('Please enter an herb name or query');
      return;
    }

    setLoading(true);
    try {
      const res = await tkApi.search({
        query: herbName,
        herb_name: herbName,
        therapeutic_claim: therapeuticClaim || undefined,
      });
      setSearchResponse(res);
      if (res.matched_herbs.length === 0) {
        toast('No exact classical matches found in database, showing RAG context.', { icon: 'ℹ️' });
      } else {
        toast.success(`Found ${res.matched_herbs.length} classical Ayurvedic prior art matches!`);
      }
    } catch (err: any) {
      console.warn('Backend TK search offline, falling back to local database:', err);
      // Fallback
      const lower = herbName.toLowerCase();
      const matched = Object.entries(defaultFallbackHerbs)
        .filter(([k]) => lower.includes(k))
        .map(([, v]) => v);

      setSearchResponse({
        query: herbName,
        matched_herbs: matched,
        rag_retrieved_provisions: [],
        total_matches: matched.length,
        defensive_advice: 'Vetted through local classical treatise pharmacopoeia archive.',
      });
    } finally {
      setLoading(false);
    }
  };

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
            The Traditional Knowledge Digital Library (TKDL) contains over 4.4 lakh codified formulations from ancient treatises. In compliance with strict legal ethics, this assistant searches open classical treatises and public prior art decisions. Non-patent office users may access the full TKDL through the paid subscription scheme approved by the Union Cabinet.
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
              placeholder="e.g., Haridra / Curcuma longa, Ashwagandha, Neem, Guggulu, Tulsi, Brahmi"
              value={herbName}
              onChange={(e) => setHerbName(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1">
              Claimed Therapeutic Indication or Novel Use
            </label>
            <input
              type="text"
              placeholder="e.g., wound healing, adaptogenic anti-stress, cognitive enhancement, anti-inflammatory"
              value={therapeuticClaim}
              onChange={(e) => setTherapeuticClaim(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
            />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs sm:text-sm font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Searching Treatises & Knowledge Base...</span>
                </>
              ) : (
                <>
                  <Search className="w-4 h-4" />
                  <span>Execute Prior Art & Section 3(p) Search</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Results Output */}
      {searchResponse && (
        <div className="space-y-6">
          {/* Matched Herbs Cards */}
          {searchResponse.matched_herbs.length > 0 ? (
            searchResponse.matched_herbs.map((herb, idx) => (
              <div key={idx} className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 pb-4">
                  <div>
                    <h3 className="text-xl font-bold text-[#1a365d]">
                      {herb.herb_name} ({herb.sanskrit_name})
                    </h3>
                    <p className="text-xs text-gray-500 italic mt-0.5">
                      {herb.botanical_name} • Family: {herb.family}
                    </p>
                  </div>
                  <span className="px-3 py-1 bg-amber-50 text-amber-900 border border-amber-200 rounded-full text-xs font-mono font-medium">
                    TKRC: {herb.tkrc_class}
                  </span>
                </div>

                {/* Section 3(p) Rejection Risk Warning */}
                <div className="p-4 bg-amber-50/80 border border-amber-200 rounded-xl space-y-1.5">
                  <div className="flex items-center gap-2 text-amber-900 font-bold text-xs uppercase tracking-wider">
                    <AlertTriangle className="w-4 h-4 text-amber-600" />
                    <span>Section 3(p) Traditional Knowledge Rejection Risk</span>
                  </div>
                  <p className="text-xs text-amber-950 font-medium leading-relaxed">
                    {herb.section_3p_rejection_risk}
                  </p>
                </div>

                {/* Classical Treatises Verses */}
                <div className="space-y-3">
                  <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-[#2c7a7b]" />
                    <span>Documented Classical Treatises & Sanskrit Shlokas</span>
                  </h4>
                  <div className="grid grid-cols-1 gap-3">
                    {herb.classical_treatises.map((cit, cidx) => (
                      <div key={cidx} className="p-3.5 bg-gray-50 rounded-xl border border-gray-100 space-y-2 text-xs">
                        <div className="flex justify-between items-start">
                          <span className="font-bold text-[#1a365d]">{cit.treatise}</span>
                          {cit.verse_or_chapter && (
                            <span className="text-gray-500 font-mono text-[11px]">{cit.verse_or_chapter}</span>
                          )}
                        </div>
                        {cit.sanskrit_sloka && (
                          <div className="p-2.5 bg-white border border-amber-100 rounded-lg text-amber-900 font-serif text-xs italic">
                            "{cit.sanskrit_sloka}"
                          </div>
                        )}
                        <div className="flex flex-wrap gap-1.5 pt-1">
                          {cit.indications.map((ind, iidx) => (
                            <span key={iidx} className="px-2 py-0.5 bg-white border border-gray-200 text-gray-700 rounded text-[11px]">
                              {ind}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Famous Revocation Case Study */}
                {herb.famous_revocation_case && (
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
                      <ShieldAlert className="w-4 h-4 text-red-600" />
                      <span>Landmark International Patent Revocation Precedent</span>
                    </h4>
                    <div className="p-4 bg-red-50/60 border border-red-200 rounded-xl text-xs space-y-1.5">
                      <div className="flex justify-between font-bold text-red-950">
                        <span>{herb.famous_revocation_case.patent_number} ({herb.famous_revocation_case.patent_office})</span>
                        <span className="text-red-700 font-semibold">{herb.famous_revocation_case.outcome}</span>
                      </div>
                      <p className="text-gray-700 leading-relaxed">
                        <strong className="text-gray-900">Applicant:</strong> {herb.famous_revocation_case.applicant}
                      </p>
                      <p className="text-gray-700 leading-relaxed">
                        <strong className="text-gray-900">Challenged Claims:</strong> {herb.famous_revocation_case.disputed_claims}
                      </p>
                      <p className="text-gray-800 pt-1 font-medium">
                        <strong className="text-gray-900">Key Prior Art:</strong> {herb.famous_revocation_case.key_prior_art_cited}
                      </p>
                    </div>
                  </div>
                )}

                {/* Defensive Search Guidance */}
                <div className="p-4 bg-teal-50/60 border border-teal-200 rounded-xl space-y-1 text-xs">
                  <span className="font-bold text-[#2c7a7b] uppercase tracking-wider text-[11px]">
                    Defensive Strategy & Patent Prosecution Advice
                  </span>
                  <p className="text-teal-950 leading-relaxed">
                    {herb.defensive_search_guidance}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-8 text-center space-y-2">
              <BookOpen className="w-8 h-8 text-gray-400 mx-auto" />
              <h3 className="font-bold text-gray-800">No classical herb profile matched directly</h3>
              <p className="text-xs text-gray-500 max-w-md mx-auto">
                The term did not match our curated 15+ classical pharmacopoeial plants. Check the retrieved knowledge base provisions below.
              </p>
            </div>
          )}

          {/* RAG Retrieved Legal Provisions */}
          {searchResponse.rag_retrieved_provisions.length > 0 && (
            <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-3">
              <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#1a365d]" />
                <span>Statutory Knowledge Base Citations</span>
              </h4>
              <div className="space-y-2.5">
                {searchResponse.rag_retrieved_provisions.map((prov, pidx) => (
                  <div key={pidx} className="p-3.5 bg-gray-50 rounded-xl border border-gray-200 text-xs space-y-1">
                    <div className="flex justify-between items-center text-gray-600 font-semibold">
                      <span>{prov.source_title} {prov.section ? `• ${prov.section}` : ''}</span>
                      <span className="text-[10px] px-2 py-0.5 bg-white rounded border border-gray-200 text-[#2c7a7b] font-mono">
                        Score: {prov.score}
                      </span>
                    </div>
                    <p className="text-gray-700 leading-relaxed text-[11px] pt-1">
                      {prov.content}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Action Links */}
          <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-5 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-xs text-gray-600 text-center sm:text-left">
              Need comprehensive patentability assessment or Biological Diversity Act filing clearance?
            </div>
            <div className="flex gap-2.5">
              <Link
                to="/ip-assessment"
                className="px-4 py-2 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs font-semibold rounded-lg shadow-2xs inline-flex items-center gap-1.5"
              >
                <span>IP Route Assessment</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
              <Link
                to="/abs"
                className="px-4 py-2 bg-[#2c7a7b] hover:bg-[#235e5f] text-white text-xs font-semibold rounded-lg shadow-2xs inline-flex items-center gap-1.5"
              >
                <span>ABS Clearance</span>
                <ArrowRight className="w-3 h-3" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TKSearch;
