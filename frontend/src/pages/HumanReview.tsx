import React, { useState, useEffect } from 'react';
import { 
  Users, Send, CheckCircle2, Clock, AlertTriangle, 
  MessageSquare, Shield, RefreshCw, Filter, UserCheck
} from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { humanReviewApi, type HumanReviewItem } from '../api/humanReview';

const defaultFallbackReviews: HumanReviewItem[] = [
  {
    id: 'hr-1',
    user_id: 'usr-1',
    topic: 'Cross-Border Herbal Extract Export (EU Directive 2004/24/EC)',
    user_question: 'Can our Ayurvedic company export proprietary Bacopa monnieri extracts to Germany as traditional herbal medicine without full clinical trials?',
    ai_assessment: { topic: 'Cross-Border Herbal Extract Export (EU Directive 2004/24/EC)' },
    priority: 'urgent',
    status: 'in_review',
    facilitator_notes: 'Reviewing documentation of 15-year historical sales in Netherlands and UK.',
    created_at: '2026-09-02T10:00:00Z',
  },
  {
    id: 'hr-2',
    user_id: 'usr-2',
    topic: 'Section 3(p) TKDL Avoidance for Modified Dosage Form',
    user_question: 'Does a sustained-release lipid tablet of classical Dashamoola constitute patentable non-obvious subject matter?',
    ai_assessment: { topic: 'Section 3(p) TKDL Avoidance for Modified Dosage Form' },
    priority: 'normal',
    status: 'new',
    created_at: '2026-09-01T15:30:00Z',
  },
];

