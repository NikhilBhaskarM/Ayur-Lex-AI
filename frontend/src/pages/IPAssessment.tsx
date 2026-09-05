import React, { useState } from 'react';
import { 
  Shield, Scale, Tag, MapPin, Package, Sprout, 
  Lock, BookOpen, CheckCircle2, AlertTriangle, ArrowRight, RefreshCw 
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

interface IPRouteResult {
  title: string;
  ipType: string;
  governingAct: string;
  keySections: string;
  statutoryPrerequisites: string[];
  ayurvedicSpecificNuances: string[];
  exclusionRisks: string[];
  actionSteps: string[];
}

const IPAssessment: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);

  const ipAssets = [
    {
      id: 'patent_formulation',
      icon: Scale,
      label: 'New Formulation / Extraction Process',
      desc: 'Novel synergistic herbal combination, specialized extraction method, or novel delivery system',
    },
    {
      id: 'trademark_brand',
      icon: Tag,
      label: 'Brand Name / Product Name / Logo',
      desc: 'Distinctive commercial name, house mark, or packaging label design',
    },
    {
      id: 'classical_formulation',
      icon: BookOpen,
      label: 'Classical Ancient Formulation',
      desc: 'Time-tested Ayurvedic preparation straight from ancient texts (e.g., Chyawanprash, Triphala)',
    },
    {
      id: 'geographical_indication',
      icon: MapPin,
      label: 'Regional Medicinal Plant / Traditional Variety',
      desc: 'Herbs whose qualities are essentially attributable to regional geographical origin (e.g., Nagauri Ashwagandha)',
    },
    {
      id: 'industrial_design',
      icon: Package,
      label: 'Packaging Shape / Aesthetic Container',
      desc: 'Novel 3D shape of an Ayurvedic dispenser, herbal bottle, or medicinal applicator',
    },
    {
      id: 'plant_variety',
      icon: Sprout,
      label: 'New Medicinal Plant Variety / Cultivar',
      desc: 'Distinct, uniform, and stable bred variety of an Ayurvedic medicinal plant',
    },
    {
      id: 'trade_secret',
      icon: Lock,
      label: 'Confidential Manufacturing Secret',
      desc: 'Proprietary processing ratios, purification tricks, or confidential know-how kept undisclosed',
    },
  ];

  const getRouteDetails = (assetId: string): IPRouteResult => {
    switch (assetId) {
      case 'patent_formulation':
        return {
          title: 'Patent Protection Assessment (Patents Act, 1970)',
          ipType: 'Patent',
          governingAct: 'The Patents Act, 1970 (as amended)',
          keySections: 'Section 3(p), Section 3(d), Section 3(e), Section 10(4)(d)(ii)',
          statutoryPrerequisites: [
            'Novelty: Must not have been published anywhere in the world or documented in TKDL/classical texts.',
            'Inventive Step: Non-obvious to a person skilled in Ayurvedic pharmacology and modern phytochemistry.',
            'Industrial Application: Capable of industrial replication and manufacture.',
            'Synergism Requirement (Section 3(e)): Combinations of known herbs MUST show experimental quantitative synergistic therapeutic effect over individual herbs.',
            'Enhanced Efficacy (Section 3(d)): New forms or extracts of known substances require comparative clinical/pharmacological data demonstrating significantly superior therapeutic efficacy.',
          ],
          ayurvedicSpecificNuances: [
            'Section 3(p) bars patenting of traditional knowledge or mere aggregation of known properties of components.',
            'Mandatory biological disclosure under Section 10(4)(d)(ii) of source and geographical origin.',
            'Mandatory NBA registration/approval under Section 6 of Biological Diversity Act before grant.',
          ],
          exclusionRisks: [
            'Rejection under Section 3(p) if cited in TKDL.',
            'Rejection under Section 3(e) if ingredients merely perform their known textbook functions.',
            'Opposition under Section 25 on grounds of traditional folklore anticipation.',
          ],
          actionSteps: [
            'Conduct comprehensive TKDL and prior art search across international patent databases.',
            'Generate in vitro / in vivo synergism data with Combination Index (CI) calculation.',
            'Prepare draft specification with clear biological origin disclosure.',
            'File Form III registration with National Biodiversity Authority.',
          ],
        };

      case 'trademark_brand':
        return {
          title: 'Trademark Registration Assessment (Trade Marks Act, 1999)',
          ipType: 'Trade Mark',
          governingAct: 'The Trade Marks Act, 1999',
          keySections: 'Section 9(1)(b), Section 9(1)(c), Section 9(2)(b), Section 11',
          statutoryPrerequisites: [
            'Distinctiveness: Must distinguish applicant goods from others in the marketplace.',
            'Non-Descriptive: Must not merely describe the herb, ingredients, or therapeutic purpose.',
            'Class 5 (Pharmaceuticals / ASU Medicines) or Class 30 / 32 (Ayurveda Aahara / Dietary Foods) or Class 3 (Cosmetics).',
          ],
          ayurvedicSpecificNuances: [
            'Names of classical preparations in First Schedule texts (e.g., Chyawanprash, Triphala, Ashwagandharishta) are PUBLICI JURIS (public domain) and CANNOT be registered by any single entity (Dabur v. Baidyanath).',
            'Manufacturers must append their distinctive house mark (e.g., "XYZ Chyawanprash").',
            'Section 9(2)(b) bars marks hurting religious sentiments (e.g., claiming exclusive trademark monopoly over revered deities for drugs).',
            'Cadila Healthcare Supreme Court doctrine strictly enforces confusing similarity standards for medicinal marks.',
          ],
          exclusionRisks: [
            'Objection under Section 9(1)(b) if the mark directly translates to an Ayurvedic disease or herbal ingredient.',
            'Cancellation action by competitors if classical name is registered.',
          ],
          actionSteps: [
            'Perform phonetically similar mark search on the official IP India Trade Marks Registry.',
            'Avoid purely descriptive Sanskrit terminology as the primary trademark.',
            'File Form TM-A under relevant classes (Class 5 for ASU medicines, Class 30 for Ayurveda Aahara).',
          ],
        };

      case 'classical_formulation':
        return {
          title: 'Traditional Knowledge & Prior Art Route',
          ipType: 'Traditional Knowledge (Defensive Protection)',
          governingAct: 'Patents Act Section 3(p) & Biological Diversity Act 2023',
          keySections: 'Section 3(p), Patents Act 1970; First Schedule, Drugs & Cosmetics Act 1940',
          statutoryPrerequisites: [
            'Belongs to codified Indian public domain.',
            'Cannot be monopolized by patent by any company.',
            'Free to manufacture under Form 25-D ASU Classical License with adherence to Schedule T GMP.',
          ],
          ayurvedicSpecificNuances: [
            'Exempted from SBB prior intimation and ABS payments under 2023 Biodiversity Amendment Act for codified TK.',
            'Standardized by PCIM&H in Ayurvedic Pharmacopoeia of India (API) & Ayurvedic Formulary of India (AFI).',
          ],
          exclusionRisks: [
            'Any patent application filed on this formulation will be rejected under Section 3(p) via TKDL citation.',
          ],
          actionSteps: [
            'Verify exact textual formula in First Schedule treatise.',
            'Obtain State Licensing Authority classical manufacturing license.',
            'Protect commercial identity via distinctive house trademark rather than patenting formulation.',
          ],
        };

      case 'geographical_indication':
        return {
          title: 'Geographical Indication (GI) Assessment',
          ipType: 'Geographical Indication',
          governingAct: 'Geographical Indications of Goods (Registration and Protection) Act, 1999',
          keySections: 'Section 2(1)(e), Section 18, Section 21',
          statutoryPrerequisites: [
            'Goods originating in a defined territory where unique quality/reputation is attributable to geography.',
            'Application must be made by an Association of Producers or statutory body representing cultivators, not a single private commercial firm.',
          ],
          ayurvedicSpecificNuances: [
            'Dravyaguna science recognizes "Desha" (habitat) potency variations (e.g., Nagauri Ashwagandha, Navara Rice, Waigaon Turmeric).',
            'Authorized users gain statutory right to use the official GI tag, commanding premium export pricing and anti-counterfeiting protection.',
          ],
          exclusionRisks: [
            'Rejection if applicant cannot prove historical association with the geographical territory.',
          ],
          actionSteps: [
            'Form or collaborate with a regional herbal producers cooperative or association.',
            'Collate historical, agro-climatic, and chemical fingerprinting data.',
            'File application at GI Registry in Chennai.',
          ],
        };

      default:
        return {
          title: 'Intellectual Property Strategy',
          ipType: 'Specialized IP',
          governingAct: 'Relevant IP Statutes',
          keySections: 'Applicable Provisions',
          statutoryPrerequisites: ['Assessment depending on exact asset details.'],
          ayurvedicSpecificNuances: ['Subject to Indian statutory boundaries.'],
          exclusionRisks: ['Ensure compliance with public domain and biodiversity rules.'],
          actionSteps: ['Consult human legal facilitator.'],
        };
    }
  };

  const routeData = selectedAsset ? getRouteDetails(selectedAsset) : null;

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-purple-50 rounded-xl">
            <Shield className="w-6 h-6 text-purple-600" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Ayurvedic IP Decision Engine & Router
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Identify the legally viable intellectual property mechanism for your Ayurvedic invention, brand, packaging, or plant variety.
            </p>
          </div>
        </div>
      </div>

      {/* Asset Selection Grid */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
        <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
          Select the Primary Asset You Want to Protect:
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-2">
          {ipAssets.map((asset) => {
            const isSelected = selectedAsset === asset.id;
            return (
              <button
                key={asset.id}
                type="button"
                onClick={() => setSelectedAsset(asset.id)}
                className={`p-4 border rounded-xl text-left transition-all flex items-start gap-3.5 ${
                  isSelected
                    ? 'border-purple-600 bg-purple-50/50 ring-1 ring-purple-500 shadow-2xs'
                    : 'border-gray-200 hover:bg-gray-50/80 hover:border-gray-300'
                }`}
              >
                <div className={`p-2.5 rounded-lg shrink-0 ${isSelected ? 'bg-purple-600 text-white' : 'bg-gray-100 text-gray-600'}`}>
                  <asset.icon className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-900">{asset.label}</h3>
                  <p className="text-xs text-gray-500 mt-1 leading-relaxed">{asset.desc}</p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Route Assessment Output */}
      {routeData && (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-gray-100 pb-4">
            <div>
              <span className="text-xs font-bold text-purple-700 uppercase tracking-wider">
                Recommended Protection Route
              </span>
              <h2 className="text-xl sm:text-2xl font-bold text-[#1a365d] mt-1">
                {routeData.title}
              </h2>
              <p className="text-xs text-gray-500 mt-0.5">
                Governing Act: {routeData.governingAct} • Key Provisions: {routeData.keySections}
              </p>
            </div>
            <span className="px-3 py-1 bg-purple-100 text-purple-800 text-xs font-bold rounded-full border border-purple-200">
              {routeData.ipType} Route
            </span>
          </div>

          {/* Statutory Prerequisites */}
          <div className="space-y-2.5">
            <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Statutory Prerequisites & Legal Standards</span>
            </h3>
            <ul className="space-y-2 bg-gray-50 p-4 rounded-xl border border-gray-100">
              {routeData.statutoryPrerequisites.map((req, i) => (
                <li key={i} className="text-xs sm:text-sm text-gray-700 flex items-start gap-2">
                  <span className="text-purple-600 font-bold">•</span>
                  <span>{req}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Ayurvedic Specific Nuances */}
          <div className="space-y-2.5">
            <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-1.5">
              <Scale className="w-4 h-4 text-[#1a365d]" />
              <span>Ayurvedic & Traditional Knowledge Specific Legal Filters</span>
            </h3>
            <div className="space-y-2">
              {routeData.ayurvedicSpecificNuances.map((nuance, i) => (
                <div key={i} className="p-3 bg-blue-50/50 border border-blue-100 rounded-lg text-xs sm:text-sm text-gray-800">
                  {nuance}
                </div>
              ))}
            </div>
          </div>

          {/* Exclusion Risks */}
          <div className="space-y-2.5">
            <h3 className="text-xs font-bold text-amber-800 uppercase tracking-wider flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Key Statutory Exclusion & Refusal Risks</span>
            </h3>
            <ul className="space-y-1.5">
              {routeData.exclusionRisks.map((risk, i) => (
                <li key={i} className="text-xs text-amber-900 bg-amber-50 p-2.5 rounded-lg border border-amber-200">
                  ⚠️ {risk}
                </li>
              ))}
            </ul>
          </div>

          {/* Action Steps */}
          <div className="space-y-2.5 pt-2">
            <h3 className="text-xs font-bold text-gray-700 uppercase tracking-wider">
              Recommended Next Action Steps
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {routeData.actionSteps.map((step, i) => (
                <div key={i} className="p-3.5 bg-white border border-gray-200 rounded-lg text-xs text-gray-800 font-medium flex items-start gap-2 shadow-2xs">
                  <span className="font-bold text-[#1a365d] bg-gray-100 w-5 h-5 rounded-full flex items-center justify-center shrink-0">
                    {i + 1}
                  </span>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Legal Disclaimer */}
          <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-600 text-center">
            This information is for informational purposes only and does not constitute legal advice. Patentability and trademark registrability determinations are subject to official prosecution by the Controller General of Patents, Designs and Trade Marks.
          </div>
        </div>
      )}
    </div>
  );
};

export default IPAssessment;
