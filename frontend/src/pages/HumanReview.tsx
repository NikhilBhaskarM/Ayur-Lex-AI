import React, { useState } from 'react';
import { Users, Send, CheckCircle2, Clock, AlertTriangle, MessageSquare, Shield } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';

interface ReviewRequest {
  id: string;
  topic: string;
  userQuestion: string;
  aiAssessmentSummary: string;
  priority: 'Normal' | 'Urgent';
  status: 'new' | 'assigned' | 'in_review' | 'completed';
  facilitatorNotes?: string;
  createdAt: string;
}

const defaultReviews: ReviewRequest[] = [
  {
    id: 'hr-1',
    topic: 'Cross-Border Herbal Extract Export (EU Directive 2004/24/EC)',
    userQuestion: 'Can our Ayurvedic company export proprietary Bacopa monnieri extracts to Germany as traditional herbal medicine without full clinical trials?',
    aiAssessmentSummary: 'Requires 30 years medicinal use proof (15 years within EU) under THMPD. Recommended human regulatory attorney validation for German BfArM compliance.',
    priority: 'Urgent',
    status: 'in_review',
    facilitatorNotes: 'Reviewing documentation of 15-year historical sales in Netherlands and UK.',
    createdAt: '2026-09-02T10:00:00Z',
  },
  {
    id: 'hr-2',
    topic: 'Section 3(p) TKDL Avoidance for Modified Dosage Form',
    userQuestion: 'Does a sustained-release lipid tablet of classical Dashamoola constitute patentable non-obvious subject matter?',
    aiAssessmentSummary: 'High Section 3(p) and 3(d) rejection risk unless supported by pharmacokinetic sustained-release plasma concentration curves.',
    priority: 'Normal',
    status: 'new',
    createdAt: '2026-09-01T15:30:00Z',
  },
];

