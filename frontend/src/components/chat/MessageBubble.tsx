import React from 'react';
import ReactMarkdown from 'react-markdown';
import { MapPin, Globe, AlertTriangle, MessageSquare } from 'lucide-react';
import ConfidenceBadge from '../common/ConfidenceBadge';
import CitationCard from './CitationCard';
import type { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  onSelectSuggestion?: (question: string) => void;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, onSelectSuggestion }) => {
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
        {/* Header Bar */}
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
            {message.llm_model && (
              <span className="inline-flex items-center gap-1 text-slate-700 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded-md text-[11px] font-mono">
                <span>🤖 {message.llm_model}</span>
              </span>
            )}
          </div>
          {message.confidence && <ConfidenceBadge level={message.confidence.level} />}
        </div>

        {/* Content Body */}
        <div className="px-5 py-4 prose prose-sm max-w-none text-gray-800 leading-relaxed">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

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

        {/* Legal Disclaimer Footer on Message */}
        <div className="bg-amber-50/50 border-t border-amber-100 px-4 py-2 flex items-center gap-2 text-[11px] text-amber-800">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          <span>{message.disclaimer || 'This information is for informational purposes only and does not constitute legal advice.'}</span>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
