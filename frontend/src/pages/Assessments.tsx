import React, { useState } from 'react';
import { FileText, Calendar, CheckCircle2, Search, ExternalLink, Printer, Filter } from 'lucide-react';
import { Link } from 'react-router-dom';
import ConfidenceBadge from '@/components/common/ConfidenceBadge';
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
      patent_status: 'Section 3(e) Synergism & Section 3(d) Enhanced Efficacy Data Required',
      statute: 'The Patents Act, 1970',
    },
    confidence: 'MEDIUM',
    status: 'completed',
    created_at: '2026-08-28T09:40:00Z',
  },
];

const Assessments: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>(defaultAssessments);
  const [search, setSearch] = useState('');
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);

  const filtered = assessments.filter(
    (a) =>
      a.assessment_type.toLowerCase().includes(search.toLowerCase()) ||
      (a.formulation_data?.name || '').toLowerCase().includes(search.toLowerCase()) ||
      a.jurisdiction.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-[#1a365d]/10 rounded-xl">
            <FileText className="w-6 h-6 text-[#1a365d]" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Saved Regulatory & IP Assessments
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Review and audit previous formulation analyses, ABS checklists, and patentability assessments.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search assessments..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden bg-white"
            />
          </div>
          <Link
            to="/classify"
            className="px-3.5 py-2 bg-[#1a365d] text-white rounded-lg text-xs font-semibold hover:bg-[#0f2342] shrink-0"
          >
            + New Assessment
          </Link>
        </div>
      </div>

      {/* List */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Left column: List of items */}
        <div className="md:col-span-2 space-y-3">
          {filtered.length === 0 ? (
            <div className="bg-white p-8 rounded-xl border border-gray-200 text-center text-gray-400">
              No saved assessments match your query.
            </div>
          ) : (
            filtered.map((item) => {
              const isSelected = selectedAssessment?.id === item.id;
              return (
                <div
                  key={item.id}
                  onClick={() => setSelectedAssessment(item)}
                  className={`bg-white rounded-xl border p-4.5 cursor-pointer transition-all shadow-2xs ${
                    isSelected
                      ? 'border-[#2c7a7b] ring-1 ring-[#2c7a7b] bg-[#e6fffa]/10'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50/50'
                  }`}
                >
                  <div className="flex justify-between items-start gap-2">
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[#2c7a7b]">
                        {item.assessment_type}
                      </span>
                      <h3 className="text-base font-semibold text-gray-900 mt-0.5">
                        {item.formulation_data?.name || 'Formulation Assessment'}
                      </h3>
                    </div>
                    <ConfidenceBadge level={item.confidence as any || 'HIGH'} />
                  </div>

                  <p className="text-xs text-gray-600 mt-2 font-medium">
                    {item.classification_result?.classification || item.classification_result?.abs_status || item.classification_result?.patent_status}
                  </p>

                  <div className="flex items-center justify-between mt-3.5 pt-3 border-t border-gray-100 text-[11px] text-gray-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                    <span className="px-2 py-0.5 bg-gray-100 rounded text-gray-700 font-medium">
                      {item.jurisdiction}
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right column: Detail Viewer */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-2xs h-fit space-y-4">
          {selectedAssessment ? (
            <>
              <div className="flex justify-between items-center border-b border-gray-100 pb-3">
                <h3 className="font-bold text-sm text-gray-900">Assessment Detail</h3>
                <button
                  type="button"
                  onClick={() => window.print()}
                  className="flex items-center gap-1 text-xs text-gray-500 hover:text-[#1a365d]"
                  title="Print Report"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Print</span>
                </button>
              </div>

              <div>
                <span className="text-[10px] text-gray-400 uppercase tracking-wider font-bold">Assessment Type</span>
                <p className="text-xs font-semibold text-[#1a365d]">{selectedAssessment.assessment_type}</p>
              </div>

              <div>
                <span className="text-[10px] text-gray-400 uppercase tracking-wider font-bold">Formulation Subject</span>
                <p className="text-xs font-semibold text-gray-900">{selectedAssessment.formulation_data?.name}</p>
                {selectedAssessment.formulation_data?.intended_use && (
                  <p className="text-[11px] text-gray-500 mt-0.5">{selectedAssessment.formulation_data.intended_use}</p>
                )}
              </div>

              <div>
                <span className="text-[10px] text-gray-400 uppercase tracking-wider font-bold">Statutory Conclusion</span>
                <p className="text-xs text-gray-800 bg-gray-50 p-2.5 rounded-lg border border-gray-100 mt-1 font-medium">
                  {selectedAssessment.classification_result?.classification || selectedAssessment.classification_result?.abs_status || selectedAssessment.classification_result?.patent_status}
                </p>
                {selectedAssessment.classification_result?.statute && (
                  <p className="text-[11px] text-gray-500 mt-1 font-mono">
                    Governing Law: {selectedAssessment.classification_result.statute}
                  </p>
                )}
              </div>

              <div className="pt-2 border-t border-gray-100">
                <Link
                  to="/review"
                  className="w-full flex items-center justify-center gap-1.5 py-2 px-3 bg-[#d69e2e] text-[#1a365d] rounded-lg text-xs font-bold hover:bg-[#b7791f] hover:text-white transition-colors"
                >
                  <span>Submit for Human Expert Review</span>
                </Link>
              </div>
            </>
          ) : (
            <div className="text-center py-10 text-gray-400 text-xs">
              <FileText className="w-8 h-8 mx-auto mb-2 text-gray-300" />
              <span>Select an assessment to view complete statutory breakdown.</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assessments;
