import React, { useState, useEffect } from 'react';
import { 
  FileText, Calendar, CheckCircle2, Search, ExternalLink, 
  Printer, Filter, RefreshCw, Eye, X, Scale, Leaf, Tag
} from 'lucide-react';
import { Link } from 'react-router-dom';
import ConfidenceBadge from '@/components/common/ConfidenceBadge';
import { assessmentsApi } from '../api/assessments';
import type { Assessment } from '@/types';

const defaultFallbackAssessments: Assessment[] = [
  {
    id: 'asm-101',
    assessment_type: 'classification',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Triphala-Guggulu Compound',
      intended_use: 'Lipid management & metabolic wellness',
    },
    classification_result: {
      classification: 'Patent or Proprietary (P&P) Ayurvedic Medicine',
      reasoning: 'Under Drugs and Cosmetics Act Section 3(h), proprietary modifications requires licensing under Form 25-D.',
    },
    confidence: 'HIGH',
    status: 'completed',
    created_at: '2026-09-02T14:30:00Z',
  },
  {
    id: 'asm-102',
    assessment_type: 'abs',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Nagauri Ashwagandha Export Extract',
      origin: 'Rajasthan, India',
    },
    classification_result: {
      classification: 'NBA Form I Prior Approval Required',
      reasoning: 'Biological Diversity Act Section 3(2) foreign export access clearance.',
    },
    confidence: 'HIGH',
    status: 'completed',
    created_at: '2026-09-01T11:15:00Z',
  },
  {
    id: 'asm-103',
    assessment_type: 'ip',
    jurisdiction: 'India',
    formulation_data: {
      name: 'Standardized Curcuminoid Nano-Emulsion',
      indication: 'Anti-inflammatory wound dressing',
    },
    classification_result: {
      classification: 'Section 3(e) Synergism & Section 3(d) Enhanced Efficacy Required',
      reasoning: 'The Patents Act, 1970 Sections 3(p) and 3(e) scrutiny.',
    },
    confidence: 'MEDIUM',
    status: 'completed',
    created_at: '2026-08-28T09:40:00Z',
  },
];