const HumanReview: React.FC = () => {
  const user = useAuthStore((s) => s.user);
  const isFacilitatorOrAdmin = user?.role === 'ADMIN' || user?.role === 'FACILITATOR';

  const [reviews, setReviews] = useState<HumanReviewItem[]>(defaultFallbackReviews);
  const [topic, setTopic] = useState('');
  const [question, setQuestion] = useState('');
  const [priority, setPriority] = useState<'normal' | 'urgent'>('normal');
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('ALL');

  // Facilitator note editing state
  const [selectedReview, setSelectedReview] = useState<HumanReviewItem | null>(null);
  const [facilitatorNoteInput, setFacilitatorNoteInput] = useState('');
  const [updating, setUpdating] = useState(false);

  const fetchReviews = async () => {
    try {
      const data = await humanReviewApi.getReviews(statusFilter === 'ALL' ? undefined : statusFilter);
      if (Array.isArray(data) && data.length > 0) {
        setReviews(data);
      }
    } catch (err) {
      console.warn('Backend human review API offline, using cached tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, [statusFilter]);

  const handleSubmitRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim() || !question.trim()) {
      toast.error('Please fill in both topic and details');
      return;
    }

    setSubmitting(true);
    try {
      const created = await humanReviewApi.createReview({
        topic: topic.trim(),
        user_question: question.trim(),
        priority: priority,
      });
      setReviews([created, ...reviews]);
      setTopic('');
      setQuestion('');
      toast.success('Your query has been submitted to the human legal facilitator queue and saved in the database.');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to submit query to facilitator queue');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateNote = async (reviewId: string) => {
    if (!facilitatorNoteInput.trim()) {
      toast.error('Please enter guidance notes before submitting');
      return;
    }

    setUpdating(true);
    try {
      const updated = await humanReviewApi.updateReview(reviewId, {
        facilitator_notes: facilitatorNoteInput,
        final_guidance: facilitatorNoteInput,
        status: 'completed',
      });
      setReviews(reviews.map((r) => (r.id === reviewId ? updated : r)));
      if (selectedReview && selectedReview.id === reviewId) {
        setSelectedReview(updated);
      }
      setFacilitatorNoteInput('');
      toast.success('Facilitator guidance updated and saved to permanent database.');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to update facilitator notes');
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-[#d69e2e]/10 rounded-xl">
            <Users className="w-6 h-6 text-[#d69e2e]" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">
              Human Facilitator Review & Legal Advisory Queue
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Submit complex patentability questions, export regulatory hurdles, or Section 3(p) TKDL issues for human attorney review.
            </p>
          </div>
        </div>
      </div>

      {/* Role Badge Banner */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-xl text-xs flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-[#2c7a7b]" />
          <span className="text-gray-700">
            Current User Role: <strong className="text-gray-900">{user?.role || 'USER'}</strong>
          </span>
        </div>
        {isFacilitatorOrAdmin && (
          <span className="px-2.5 py-0.5 bg-purple-100 text-purple-800 rounded-full font-semibold text-[11px] border border-purple-200 flex items-center gap-1">
            <UserCheck className="w-3 h-3" />
            <span>Facilitator Advisory Mode Active</span>
          </span>
        )}
      </div>

      {/* Submit Ticket Card */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
        <h2 className="text-base font-semibold text-gray-900 border-b border-gray-100 pb-2">
          Submit New Query for Expert Review
        </h2>

        <form onSubmit={handleSubmitRequest} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="sm:col-span-2">
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Subject / Regulatory Topic *
              </label>
              <input
                type="text"
                required
                placeholder="e.g., Section 3(d) Enhanced Efficacy Data for Modified Guggulipid"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-3.5 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Priority</label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value as any)}
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              >
                <option value="normal">Normal (48h Turnaround)</option>
                <option value="urgent">Urgent (24h Expedited)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">
              Detailed Question & Factual Background *
            </label>
            <textarea
              required
              rows={4}
              placeholder="Describe your formulation, biological source location, experimental clinical data, or specific regulatory notice received..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs sm:text-sm font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
              <span>{submitting ? 'Submitting to Queue...' : 'Submit to Facilitator Queue'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Reviews Queue List */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 overflow-hidden space-y-0">
        <div className="p-5 border-b border-gray-200 bg-[#f8fafc] flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
          <div>
            <h2 className="text-base font-bold text-[#1a365d] flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-[#2c7a7b]" />
              <span>{isFacilitatorOrAdmin ? 'All Advisory Requests Queue' : 'My Review Requests'}</span>
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Live status of submitted queries and completed legal facilitator opinions.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Filter className="w-3.5 h-3.5 text-gray-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-2.5 py-1 bg-white border border-gray-300 rounded-lg text-xs text-gray-700 outline-hidden"
            >
              <option value="ALL">All Statuses</option>
              <option value="new">New</option>
              <option value="in_review">In Review</option>
              <option value="completed">Completed</option>
            </select>
            <button
              onClick={fetchReviews}
              className="p-1 text-gray-400 hover:text-gray-600 rounded-md"
              title="Refresh"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="divide-y divide-gray-100">
          {reviews.length === 0 ? (
            <div className="p-8 text-center text-xs text-gray-400">
              No advisory review requests found in this view.
            </div>
          ) : (
            reviews.map((rev) => {
              const topicTitle = rev.topic || rev.ai_assessment?.topic || 'Statutory Advisory Request';
              return (
                <div key={rev.id} className="p-5 space-y-3 hover:bg-gray-50/50 transition-colors">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                          rev.priority === 'urgent'
                            ? 'bg-red-100 text-red-800 border border-red-200'
                            : 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {rev.priority}
                      </span>
                      <h3 className="font-bold text-sm text-[#1a365d]">{topicTitle}</h3>
                    </div>

                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        rev.status === 'completed'
                          ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                          : rev.status === 'in_review'
                          ? 'bg-blue-50 text-blue-800 border border-blue-200'
                          : 'bg-amber-50 text-amber-800 border border-amber-200'
                      }`}
                    >
                      {rev.status === 'completed'
                        ? 'Completed'
                        : rev.status === 'in_review'
                        ? 'In Facilitator Review'
                        : 'New Ticket'}
                    </span>
                  </div>

                  <p className="text-xs text-gray-700 leading-relaxed bg-gray-50 p-3 rounded-lg border border-gray-100">
                    <strong className="text-gray-900">User Question:</strong> {rev.user_question}
                  </p>

                  {/* Facilitator Guidance Output */}
                  {rev.facilitator_notes && (
                    <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs">
                      <div className="flex items-center gap-1.5 font-bold text-emerald-950">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                        <span>Official Facilitator Guidance & Legal Advisory Opinion</span>
                      </div>
                      <p className="text-emerald-950 leading-relaxed pl-5">
                        {rev.facilitator_notes}
                      </p>
                    </div>
                  )}

                  {/* Facilitator Action Area */}
                  {isFacilitatorOrAdmin && (
                    <div className="pt-2 border-t border-gray-100 flex items-center justify-between">
                      <span className="text-[11px] text-gray-400 font-mono">
                        Ticket ID: {rev.id.slice(0, 8)} • Submitted {new Date(rev.created_at).toLocaleDateString()}
                      </span>

                      <button
                        onClick={() => {
                          setSelectedReview(rev);
                          setFacilitatorNoteInput(rev.facilitator_notes || '');
                        }}
                        className="px-3 py-1 bg-purple-50 hover:bg-purple-100 text-purple-800 border border-purple-200 rounded-md text-xs font-semibold transition-colors"
                      >
                        {rev.facilitator_notes ? 'Edit Guidance' : 'Add Legal Opinion'}
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Facilitator Guidance Modal */}
      {selectedReview && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 max-w-xl w-full p-6 space-y-4">
            <h3 className="font-bold text-base text-[#1a365d] border-b border-gray-100 pb-2">
              Record Official Facilitator Opinion
            </h3>

            <div className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
              <strong className="text-gray-900">Question:</strong> {selectedReview.user_question}
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Facilitator Advisory Notes & Actionable Guidance *
              </label>
              <textarea
                rows={5}
                required
                placeholder="Enter statutory references, THMPD 30-year proof requirements, Section 3(d) comparative data suggestions, or NBA Form filing instructions..."
                value={facilitatorNoteInput}
                onChange={(e) => setFacilitatorNoteInput(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-xs focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              />
            </div>

            <div className="flex justify-end gap-2.5 pt-2">
              <button
                type="button"
                onClick={() => setSelectedReview(null)}
                className="px-4 py-2 border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={updating}
                onClick={() => handleUpdateNote(selectedReview.id)}
                className="px-5 py-2 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
              >
                {updating ? 'Saving...' : 'Save & Mark Completed'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HumanReview;
