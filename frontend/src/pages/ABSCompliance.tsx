import React, { useState } from 'react';
import { 
  Leaf, ShieldAlert, CheckCircle2, AlertTriangle, FileText, 
  Scale, ExternalLink, RefreshCw, ArrowRight, Save
} from 'lucide-react';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { absApi, type ABSChecklistItem, type ABSEvaluationResponse } from '../api/abs';

const ABSCompliance: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);

  // Form State
  const [involvesBioResource, setInvolvesBioResource] = useState<boolean | null>(true);
  const [sourceIsIndia, setSourceIsIndia] = useState<boolean | null>(true);
  const [entityType, setEntityType] = useState<'indian_citizen' | 'indian_entity' | 'foreign_or_nri'>('indian_entity');
  const [purpose, setPurpose] = useState<'commercial' | 'research' | 'bio_survey'>('commercial');
  const [isCultivated, setIsCultivated] = useState<boolean | null>(false);
  const [isAyushPractitioner, setIsAyushPractitioner] = useState<boolean | null>(false);
  const [isCodifiedTK, setIsCodifiedTK] = useState<boolean | null>(true);
  const [appliesForIpr, setAppliesForIpr] = useState<boolean | null>(false);

  const [loading, setLoading] = useState(false);
  const [evaluationResponse, setEvaluationResponse] = useState<ABSEvaluationResponse | null>(null);

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const res = await absApi.evaluate({
        involves_bio_resource: involvesBioResource ?? true,
        source_is_india: sourceIsIndia ?? true,
        entity_type: entityType,
        purpose: purpose,
        is_cultivated: isCultivated ?? false,
        is_ayush_practitioner: isAyushPractitioner ?? false,
        is_codified_tk: isCodifiedTK ?? true,
        applies_for_ipr: appliesForIpr ?? false,
        jurisdiction: jurisdiction || 'India',
      });
      setEvaluationResponse(res);
      toast.success('ABS statutory compliance evaluated and saved to database!');
    } catch (err: any) {
      console.warn('Backend ABS evaluation offline, falling back to local evaluation:', err);
      // Fallback local evaluation
      const checklist: ABSChecklistItem[] = [
        {
          question: 'Are Indian biological resources or associated knowledge involved?',
          user_answer: involvesBioResource ? 'Yes' : 'No',
          relevant_provision: 'Section 2(c), Biological Diversity Act, 2002',
          why_it_matters: 'The Biological Diversity Act applies exclusively to biological resources and associated traditional knowledge.',
          required_action: involvesBioResource ? 'Verify biological origin and botanical taxon.' : 'No ABS obligations.',
          authority: 'National Biodiversity Authority (NBA) / State Biodiversity Boards (SBB)',
          confidence: 'HIGH',
          needs_human_review: false,
        },
      ];
      setEvaluationResponse({
        overall_status: entityType === 'foreign_or_nri' ? 'APPROVAL_REQUIRED_FROM_NBA' : 'INTIMATION_TO_SBB_REQUIRED',
        summary: 'Evaluated locally. Please connect backend for database persistence.',
        required_forms: entityType === 'foreign_or_nri' ? ['NBA Form I'] : ['SBB Prior Intimation Form'],
        benefit_sharing_applicable: entityType === 'foreign_or_nri',
        checklist: checklist,
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
          <div className="p-3 bg-emerald-50 rounded-xl">
            <Leaf className="w-6 h-6 text-emerald-600" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Access & Benefit Sharing (ABS) Compliance Evaluator
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Biological Diversity Act, 2002 & Biological Diversity (Amendment) Act, 2023 Statutory Filter.
            </p>
          </div>
        </div>
      </div>

      {/* Mandatory Statutory Notice */}
      <div className="p-4 bg-amber-50/80 border border-amber-200 rounded-xl text-xs sm:text-sm text-amber-900 flex items-start gap-3 shadow-2xs">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-amber-950">
            Critical Compliance Warning: Section 3 vs. Section 7 & Section 6 IPR Bar
          </p>
          <p className="text-xs text-amber-900 leading-relaxed">
            Non-compliance with the Biological Diversity Act carries severe civil liabilities. Under Section 6, applying for patent rights on Indian biological inventions without prior approval / registration with the National Biodiversity Authority (NBA) constitutes a statutory violation.
          </p>
        </div>
      </div>

      {/* Form Questions Card */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
        <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
          Statutory Entity & Resource Classification
        </h2>

        {/* Q1: Biological Resource */}
        <div className="space-y-2">
          <label className="block text-xs sm:text-sm font-semibold text-gray-800">
            1. Does your formulation or research involve plants, seeds, extracts, or microorganisms originating from India?
          </label>
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => setInvolvesBioResource(true)}
              className={`px-4 py-2 rounded-lg text-xs font-semibold border transition-all ${
                involvesBioResource === true
                  ? 'bg-emerald-50 border-emerald-500 text-emerald-800 ring-2 ring-emerald-500/20'
                  : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
              }`}
            >
              Yes (Indian Biological Resource)
            </button>
            <button
              type="button"
              onClick={() => setInvolvesBioResource(false)}
              className={`px-4 py-2 rounded-lg text-xs font-semibold border transition-all ${
                involvesBioResource === false
                  ? 'bg-gray-100 border-gray-400 text-gray-800'
                  : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
              }`}
            >
              No (Synthetic / Non-Biological)
            </button>
          </div>
        </div>

        {/* Q2: Entity Status */}
        <div className="space-y-2">
          <label className="block text-xs sm:text-sm font-semibold text-gray-800">
            2. What is the legal categorization of your organization / enterprise?
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { id: 'indian_citizen', label: 'Indian Citizen / Individual Vaidya' },
              { id: 'indian_entity', label: 'Domestic Indian Company (100% Indian)' },
              { id: 'foreign_or_nri', label: 'Foreign Entity / NRI / Any Foreign Equity' },
            ].map((opt) => (
              <button
                key={opt.id}
                type="button"
                onClick={() => setEntityType(opt.id as any)}
                className={`p-3 rounded-lg text-xs font-semibold border text-left transition-all ${
                  entityType === opt.id
                    ? 'bg-[#1a365d]/10 border-[#1a365d] text-[#1a365d] ring-2 ring-[#1a365d]/20'
                    : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Q3: Purpose */}
        <div className="space-y-2">
          <label className="block text-xs sm:text-sm font-semibold text-gray-800">
            3. What is the primary purpose of accessing the biological resource?
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { id: 'commercial', label: 'Commercial Utilization (Manufacturing / Sales)' },
              { id: 'research', label: 'Laboratory Research / Clinical Studies' },
              { id: 'bio_survey', label: 'Bio-survey / Bioutilization' },
            ].map((opt) => (
              <button
                key={opt.id}
                type="button"
                onClick={() => setPurpose(opt.id as any)}
                className={`p-3 rounded-lg text-xs font-semibold border text-left transition-all ${
                  purpose === opt.id
                    ? 'bg-[#2c7a7b]/10 border-[#2c7a7b] text-[#2c7a7b] ring-2 ring-[#2c7a7b]/20'
                    : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Q4: Exemptions (2023 Amendment) */}
        <div className="space-y-3 pt-2 border-t border-gray-100">
          <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
            Statutory Exemption Criteria (2023 Amendment Act)
          </span>

          <div className="space-y-2.5">
            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200/80 cursor-pointer">
              <input
                type="checkbox"
                checked={isCultivated ?? false}
                onChange={(e) => setIsCultivated(e.target.checked)}
                className="rounded border-gray-300 text-[#2c7a7b] focus:ring-[#2c7a7b] w-4 h-4"
              />
              <span className="text-xs text-gray-800">
                <strong>Cultivated Medicinal Plants:</strong> Raw herbs are sourced from registered cultivated farm produce rather than wild forest harvesting.
              </span>
            </label>

            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200/80 cursor-pointer">
              <input
                type="checkbox"
                checked={isAyushPractitioner ?? false}
                onChange={(e) => setIsAyushPractitioner(e.target.checked)}
                className="rounded border-gray-300 text-[#2c7a7b] focus:ring-[#2c7a7b] w-4 h-4"
              />
              <span className="text-xs text-gray-800">
                <strong>Registered AYUSH Practitioner:</strong> Practitioner of indigenous medicine practicing for livelihood.
              </span>
            </label>

            <label className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200/80 cursor-pointer">
              <input
                type="checkbox"
                checked={appliesForIpr ?? false}
                onChange={(e) => setAppliesForIpr(e.target.checked)}
                className="rounded border-gray-300 text-[#2c7a7b] focus:ring-[#2c7a7b] w-4 h-4"
              />
              <span className="text-xs text-gray-800">
                <strong>IPR / Patent Intent:</strong> Planning to file or have filed a patent application based on this biological research (Section 6 trigger).
              </span>
            </label>
          </div>
        </div>

        {/* Evaluate Button */}
        <div className="flex justify-end pt-4 border-t border-gray-100">
          <button
            type="button"
            onClick={handleEvaluate}
            disabled={loading}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs sm:text-sm font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Evaluating Statutory Compliance...</span>
              </>
            ) : (
              <>
                <Scale className="w-4 h-4" />
                <span>Evaluate ABS Obligations & Save Assessment</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Evaluation Results Card */}
      {evaluationResponse && (
        <div className="space-y-6">
          {/* Status Banner */}
          <div
            className={`p-5 rounded-xl border space-y-2 ${
              evaluationResponse.overall_status === 'APPROVAL_REQUIRED_FROM_NBA'
                ? 'bg-red-50 border-red-200 text-red-950'
                : evaluationResponse.overall_status === 'EXEMPTION_APPLICABLE'
                ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                : 'bg-blue-50 border-blue-200 text-blue-950'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold uppercase tracking-wider">
                Overall Determination
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-white/80 border border-current">
                {evaluationResponse.overall_status}
              </span>
            </div>
            <p className="text-sm font-medium leading-relaxed">
              {evaluationResponse.summary}
            </p>

            {/* Required Forms Badges */}
            {evaluationResponse.required_forms.length > 0 && (
              <div className="pt-2 flex flex-wrap items-center gap-2">
                <span className="text-xs font-bold">Mandatory Filings:</span>
                {evaluationResponse.required_forms.map((form, fidx) => (
                  <span
                    key={fidx}
                    className="px-2.5 py-1 bg-white text-gray-900 border border-gray-300 rounded-md text-xs font-mono font-semibold"
                  >
                    📄 {form}
                  </span>
                ))}
              </div>
            )}

            {evaluationResponse.estimated_benefit_sharing_rate && (
              <div className="text-xs pt-1 font-medium text-gray-700">
                <strong>Applicable Benefit Sharing Levy:</strong> {evaluationResponse.estimated_benefit_sharing_rate}
              </div>
            )}
          </div>

          {/* Checklist Table */}
          <div className="bg-white rounded-xl shadow-2xs border border-gray-200 overflow-hidden">
            <div className="p-4 px-6 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
              <h3 className="font-bold text-sm text-[#1a365d]">
                Statutory Compliance Breakdown & Required Actions
              </h3>
              <span className="text-xs text-gray-500 font-mono">
                {evaluationResponse.checklist.length} provisions audited
              </span>
            </div>

            <div className="divide-y divide-gray-100">
              {evaluationResponse.checklist.map((item, idx) => (
                <div key={idx} className="p-5 space-y-2 text-xs">
                  <div className="flex justify-between items-start">
                    <span className="font-bold text-gray-900 text-sm">{item.question}</span>
                    <span className="font-mono px-2 py-0.5 bg-gray-100 rounded text-[11px] text-gray-700 font-medium">
                      {item.relevant_provision}
                    </span>
                  </div>
                  <div className="text-gray-600">
                    <strong className="text-gray-800">Your Answer:</strong> {item.user_answer}
                  </div>
                  <p className="text-gray-600 leading-relaxed">
                    {item.why_it_matters}
                  </p>
                  <div className="p-3 bg-emerald-50/50 border border-emerald-100 rounded-lg text-emerald-950 font-medium flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <div>
                      <strong>Required Statutory Action:</strong> {item.required_action}
                      <div className="text-[11px] text-emerald-800 mt-0.5">
                        Competent Authority: {item.authority}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Assessment Saved Link */}
          {evaluationResponse.id && (
            <div className="p-4 bg-white rounded-xl border border-gray-200 shadow-2xs flex items-center justify-between">
              <div className="text-xs text-gray-600 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Assessment record saved to permanent database index.</span>
              </div>
              <Link
                to="/assessments"
                className="text-xs font-semibold text-[#2c7a7b] hover:underline inline-flex items-center gap-1"
              >
                <span>View in Saved Assessments</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ABSCompliance;