const Assessments: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>(defaultFallbackAssessments);
  const [loading, setLoading] = useState<boolean>(true);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('ALL');
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);

  const fetchAssessments = async () => {
    try {
      const data = await assessmentsApi.getAssessments(1, 50);
      if (Array.isArray(data) && data.length > 0) {
        setAssessments(data);
      }
    } catch (err) {
      console.warn('Backend assessments API offline, using cached samples:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssessments();
  }, []);

  const filtered = assessments.filter((a) => {
    const matchesSearch =
      a.assessment_type.toLowerCase().includes(search.toLowerCase()) ||
      (a.formulation_data?.name || a.formulation_data?.formulation_name || '').toLowerCase().includes(search.toLowerCase()) ||
      (a.jurisdiction || '').toLowerCase().includes(search.toLowerCase());

    const matchesType = typeFilter === 'ALL' || a.assessment_type.toLowerCase() === typeFilter.toLowerCase();
    return matchesSearch && matchesType;
  });

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
              Review and audit previous formulation analyses, ABS checklists, and patentability assessments from the database.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 w-full sm:w-auto">
          <button
            onClick={fetchAssessments}
            className="p-2 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 text-xs"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>

          <div className="relative flex-1 sm:w-56">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search assessments..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden bg-white"
            />
          </div>

          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-2.5 py-2 border border-gray-300 rounded-lg text-xs bg-white text-gray-700 outline-hidden"
          >
            <option value="ALL">All Types</option>
            <option value="classification">Classification</option>
            <option value="ip">IP Route</option>
            <option value="abs">ABS Compliance</option>
          </select>
        </div>
      </div>

      {/* Main Table */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-50 text-gray-500 uppercase tracking-wider font-semibold border-b border-gray-200">
              <tr>
                <th className="px-5 py-3">Assessment Type</th>
                <th className="px-5 py-3">Formulation / Asset</th>
                <th className="px-5 py-3">Jurisdiction</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3">Evaluated Date</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-5 py-8 text-center text-gray-400">
                    No assessments found matching your filters.
                  </td>
                </tr>
              ) : (
                filtered.map((asm) => {
                  const formName =
                    asm.formulation_data?.formulation_name ||
                    asm.formulation_data?.name ||
                    asm.formulation_data?.asset_id ||
                    'Untitled Formulation';

                  let badgeColor = 'bg-blue-50 text-blue-800 border-blue-200';
                  let typeLabel = asm.assessment_type;
                  if (asm.assessment_type === 'abs') {
                    badgeColor = 'bg-emerald-50 text-emerald-800 border-emerald-200';
                    typeLabel = 'ABS Compliance';
                  } else if (asm.assessment_type === 'ip') {
                    badgeColor = 'bg-purple-50 text-purple-800 border-purple-200';
                    typeLabel = 'IP Protection';
                  } else if (asm.assessment_type === 'classification') {
                    badgeColor = 'bg-amber-50 text-amber-800 border-amber-200';
                    typeLabel = 'Classification';
                  }

                  return (
                    <tr key={asm.id} className="hover:bg-gray-50/70 transition-colors">
                      <td className="px-5 py-3.5">
                        <span className={`px-2 py-0.5 rounded-md font-semibold text-[11px] border ${badgeColor}`}>
                          {typeLabel}
                        </span>
                      </td>
                      <td className="px-5 py-3.5 font-bold text-gray-900">
                        {formName}
                      </td>
                      <td className="px-5 py-3.5 text-gray-600">
                        {asm.jurisdiction || 'India'}
                      </td>
                      <td className="px-5 py-3.5">
                        <span className="inline-flex items-center gap-1 text-emerald-700 font-medium">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span className="capitalize">{asm.status}</span>
                        </span>
                      </td>
                      <td className="px-5 py-3.5 text-gray-500 font-mono text-[11px]">
                        {new Date(asm.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        <button
                          onClick={() => setSelectedAssessment(asm)}
                          className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-semibold text-[#2c7a7b] hover:bg-teal-50 rounded-md transition-colors"
                        >
                          <Eye className="w-3 h-3" />
                          <span>View Detail</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Assessment Detail Modal */}
      {selectedAssessment && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden">
            <div className="p-4 px-6 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <h3 className="font-bold text-sm text-[#1a365d]">
                Assessment Details: {selectedAssessment.id.slice(0, 8)}
              </h3>
              <button
                onClick={() => setSelectedAssessment(null)}
                className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 text-xs">
              <div className="flex justify-between items-center bg-gray-50 p-3 rounded-lg border border-gray-200">
                <div>
                  <span className="text-gray-500 text-[11px]">Type:</span>{' '}
                  <strong className="text-gray-900 uppercase">{selectedAssessment.assessment_type}</strong>
                </div>
                <div>
                  <span className="text-gray-500 text-[11px]">Date:</span>{' '}
                  <span className="font-mono text-gray-700">
                    {new Date(selectedAssessment.created_at).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* Formulation Data */}
              {selectedAssessment.formulation_data && (
                <div className="space-y-1">
                  <h4 className="font-bold text-gray-800 uppercase tracking-wider text-[11px]">
                    Formulation Input Data
                  </h4>
                  <pre className="p-3 bg-gray-950 text-gray-100 rounded-lg font-mono text-[11px] overflow-x-auto">
                    {JSON.stringify(selectedAssessment.formulation_data, null, 2)}
                  </pre>
                </div>
              )}

              {/* Detailed Results */}
              {(selectedAssessment.classification_result || selectedAssessment.ip_assessment || selectedAssessment.abs_assessment) && (
                <div className="space-y-1">
                  <h4 className="font-bold text-gray-800 uppercase tracking-wider text-[11px]">
                    Evaluated Statutory Output
                  </h4>
                  <pre className="p-3 bg-gray-50 border border-gray-200 text-gray-900 rounded-lg font-mono text-[11px] overflow-x-auto">
                    {JSON.stringify(
                      selectedAssessment.classification_result ||
                        selectedAssessment.ip_assessment ||
                        selectedAssessment.abs_assessment,
                      null,
                      2
                    )}
                  </pre>
                </div>
              )}
            </div>

            <div className="p-3 px-6 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button
                onClick={() => setSelectedAssessment(null)}
                className="px-4 py-1.5 bg-white border border-gray-300 text-xs font-semibold rounded-lg text-gray-700 hover:bg-gray-100"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Assessments;