const HumanReview: React.FC = () => {
  const user = useAuthStore((s) => s.user);
  const isFacilitatorOrAdmin = user?.role === 'ADMIN' || user?.role === 'FACILITATOR';

  const [reviews, setReviews] = useState<ReviewRequest[]>(defaultReviews);
  const [topic, setTopic] = useState('');
  const [question, setQuestion] = useState('');
  const [priority, setPriority] = useState<'Normal' | 'Urgent'>('Normal');
  const [submitting, setSubmitting] = useState(false);

  // Facilitator note editing state
  const [selectedReview, setSelectedReview] = useState<ReviewRequest | null>(null);
  const [facilitatorNoteInput, setFacilitatorNoteInput] = useState('');

  const handleSubmitRequest = (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim() || !question.trim()) {
      toast.error('Please fill in both topic and details');
      return;
    }

    setSubmitting(true);
    const newReq: ReviewRequest = {
      id: `hr-${Date.now()}`,
      topic,
      userQuestion: question,
      aiAssessmentSummary: 'Submitted by user for facilitator review and statutory opinion.',
      priority,
      status: 'new',
      createdAt: new Date().toISOString(),
    };

    setReviews([newReq, ...reviews]);
    setTopic('');
    setQuestion('');
    setSubmitting(false);
    toast.success('Your query has been submitted to the human legal facilitator queue.');
  };

  const handleUpdateNote = (reviewId: string) => {
    if (!facilitatorNoteInput.trim()) return;

    setReviews(
      reviews.map((r) =>
        r.id === reviewId
          ? {
              ...r,
              facilitatorNotes: facilitatorNoteInput,
              status: 'completed',
            }
          : r
      )
    );

    if (selectedReview && selectedReview.id === reviewId) {
      setSelectedReview({
        ...selectedReview,
        facilitatorNotes: facilitatorNoteInput,
        status: 'completed',
      });
    }

    setFacilitatorNoteInput('');
    toast.success('Facilitator guidance updated.');
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
              Human Facilitator & Legal Expert Workflow
            </h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Escalate complex, edge-case, or high-stakes Ayurvedic IPR, ABS, and international regulatory questions to expert IP facilitators.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form to submit a review */}
        <div className="lg:col-span-1 bg-white rounded-xl border border-gray-200 p-5 shadow-2xs space-y-4 h-fit">
          <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2">
            Request Expert Review
          </h2>

          <form onSubmit={handleSubmitRequest} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Legal Area / Product Topic *
              </label>
              <input
                type="text"
                required
                placeholder="e.g., US FDA NDI vs Drug classification for Guggul"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Question & Specific Concerns *
              </label>
              <textarea
                rows={4}
                required
                placeholder="Describe the formulation, specific claims, jurisdictions of concern, or prior art ambiguities..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Priority Level
              </label>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <button
                  type="button"
                  onClick={() => setPriority('Normal')}
                  className={`p-2 border rounded-lg font-medium ${
                    priority === 'Normal' ? 'bg-[#1a365d] text-white border-[#1a365d]' : 'bg-gray-50 text-gray-700'
                  }`}
                >
                  Normal
                </button>
                <button
                  type="button"
                  onClick={() => setPriority('Urgent')}
                  className={`p-2 border rounded-lg font-medium ${
                    priority === 'Urgent' ? 'bg-red-600 text-white border-red-600' : 'bg-gray-50 text-gray-700'
                  }`}
                >
                  Urgent
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-[#1a365d] text-white rounded-lg text-xs font-bold hover:bg-[#0f2342] transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Submit for Human Review</span>
            </button>
          </form>

          <div className="text-[11px] text-gray-400 bg-gray-50 p-2.5 rounded-lg border border-gray-100">
            Facilitators typically review submissions within 24–48 hours and provide citation-grounded statutory annotations.
          </div>
        </div>

        {/* Review Queue & Details */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-bold text-gray-900">
            Active Review Queue ({reviews.length})
          </h2>

          <div className="space-y-3">
            {reviews.map((r) => {
              const isSelected = selectedReview?.id === r.id;
              const isDone = r.status === 'completed';
              const isInReview = r.status === 'in_review';

              return (
                <div
                  key={r.id}
                  onClick={() => setSelectedReview(r)}
                  className={`bg-white rounded-xl border p-4.5 cursor-pointer transition-all shadow-2xs ${
                    isSelected ? 'border-[#2c7a7b] ring-1 ring-[#2c7a7b]' : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex justify-between items-start gap-2">
                    <div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                            r.priority === 'Urgent' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-700'
                          }`}
                        >
                          {r.priority}
                        </span>
                        <span
                          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-medium ${
                            isDone
                              ? 'bg-green-100 text-green-800'
                              : isInReview
                              ? 'bg-blue-100 text-blue-800'
                              : 'bg-amber-100 text-amber-800'
                          }`}
                        >
                          {isDone ? <CheckCircle2 className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                          <span className="capitalize">{r.status.replace('_', ' ')}</span>
                        </span>
                      </div>
                      <h3 className="text-sm font-bold text-[#1a365d] mt-1.5">{r.topic}</h3>
                    </div>
                    <span className="text-[11px] text-gray-400">
                      {new Date(r.createdAt).toLocaleDateString()}
                    </span>
                  </div>

                  <p className="text-xs text-gray-700 mt-2 line-clamp-2">{r.userQuestion}</p>

                  {r.facilitatorNotes && (
                    <div className="mt-3 p-3 bg-emerald-50/70 border border-emerald-200 rounded-lg text-xs text-emerald-900">
                      <span className="font-bold block mb-0.5">Facilitator Guidance:</span>
                      {r.facilitatorNotes}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Facilitator Action Box (if admin/facilitator or item selected) */}
          {selectedReview && (
            <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-2xs space-y-3">
              <h3 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2">
                Facilitator Review Panel: {selectedReview.topic}
              </h3>

              <div className="text-xs space-y-2">
                <div>
                  <span className="font-bold text-gray-600 block">User Inquiry:</span>
                  <p className="text-gray-800 bg-gray-50 p-2.5 rounded-lg border border-gray-100 mt-0.5">
                    {selectedReview.userQuestion}
                  </p>
                </div>
                <div>
                  <span className="font-bold text-gray-600 block">AI Baseline Assessment:</span>
                  <p className="text-gray-800 bg-gray-50 p-2.5 rounded-lg border border-gray-100 mt-0.5">
                    {selectedReview.aiAssessmentSummary}
                  </p>
                </div>
              </div>

              {isFacilitatorOrAdmin && (
                <div className="pt-2 border-t border-gray-100 space-y-2">
                  <label className="block text-xs font-bold text-gray-700">
                    Add Expert Annotations & Recommendation:
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Enter statutory guidance, suggested section references, or recommended testing protocols..."
                    value={facilitatorNoteInput}
                    onChange={(e) => setFacilitatorNoteInput(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs outline-hidden focus:ring-2 focus:ring-[#2c7a7b]"
                  />
                  <div className="flex justify-end">
                    <button
                      type="button"
                      onClick={() => handleUpdateNote(selectedReview.id)}
                      className="px-4 py-2 bg-[#2c7a7b] text-white rounded-lg text-xs font-semibold hover:bg-[#235e5f]"
                    >
                      Complete Review & Post Guidance
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HumanReview;
