import React, { useState } from 'react';
import { Leaf, ShieldAlert, CheckCircle2, AlertTriangle, FileText, Scale, ExternalLink, RefreshCw } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

interface ABSChecklistItem {
  question: string;
  userAnswer: string;
  relevantProvision: string;
  whyItMatters: string;
  requiredAction: string;
  authority: string;
  confidence: 'HIGH' | 'MEDIUM' | 'LOW';
  needsHumanReview: boolean;
}

const ABSCompliance: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);

  // Form State
  const [involvesBioResource, setInvolvesBioResource] = useState<boolean | null>(null);
  const [sourceIsIndia, setSourceIsIndia] = useState<boolean | null>(null);
  const [entityType, setEntityType] = useState<'indian_citizen' | 'indian_entity' | 'foreign_or_nri' | null>(null);
  const [purpose, setPurpose] = useState<'commercial' | 'research' | 'bio_survey' | null>(null);
  const [isCultivated, setIsCultivated] = useState<boolean | null>(null);
  const [isAyushPractitioner, setIsAyushPractitioner] = useState<boolean | null>(null);
  const [isCodifiedTK, setIsCodifiedTK] = useState<boolean | null>(null);

  const [generatedChecklist, setGeneratedChecklist] = useState<ABSChecklistItem[] | null>(null);

  const handleEvaluate = () => {
    const checklist: ABSChecklistItem[] = [];

    // 1. Biological Resource Involvement
    checklist.push({
      question: 'Are Indian biological resources or associated knowledge involved?',
      userAnswer: involvesBioResource ? 'Yes' : 'No',
      relevantProvision: 'Section 2(c), Biological Diversity Act, 2002',
      whyItMatters: 'The Biological Diversity Act applies exclusively to biological resources and associated traditional knowledge.',
      requiredAction: involvesBioResource ? 'Verify biological origin and botanical taxon.' : 'No ABS obligations under the BD Act if no biological material is utilized.',
      authority: 'National Biodiversity Authority (NBA) / State Biodiversity Boards (SBB)',
      confidence: 'HIGH',
      needsHumanReview: false,
    });

    // 2. Entity Status & Section 3 vs Section 7
    if (entityType === 'foreign_or_nri') {
      checklist.push({
        question: 'Entity Categorization (Foreign, NRI, or Indian company with foreign shareholding/management)',
        userAnswer: 'Non-Indian / Foreign Entity (Section 3(2))',
        relevantProvision: 'Section 3(1) & Section 3(2), BD Act, 2002',
        whyItMatters: 'Foreign individuals, NRIs, and Indian entities with any foreign equity or control must obtain mandatory PRIOR APPROVAL from NBA before accessing resources or research results.',
        requiredAction: 'File NBA Form I (Access for research/commercial utilization) and enter into Access and Benefit Sharing Agreement.',
        authority: 'National Biodiversity Authority (NBA, Chennai)',
        confidence: 'HIGH',
        needsHumanReview: true,
      });
    } else {
      checklist.push({
        question: 'Entity Categorization (Indian Citizen or Indian Corporate Body)',
        userAnswer: 'Domestic Entity / Citizen (Section 7)',
        relevantProvision: 'Section 7, BD Act, 2002 (as amended by 2023 Amendment Act)',
        whyItMatters: 'Domestic Indian entities are regulated by State Biodiversity Boards (SBB) rather than NBA for domestic commercial exploitation.',
        requiredAction: 'Determine whether SBB prior intimation is required or covered under 2023 exemptions.',
        authority: 'State Biodiversity Board (SBB)',
        confidence: 'HIGH',
        needsHumanReview: false,
      });
    }

    // 3. 2023 Statutory Exemptions Check
    if (isAyushPractitioner) {
      checklist.push({
        question: 'Registered AYUSH Medical Practitioner Exemption',
        userAnswer: 'Yes — Registered Vaid / Hakim / AYUSH Practitioner',
        relevantProvision: 'Proviso to Section 7 (2023 Amendment Act)',
        whyItMatters: 'The 2023 Amendment explicitly exempts registered AYUSH medical practitioners practicing indigenous medicine for livelihood from SBB intimation and ABS payments.',
        requiredAction: 'Maintain proof of AYUSH state registration/license. No SBB ABS levy applies for personal clinical practice.',
        authority: 'State Licensing Authority / SBB',
        confidence: 'HIGH',
        needsHumanReview: false,
      });
    }

    if (isCodifiedTK) {
      checklist.push({
        question: 'Codified Traditional Knowledge Exemption',
        userAnswer: 'Yes — Utilization of Codified Traditional Knowledge (Classical texts)',
        relevantProvision: 'Proviso to Section 7 & Section 23 (2023 Amendment Act)',
        whyItMatters: 'Users of codified traditional knowledge are exempted from prior intimation to SBB and benefit-sharing levies under the 2023 framework.',
        requiredAction: 'Document the First Schedule classical textual citation supporting the formulation formula.',
        authority: 'State Biodiversity Board (SBB)',
        confidence: 'HIGH',
        needsHumanReview: true,
      });
    }

    if (isCultivated) {
      checklist.push({
        question: 'Cultivated Medicinal Plants Exemption',
        userAnswer: 'Yes — Sourced from cultivated medicinal plant farms',
        relevantProvision: 'Proviso to Section 7 & Section 40, BD Act (2023 Amendment)',
        whyItMatters: 'Cultivated medicinal plants are exempted from Section 7 access controls, shifting focus from wild harvested biodiversity.',
        requiredAction: 'Obtain Certificate of Origin / Cultivation certificate from farmer/producer or local Panchayat/BMC.',
        authority: 'Biodiversity Management Committee (BMC) / SBB',
        confidence: 'MEDIUM',
        needsHumanReview: true,
      });
    }

    // 4. IPR Filing Intent
    checklist.push({
      question: 'Intellectual Property Filing (Patents / Plant Varieties)',
      userAnswer: 'Potential Patent or IPR application',
      relevantProvision: 'Section 6(1) & Section 6(1A), BD Act',
      whyItMatters: 'Under Section 6(1), NBA approval was required before application. Under the 2023 Amendment (Section 6(1A)), Indian entities must REGISTER with the NBA prior to the grant of the patent. Benefit sharing applies upon commercial utilization.',
      requiredAction: 'File Form III registration with NBA before IPO patent grant. Ensure Section 10(4)(d)(ii) source disclosure in patent specification.',
      authority: 'National Biodiversity Authority (NBA) & Indian Patent Office',
      confidence: 'HIGH',
      needsHumanReview: true,
    });

    setGeneratedChecklist(checklist);
  };

  const resetForm = () => {
    setInvolvesBioResource(null);
    setSourceIsIndia(null);
    setEntityType(null);
    setPurpose(null);
    setIsCultivated(null);
    setIsAyushPractitioner(null);
    setIsCodifiedTK(null);
    setGeneratedChecklist(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Title */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-emerald-50 rounded-xl">
            <Leaf className="w-6 h-6 text-emerald-600" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              ABS Compliance Helper & Checklist Generator
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Evaluate Access and Benefit Sharing obligations under India's Biological Diversity Act 2002 & the 2023 Amendment Act.
            </p>
          </div>
        </div>
      </div>

      {/* Questionnaire */}
      {!generatedChecklist ? (
        <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
          <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
            Interactive Statutory ABS Questionnaire
          </h2>

          {/* Q1 */}
          <div className="space-y-2.5">
            <label className="block text-xs sm:text-sm font-medium text-gray-800">
              1. Does your product utilize any biological resource (herbs, botanicals, extracts, animal/mineral byproducts) originating from India?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setInvolvesBioResource(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  involvesBioResource === true ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Yes — Indian Biological Resource
              </button>
              <button
                type="button"
                onClick={() => setInvolvesBioResource(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  involvesBioResource === false ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                No — Purely Non-Indian / Synthetic
              </button>
            </div>
          </div>

          {/* Q2 */}
          <div className="space-y-2.5">
            <label className="block text-xs sm:text-sm font-medium text-gray-800">
              2. What is the legal status and citizenship of the applicant/entity?
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button
                type="button"
                onClick={() => setEntityType('indian_citizen')}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  entityType === 'indian_citizen' ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Indian Citizen (Individual)
              </button>
              <button
                type="button"
                onClick={() => setEntityType('indian_entity')}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  entityType === 'indian_entity' ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                100% Indian Owned Entity / MSME
              </button>
              <button
                type="button"
                onClick={() => setEntityType('foreign_or_nri')}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  entityType === 'foreign_or_nri' ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Foreign Entity / NRI / Foreign Equity
              </button>
            </div>
          </div>

          {/* Q3 */}
          <div className="space-y-2.5">
            <label className="block text-xs sm:text-sm font-medium text-gray-800">
              3. Are the medicinal plants sourced from registered agricultural cultivation?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setIsCultivated(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isCultivated === true ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Yes — Cultivated (Exemption Candidate)
              </button>
              <button
                type="button"
                onClick={() => setIsCultivated(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isCultivated === false ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                No — Wild Harvested / Forest Origin
              </button>
            </div>
          </div>

          {/* Q4 */}
          <div className="space-y-2.5">
            <label className="block text-xs sm:text-sm font-medium text-gray-800">
              4. Is the product directly based on codified traditional knowledge (classical texts like AFI, Charaka, Bhavaprakasha)?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setIsCodifiedTK(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isCodifiedTK === true ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Yes — Codified Traditional Knowledge
              </button>
              <button
                type="button"
                onClick={() => setIsCodifiedTK(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isCodifiedTK === false ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                No — Novel Folk Use or Non-Codified
              </button>
            </div>
          </div>

          {/* Q5 */}
          <div className="space-y-2.5">
            <label className="block text-xs sm:text-sm font-medium text-gray-800">
              5. Are you a registered AYUSH medical practitioner practicing indigenous medicine for livelihood?
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setIsAyushPractitioner(true)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isAyushPractitioner === true ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                Yes — Registered AYUSH Practitioner
              </button>
              <button
                type="button"
                onClick={() => setIsAyushPractitioner(false)}
                className={`p-3 border rounded-xl text-xs sm:text-sm font-medium transition-all ${
                  isAyushPractitioner === false ? 'border-emerald-600 bg-emerald-50/50 text-emerald-800 ring-1 ring-emerald-500' : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                No — Commercial Manufacturer / Innovator
              </button>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100 flex justify-end">
            <button
              type="button"
              disabled={involvesBioResource === null || entityType === null}
              onClick={handleEvaluate}
              className="px-6 py-2.5 bg-emerald-700 text-white rounded-lg text-sm font-semibold hover:bg-emerald-800 disabled:opacity-40 transition-colors shadow-2xs"
            >
              Generate ABS Compliance Checklist
            </button>
          </div>
        </div>
      ) : (
        /* Checklist Result */
        <div className="space-y-6">
          <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 pb-3">
              <div>
                <h2 className="text-lg font-bold text-[#1a365d]">ABS COMPLIANCE CHECKLIST</h2>
                <p className="text-xs text-gray-500">
                  Biological Diversity Act Statutory Review • Jurisdiction: {jurisdiction}
                </p>
              </div>
              <button
                type="button"
                onClick={resetForm}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Reset Questionnaire</span>
              </button>
            </div>

            <div className="space-y-4 pt-2">
              {generatedChecklist.map((item, idx) => (
                <div key={idx} className="border border-gray-200 rounded-xl p-4 space-y-3 bg-white hover:border-emerald-300 transition-colors">
                  <div className="flex items-start justify-between gap-3">
                    <div className="font-semibold text-sm text-[#1a365d] flex items-center gap-2">
                      <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 text-xs flex items-center justify-center font-bold shrink-0">
                        {idx + 1}
                      </span>
                      <span>{item.question}</span>
                    </div>
                    {item.needsHumanReview && (
                      <span className="shrink-0 inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-amber-100 text-amber-800 border border-amber-200">
                        <AlertTriangle className="w-3 h-3" />
                        Human Review Advised
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-gray-50 p-3 rounded-lg border border-gray-100">
                    <div>
                      <span className="font-bold text-gray-500 block uppercase tracking-wider text-[10px]">Your Answer</span>
                      <span className="text-gray-900 font-medium">{item.userAnswer}</span>
                    </div>
                    <div>
                      <span className="font-bold text-gray-500 block uppercase tracking-wider text-[10px]">Governing Provision</span>
                      <span className="text-[#1a365d] font-semibold">{item.relevantProvision}</span>
                    </div>
                  </div>

                  <div className="text-xs space-y-2">
                    <div>
                      <span className="font-bold text-gray-700">Why it matters:</span>{' '}
                      <span className="text-gray-600">{item.whyItMatters}</span>
                    </div>
                    <div>
                      <span className="font-bold text-emerald-800">Required Action / Documentation:</span>{' '}
                      <span className="text-gray-800 font-medium">{item.requiredAction}</span>
                    </div>
                    <div>
                      <span className="font-bold text-gray-500">Regulating Authority:</span>{' '}
                      <span className="text-[#2c7a7b] font-medium">{item.authority}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Disclaimer */}
            <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-800 flex items-start gap-2 mt-4">
              <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
              <span>
                <strong>Statutory Caveat:</strong> ABS compliance depends on precise contractual structures, export customs declarations, and local BMC registrations. This checklist reflects statutory guidelines under the BD Act and does not constitute formal clearance from the National Biodiversity Authority.
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ABSCompliance;
