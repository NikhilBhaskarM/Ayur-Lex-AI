import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import SanitizedMarkdown from '../common/SanitizedMarkdown';
import { MapPin, Globe, AlertTriangle, MessageSquare, Zap, Scale, Cpu, ShieldCheck, UserCheck, Loader2 } from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';
import CitationCard from './CitationCard';
import { EscalationModal, EscalationDossierData } from '../common/EscalationModal';
import { apiClient } from '../../api/client';
import type { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  onSelectSuggestion?: (question: string) => void;
  onLaunchDebate?: (query?: string) => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onSelectSuggestion, onLaunchDebate }) => {
  const [isEscalating, setIsEscalating] = useState(false);
  const [showEscalateModal, setShowEscalateModal] = useState(false);
  const [dossier, setDossier] = useState<EscalationDossierData | null>(null);

  const handleEscalate = async () => {
    setIsEscalating(true);
    setShowEscalateModal(true);
    try {
      const res = await apiClient.post<EscalationDossierData>('/analytics/escalate', {
        query: message.content.slice(0, 300),
        assessment_answer: message.content,
        statutory_risk: message.statutory_risk || {},
        citations: message.citations || [],
        confidence_data: message.confidence || { level: 'HIGH', score: 0.95 },
        jurisdiction: message.jurisdiction || 'national',
      });
      setDossier(res.data);
    } catch (err) {
      console.error('Failed to generate attorney escalation dossier:', err);
    } finally {
      setIsEscalating(false);
    }
  };
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[85%] sm:max-w-[75%] bg-[#1a365d] text-white rounded-2xl rounded-tr-xs px-4 py-3 shadow-2xs">
          <p className="text-xs sm:text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
        </div>
      </div>
    );
  }

  const isIndia = (message.jurisdiction || '').toLowerCase().includes('india');
  const citations = message.citations || [];

  return (
    <div className="flex justify-start mb-6 w-full">
      <div className="w-full max-w-3xl bg-white border border-gray-200 shadow-2xs rounded-2xl rounded-tl-xs overflow-hidden">
        {/* Header Bar with Tier Telemetry */}
        <div className="bg-[#f8fafc] border-b border-gray-100 px-4 py-2.5 flex flex-wrap justify-between items-center gap-2">
          <div className="flex items-center space-x-2 text-xs font-semibold">
            {isIndia ? (
              <span className="inline-flex items-center gap-1 text-orange-800 bg-orange-50 border border-orange-200 px-2 py-0.5 rounded-md">
                <MapPin className="w-3.5 h-3.5 text-orange-600" />
                <span>🇮🇳 INDIA JURISDICTION</span>
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-blue-800 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded-md">
                <Globe className="w-3.5 h-3.5 text-blue-600" />
                <span>🌍 INTERNATIONAL FRAMEWORK</span>
              </span>
            )}

            {/* Non-Destructive Tier Badges */}
            {message.tier === 'simple' && (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold text-slate-700 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded-md">
                <Zap className="w-3 h-3 text-amber-500" />
                <span>TIER 1 (Fast Generative)</span>
              </span>
            )}

            {message.tier === 'statutory' && (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold text-blue-800 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded-md">
                <Cpu className="w-3 h-3 text-blue-600" />
                <span>TIER 2 (Statutory IRAC)</span>
              </span>
            )}

            {message.tier === 'debate' && (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono font-extrabold text-teal-900 bg-teal-100 border border-teal-300 px-2 py-0.5 rounded-md animate-pulse">
                <Scale className="w-3 h-3 text-teal-600" />
                <span>TIER 3 (Multi-LLM Chamber)</span>
              </span>
            )}
          </div>
          {message.confidence && <ConfidenceBadge level={message.confidence.level} />}
        </div>


        {/* Content Body */}
        <div className="px-5 py-4 prose prose-sm max-w-none text-gray-800 leading-relaxed">
          <SanitizedMarkdown>{message.content}</SanitizedMarkdown>
        </div>

        {/* Tier 3 Multi-Agent Chamber Action Banner */}
        {message.tier === 'debate' && (
          <div className="bg-gradient-to-r from-slate-950 via-teal-950 to-slate-900 border-t border-teal-500/40 p-4 text-white flex flex-wrap items-center justify-between gap-3">
            <div className="space-y-0.5">
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-teal-400 animate-ping" />
                <p className="text-xs font-bold text-teal-200">TIER 3 Multi-LLM Chamber Triggered</p>
              </div>
              <p className="text-[11px] text-slate-300">
                Adversarial debate available: Claude 3.5 Sonnet (Applicant) vs GPT-4o (Examiner) vs Judicial Arbiter.
              </p>
            </div>

            <div className="flex items-center gap-2">
              {onLaunchDebate ? (
                <button
                  type="button"
                  onClick={() => onLaunchDebate()}
                  className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-500 px-3.5 py-2 text-xs font-bold text-slate-950 shadow-md hover:brightness-110 transition cursor-pointer"
                >
                  <Scale size={14} />
                  Launch 3D Cyber-Cockpit
                </button>
              ) : (
                <Link
                  to="/chamber"
                  className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-500 px-3.5 py-2 text-xs font-bold text-slate-950 shadow-md hover:brightness-110 transition"
                >
                  <Scale size={14} />
                  Launch 3D Cyber-Cockpit
                </Link>
              )}
            </div>
          </div>
        )}

        {/* Citations List */}

        {citations.length > 0 && (
          <div className="bg-gray-50/70 px-5 py-3.5 border-t border-gray-100">
            <p className="text-xs font-bold text-gray-600 mb-2.5 uppercase tracking-wider flex items-center gap-1.5">
              <span>Authoritative Legal & Regulatory Citations</span>
              <span className="text-[10px] bg-gray-200 text-gray-700 px-1.5 py-0.2 rounded-full font-normal">
                {citations.length}
              </span>
            </p>
            <div className="grid gap-2">
              {citations.map((citation, idx) => (
                <CitationCard key={citation.chunk_id || idx} citation={citation} index={idx + 1} />
              ))}
            </div>
          </div>
        )}

        {/* Interactive Clarification & Follow-up Prompt Chips */}
        {message.clarification_questions && message.clarification_questions.length > 0 && (
          <div className="bg-[#f0fdf4] px-5 py-3.5 border-t border-emerald-100">
            <p className="text-xs font-bold text-emerald-900 mb-2 flex items-center gap-1.5">
              <MessageSquare className="w-3.5 h-3.5 text-emerald-600" />
              <span>Recommended Follow-ups & Details Needed:</span>
            </p>
            <div className="flex flex-wrap gap-2">
              {message.clarification_questions.map((q, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => onSelectSuggestion && onSelectSuggestion(q)}
                  className="text-xs bg-white hover:bg-emerald-50 text-emerald-900 border border-emerald-300 hover:border-emerald-400 font-medium px-3 py-1.5 rounded-full text-left transition-all shadow-2xs hover:shadow-xs cursor-pointer flex items-center gap-1.5"
                >
                  <span className="text-emerald-500">➜</span>
                  <span>{q}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Attorney Escalation Action Strip */}
        <div className="bg-slate-50 border-t border-slate-100 px-5 py-2.5 flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 text-[11px] text-slate-500 font-medium">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-600 shrink-0" />
            <span>DPDP Act 2023 Compliant • Registered Patent Agent Escalation</span>
          </div>

          <button
            type="button"
            onClick={handleEscalate}
            disabled={isEscalating}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold text-teal-900 bg-teal-100 hover:bg-teal-200 border border-teal-300 rounded-lg transition shadow-2xs cursor-pointer disabled:opacity-50"
          >
            {isEscalating ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-teal-700" />
            ) : (
              <UserCheck className="w-3.5 h-3.5 text-teal-700" />
            )}
            <span>Escalate to Patent Agent</span>
          </button>
        </div>

        {/* Legal Disclaimer Footer on Message */}
        <div className="bg-amber-50/50 border-t border-amber-100 px-4 py-2 flex items-center gap-2 text-[11px] text-amber-800">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          <span>{message.disclaimer || 'This information is for informational purposes only and does not constitute legal advice.'}</span>
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

export default MessageBubble;
