import React, { useState } from 'react';
import { 
  Shield, Scale, Tag, MapPin, Package, Sprout, 
  Lock, BookOpen, CheckCircle2, AlertTriangle, ArrowRight, RefreshCw, Save
} from 'lucide-react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { ipApi, type IPAssessmentResponse } from '../api/ip';

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
  const [selectedAsset, setSelectedAsset] = useState<string | null>('patent_formulation');
  const [formulationName, setFormulationName] = useState<string>('');
  const [saving, setSaving] = useState<boolean>(false);
  const [savedResponse, setSavedResponse] = useState<IPAssessmentResponse | null>(null);

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
          title: 'Classical Ancient Formulation (Public Domain Prior Art)',
          ipType: 'Defensive Traditional Knowledge',
          governingAct: 'First Schedule, Drugs & Cosmetics Act, 1940 / Patents Act Section 3(p)',
          keySections: 'Section 3(p), Patents Act, 1970',
          statutoryPrerequisites: [
            'Formulations described in authoritative Ayurvedic treatises (Charaka Samhita, Sushruta Samhita, etc.) belong to the common heritage of India.',
            'No commercial entity can obtain a private patent monopoly over classical textual recipes.',
          ],
          ayurvedicSpecificNuances: [
            'Exempt from patentability under Section 3(p).',
            'Exempt from clinical trial requirements for classical licensing under Rule 158-B.',
            'Commercial protection is achieved through brand name trademarking and distinctive packaging design copyright.',
          ],
          exclusionRisks: [
            'Absolute refusal under Section 3(p) if patent application is filed.',
            'Revocation of any granted patent through TKDL third-party pre-grant or post-grant opposition.',
          ],
          actionSteps: [
            'Apply for Classical ASU Drug Manufacturing License under Form 25-D from State Licensing Authority.',
            'Invest in strong, arbitrary trademark brand name registration in Class 5.',
            'Do NOT spend financial capital attempting to patent the classical herbal composition.',
          ],
        };

      case 'geographical_indication':
        return {
          title: 'Geographical Indication (GI) Assessment (GI Act, 1999)',
          ipType: 'Geographical Indication',
          governingAct: 'The Geographical Indications of Goods (Registration and Protection) Act, 1999',
          keySections: 'Section 2(1)(e), Section 8, Section 11',
          statutoryPrerequisites: [
            'Geographical Link: Reputation, quality, or characteristics must be essentially attributable to geographic origin.',
            'Collective Application: Must be applied for by an association of producers representing regional farmers/growers.',
          ],
          ayurvedicSpecificNuances: [
            'Applicable to regional Ayurvedic medicinal plants (e.g., Nagauri Ashwagandha, Malabar Pepper, Navara Rice).',
            'Provides collective territorial monopoly preventing unauthorized commercial exploitation.',
          ],
          exclusionRisks: [
            'Refusal if the geographic name has become a generic trade description across India.',
          ],
          actionSteps: [
            'Form or partner with a registered association of regional Ayurvedic herbal cultivators.',
            'Collate historical and agro-climatic evidence linking quality to geographic terrain.',
            'File GI Application with the Geographical Indications Registry in Chennai.',
          ],
        };

      case 'industrial_design':
        return {
          title: 'Packaging & Applicator Design Registration (Designs Act, 2000)',
          ipType: 'Industrial Design',
          governingAct: 'The Designs Act, 2000 & Designs Rules, 2001',
          keySections: 'Section 4, Section 5, Class 09 (Packaging / Containers)',
          statutoryPrerequisites: [
            'Novelty: Shape or surface ornamentation must be globally new and unpublished.',
            'Visual Appeal: Judged solely by aesthetic eye appeal, not functional mechanics.',
          ],
          ayurvedicSpecificNuances: [
            'Protects proprietary packaging bottles, herbal droppers, copper/brass dispensers, and applicator nozzles.',
            'Confers 10 years of initial copyright protection, extendable by 5 years to 15 years total.',
          ],
          exclusionRisks: [
            'Refusal if design is purely functional or standard industry shape.',
          ],
          actionSteps: [
            'Prepare 7-angle orthographic CAD drawings or photographs on white background.',
            'File Form-1 design application with Controller General of Patents, Designs & Trade Marks.',
          ],
        };

      case 'plant_variety':
        return {
          title: 'Medicinal Plant Variety Protection (PPV&FR Act, 2001)',
          ipType: 'Plant Variety Protection',
          governingAct: 'The Protection of Plant Varieties and Farmers Rights Act, 2001',
          keySections: 'Section 14, Section 15 (DUS Criteria)',
          statutoryPrerequisites: [
            'Distinctness: Distinguishable from all known plant varieties.',
            'Uniformity: Uniform in essential phenotypic characteristics.',
            'Stability: Remains stable after repeated seasonal propagation.',
          ],
          ayurvedicSpecificNuances: [
            'Protects novel high-bioactive cultivars of Ayurvedic medicinal plants developed through institutional breeding.',
            'Farmers retain traditional rights to save, use, and exchange seeds.',
          ],
          exclusionRisks: [
            'Rejection if plant variety fails multi-location DUS field trials.',
          ],
          actionSteps: [
            'Complete multi-location DUS testing protocol with authorized ICAR / NBPGR institutes.',
            'File registration application with the PPV&FR Authority in New Delhi.',
          ],
        };

      case 'trade_secret':
        return {
          title: 'Proprietary Processing Know-How & Trade Secrets',
          ipType: 'Trade Secret',
          governingAct: 'Indian Contract Act, 1872 & Common Law of Breach of Confidence',
          keySections: 'Section 27, Indian Contract Act; Common Law NDAs',
          statutoryPrerequisites: [
            'Secrecy: Information is not generally known or readily ascertainable.',
            'Commercial Value: Derives competitive advantage from being confidential.',
            'Reasonable Safeguards: Active physical, contractual, and digital security measures.',
          ],
          ayurvedicSpecificNuances: [
            'Protects proprietary extraction ratios, specialized purification (Shodhana) parameters, and temperature curves.',
            'Cannot protect publicly disclosed ingredients which must appear on Ayurvedic medicine labels.',
          ],
          exclusionRisks: [
            'Immediate loss of protection upon independent reverse-engineering or uncontracted employee disclosure.',
          ],
          actionSteps: [
            'Execute Non-Disclosure Agreements (NDAs) and non-compete covenants with laboratory and factory staff.',
            'Partition proprietary manufacturing phases so no single operative possesses complete formula parameters.',
          ],
        };

      default:
        return {
          title: 'Select an Asset Type',
          ipType: 'General',
          governingAct: 'Indian IPR Framework',
          keySections: 'Various Acts',
          statutoryPrerequisites: [],
          ayurvedicSpecificNuances: [],
          exclusionRisks: [],
          actionSteps: [],
        };
    }
  };

  const routeData = selectedAsset ? getRouteDetails(selectedAsset) : null;

  const handleSaveAssessment = async () => {
    if (!selectedAsset) return;

    setSaving(true);
    try {
      const res = await ipApi.evaluate({
        asset_id: selectedAsset,
        formulation_name: formulationName.trim() || undefined,
        jurisdiction: jurisdiction || 'India',
      });
      setSavedResponse(res);
      toast.success('IP protection route evaluated and saved to database!');
    } catch (err: any) {
      console.warn('Backend IP assessment offline:', err);
      toast.error('Failed to save assessment to backend database');
    } finally {
      setSaving(false);
    }
  };

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
              IP Protection Route Evaluator
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Identify the right statutory protection pathway (Patents, Trademarks, GI, Designs, Plant Varieties, or Trade Secrets) for your Ayurvedic asset.
            </p>
          </div>
        </div>
      </div>

      {/* Asset Selection Grid */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
        <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
          Step 1: Select Your Innovation Asset Type
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {ipAssets.map((asset) => {
            const isSelected = selectedAsset === asset.id;
            return (
              <button
                key={asset.id}
                type="button"
                onClick={() => {
                  setSelectedAsset(asset.id);
                  setSavedResponse(null);
                }}
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

        {/* Optional Name Input & Save */}
        <div className="pt-3 border-t border-gray-100 flex flex-col sm:flex-row gap-3 items-center justify-between">
          <input
            type="text"
            placeholder="Formulation or Brand Name (e.g., Dashamoola Lipid Emulsion)..."
            value={formulationName}
            onChange={(e) => setFormulationName(e.target.value)}
            className="w-full sm:w-80 px-3.5 py-2 border border-gray-300 rounded-lg text-xs outline-hidden focus:ring-2 focus:ring-purple-500"
          />

          <button
            type="button"
            disabled={saving || !selectedAsset}
            onClick={handleSaveAssessment}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2 bg-purple-700 hover:bg-purple-800 text-white text-xs font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50 shrink-0"
          >
            {saving ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Evaluating...</span>
              </>
            ) : (
              <>
                <Save className="w-3.5 h-3.5" />
                <span>Evaluate & Save Assessment</span>
              </>
            )}
          </button>
        </div>

        {savedResponse && (
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-emerald-900 flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Assessment saved to database index!</span>
            </span>
            <Link to="/assessments" className="font-semibold text-emerald-800 hover:underline">
              View in Saved Assessments →
            </Link>
          </div>
        )}
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
