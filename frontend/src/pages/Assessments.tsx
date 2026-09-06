import React, { useState } from 'react';
import {
  FileText,
  Calendar,
  CheckCircle2,
  Search,
  Printer,
  ArrowRight,
  ShieldCheck,
  Clock3,
  ClipboardCheck,
  UserCheck,
  Loader2,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import ConfidenceBadge from '@/components/common/ConfidenceBadge';
import { EscalationModal, EscalationDossierData } from '@/components/common/EscalationModal';
import { apiClient } from '@/api/client';
import type { Assessment } from '@/types';

const defaultAssessments: Assessment[] = [
  {
    id: 'asm-101',
    assessment_type: 'Formulation Classification',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Triphala-Guggulu Compound',
      intended_use: 'Lipid management & metabolic wellness',
    },
    classification_result: {
      classification: 'Patent or Proprietary (P&P) Ayurvedic Medicine',
      statute: 'Drugs and Cosmetics Act, Section 3(h)',
    },
    confidence: 'HIGH',
    status: 'completed',
    created_at: '2026-09-02T14:30:00Z',
  },
  {
    id: 'asm-102',
    assessment_type: 'ABS Compliance Review',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Nagauri Ashwagandha Export Extract',
      origin: 'Rajasthan, India',
    },
    classification_result: {
      abs_status: 'NBA Form I Prior Approval Required',
      statute: 'Biological Diversity Act, Section 3(2)',
    },
    confidence: 'HIGH',
    status: 'completed',
    created_at: '2026-09-01T11:15:00Z',
  },
  {
    id: 'asm-103',
    assessment_type: 'IP Patentability Pre-Screen',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Standardized Curcuminoid Nano-Emulsion',
      indication: 'Anti-inflammatory wound dressing',
    },
    classification_result: {
      patent_status:
        'Section 3(e) Synergism & Section 3(d) Enhanced Efficacy Data Required',
      statute: 'The Patents Act, 1970',
    },
    confidence: 'MEDIUM',
    status: 'completed',
    created_at: '2026-08-28T09:40:00Z',
  },
];

const Assessments: React.FC = () => {
  const [assessments] = useState<Assessment[]>(defaultAssessments);
  const [search, setSearch] = useState('');
  const [selectedAssessment, setSelectedAssessment] =
    useState<Assessment | null>(null);

  const [isEscalating, setIsEscalating] = useState(false);
  const [showEscalateModal, setShowEscalateModal] = useState(false);
  const [dossier, setDossier] = useState<EscalationDossierData | null>(null);

  const handleEscalate = async () => {
    if (!selectedAssessment) return;
    setIsEscalating(true);
    setShowEscalateModal(true);
    try {
      const summaryText = `Assessment Type: ${selectedAssessment.assessment_type}\nSubject: ${selectedAssessment.formulation_data?.name || 'Ayurvedic Formulation'}\nIntended Use: ${selectedAssessment.formulation_data?.intended_use || 'Therapeutic'}\nStatutory Result: ${selectedAssessment.classification_result?.classification || 'Adjudicated'}`;
      const res = await apiClient.post<EscalationDossierData>('/analytics/escalate', {
        query: selectedAssessment.formulation_data?.name || selectedAssessment.assessment_type,
        assessment_answer: summaryText,
        statutory_risk: { section_3p: 65, section_3e: 55, bda_clearance: 80 },
        citations: [],
        confidence_data: { level: selectedAssessment.confidence || 'HIGH', score: 0.92 },
        applicant_name: 'Applicant Confidential',
        jurisdiction: selectedAssessment.jurisdiction || 'national',
      });
      setDossier(res.data);
    } catch (err) {
      console.error('Failed to generate attorney escalation dossier:', err);
    } finally {
      setIsEscalating(false);
    }
  };

  const filtered = assessments.filter(
    (a) =>
      a.assessment_type.toLowerCase().includes(search.toLowerCase()) ||
      (a.formulation_data?.name || '')
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      a.jurisdiction.toLowerCase().includes(search.toLowerCase())
  );

  const getConclusion = (assessment: Assessment) =>
    assessment.classification_result?.classification ||
    assessment.classification_result?.abs_status ||
    assessment.classification_result?.patent_status ||
    'Assessment completed';

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">

      {/* HERO */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 p-7 sm:p-8 text-white shadow-xl">
        <div className="absolute -right-20 -top-24 h-72 w-72 rounded-full bg-teal-400/10 blur-3xl" />

        <div className="relative flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div>
            <div className="mb-3 flex items-center gap-2 text-xs font-bold tracking-widest text-teal-300">
              <ClipboardCheck size={17} />
              INTELLIGENCE WORKSPACE
            </div>

            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
              Saved Assessments
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              Review previous formulation analyses, ABS compliance checks and
              intellectual property assessments from your workspace.
            </p>
          </div>

          <Link
            to="/classify"
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-slate-900 transition hover:bg-teal-50"
          >
            New Assessment
            <ArrowRight size={17} />
          </Link>
        </div>
      </section>

      {/* STATS */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

        <div className="card">
          <div className="flex items-center justify-between">
            <div className="rounded-xl bg-teal-50 p-2.5 text-teal-700">
              <FileText size={19} />
            </div>
            <span className="text-xs font-semibold text-emerald-600">
              Active
            </span>
          </div>

          <p className="mt-4 text-2xl font-bold text-slate-900">
            {assessments.length}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Saved assessments
          </p>
        </div>

        <div className="card">
          <div className="rounded-xl bg-emerald-50 p-2.5 w-fit text-emerald-700">
            <CheckCircle2 size={19} />
          </div>

          <p className="mt-4 text-2xl font-bold text-slate-900">
            {assessments.filter((a) => a.status === 'completed').length}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Completed
          </p>
        </div>

        <div className="card">
          <div className="rounded-xl bg-blue-50 p-2.5 w-fit text-blue-700">
            <ShieldCheck size={19} />
          </div>

          <p className="mt-4 text-2xl font-bold text-slate-900">
            {assessments.filter((a) => a.confidence === 'HIGH').length}
          </p>

          <p className="text-xs text-slate-500 mt-1">
            High confidence
          </p>
        </div>

        <div className="card">
          <div className="rounded-xl bg-purple-50 p-2.5 w-fit text-purple-700">
            <Clock3 size={19} />
          </div>

          <p className="mt-4 text-2xl font-bold text-slate-900">
            2026
          </p>

          <p className="text-xs text-slate-500 mt-1">
            Current workspace
          </p>
        </div>

      </div>

      {/* SEARCH */}
      <section className="card">
        <div className="flex flex-col sm:flex-row sm:items-center gap-3">

          <div className="relative flex-1">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              type="text"
              placeholder="Search by assessment, formulation or jurisdiction..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
            />
          </div>

          <div className="rounded-xl bg-slate-100 px-4 py-3 text-xs font-semibold text-slate-600">
            {filtered.length} result{filtered.length !== 1 ? 's' : ''}
          </div>

        </div>
      </section>

      {/* CONTENT */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">

        {/* LIST */}
        <section className="lg:col-span-3 space-y-3">

          {filtered.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center">
              <Search className="mx-auto text-slate-300" size={38} />

              <h3 className="mt-4 font-bold text-slate-900">
                No assessments found
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Try another search term.
              </p>
            </div>
          ) : (
            filtered.map((item) => {
              const isSelected = selectedAssessment?.id === item.id;

              return (
                <button
                  type="button"
                  key={item.id}
                  onClick={() => setSelectedAssessment(item)}
                  className={`w-full text-left rounded-2xl border p-5 transition-all ${
                    isSelected
                      ? 'border-teal-500 bg-teal-50/30 shadow-md ring-1 ring-teal-500'
                      : 'border-slate-200 bg-white hover:border-slate-300 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">

                    <div className="min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-[10px] font-bold uppercase tracking-widest text-teal-600">
                          {item.assessment_type}
                        </span>

                        <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-500">
                          {item.jurisdiction}
                        </span>
                      </div>

                      <h3 className="mt-2 text-base font-bold text-slate-900 truncate">
                        {item.formulation_data?.name ||
                          'Formulation Assessment'}
                      </h3>

                      <p className="mt-2 line-clamp-2 text-xs leading-5 text-slate-500">
                        {getConclusion(item)}
                      </p>
                    </div>

                    <div className="shrink-0">
                      <ConfidenceBadge
                        level={(item.confidence as any) || 'HIGH'}
                      />
                    </div>

                  </div>

                  <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-3 text-[11px] text-slate-400">
                    <span className="flex items-center gap-1.5">
                      <Calendar size={13} />
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>

                    <span className="flex items-center gap-1 text-teal-600 font-semibold">
                      View details
                      <ArrowRight size={13} />
                    </span>
                  </div>
                </button>
              );
            })
          )}

        </section>

        {/* DETAIL */}
        <aside className="lg:col-span-2">

          <div className="sticky top-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

            {selectedAssessment ? (
              <>
                <div className="flex items-start justify-between border-b border-slate-100 pb-4">

                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-teal-600">
                      Assessment Detail
                    </p>

                    <h2 className="mt-1 text-lg font-bold text-slate-900">
                      Assessment Report
                    </h2>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={handleEscalate}
                      disabled={isEscalating}
                      className="flex items-center gap-1.5 rounded-lg border border-teal-300 bg-teal-50 px-3 py-2 text-xs font-bold text-teal-800 transition hover:bg-teal-100 cursor-pointer disabled:opacity-50"
                    >
                      {isEscalating ? <Loader2 size={14} className="animate-spin text-teal-700" /> : <UserCheck size={14} className="text-teal-700" />}
                      Escalate to Agent
                    </button>

                    <button
                      type="button"
                      onClick={() => window.print()}
                      className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
                    >
                      <Printer size={14} />
                      Print
                    </button>
                  </div>

                </div>

                <div className="space-y-5 mt-5">

                  {/* Type */}
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                      Assessment Type
                    </p>

                    <p className="mt-1 text-sm font-semibold text-slate-900">
                      {selectedAssessment.assessment_type}
                    </p>
                  </div>

                  {/* Subject */}
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                      Subject
                    </p>

                    <p className="mt-1 text-sm font-semibold text-slate-900">
                      {selectedAssessment.formulation_data?.name ||
                        'Formulation Assessment'}
                    </p>

                    {selectedAssessment.formulation_data?.intended_use && (
                      <p className="mt-1 text-xs text-slate-500">
                        {selectedAssessment.formulation_data.intended_use}
                      </p>
                    )}

                    {selectedAssessment.formulation_data?.origin && (
                      <p className="mt-1 text-xs text-slate-500">
                        Origin: {selectedAssessment.formulation_data.origin}
                      </p>
                    )}

                    {selectedAssessment.formulation_data?.indication && (
                      <p className="mt-1 text-xs text-slate-500">
                        Indication: {selectedAssessment.formulation_data.indication}
                      </p>
                    )}
                  </div>

                  {/* Confidence */}
                  <div className="rounded-xl bg-slate-50 border border-slate-100 p-4">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold text-slate-600">
                        Confidence
                      </span>

                      <ConfidenceBadge
                        level={(selectedAssessment.confidence as any) || 'HIGH'}
                      />
                    </div>
                  </div>

                  {/* Conclusion */}
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                      Statutory Conclusion
                    </p>

                    <div className="mt-2 rounded-xl border border-teal-100 bg-teal-50/50 p-4">
                      <p className="text-xs font-semibold leading-5 text-slate-800">
                        {getConclusion(selectedAssessment)}
                      </p>
                    </div>

                    {selectedAssessment.classification_result?.statute && (
                      <p className="mt-2 text-[11px] leading-5 text-slate-500">
                        <span className="font-semibold text-slate-700">
                          Governing law:
                        </span>{' '}
                        {selectedAssessment.classification_result.statute}
                      </p>
                    )}
                  </div>

                  {/* Review */}
                  <Link
                    to="/review"
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-900 px-4 py-3 text-xs font-bold text-white transition hover:bg-teal-700"
                  >
                    Submit for Human Expert Review
                    <ArrowRight size={15} />
                  </Link>

                </div>
              </>
            ) : (
              <div className="flex min-h-[420px] flex-col items-center justify-center text-center">

                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-600">
                  <FileText size={28} />
                </div>

                <h3 className="mt-5 font-bold text-slate-900">
                  Select an assessment
                </h3>

                <p className="mt-2 max-w-xs text-sm leading-6 text-slate-500">
                  Choose an assessment from the list to inspect its statutory
                  conclusion and supporting details.
                </p>

              </div>
            )}

          </div>
        </aside>

      </div>

      {/* DISCLAIMER */}
      <div className="rounded-2xl border border-amber-100 bg-white p-5">
        <div className="flex items-start gap-3">
          <AlertTriangleIcon />

          <div>
            <p className="text-sm font-semibold text-slate-800">
              Assessment records
            </p>

            <p className="mt-1 text-xs leading-5 text-slate-500">
              Saved assessments are intended for review and research support.
              Verify conclusions against current legislation, official
              publications and qualified professional advice.
            </p>
          </div>
        </div>
      </div>

      <EscalationModal
        isOpen={showEscalateModal}
        onClose={() => setShowEscalateModal(false)}
        dossier={dossier}
        isLoading={isEscalating}
      />
    </div>
  );
};

const AlertTriangleIcon = () => (
  <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-amber-50 text-amber-600">
    <span className="text-sm font-bold">!</span>
  </div>
);

export default Assessments;