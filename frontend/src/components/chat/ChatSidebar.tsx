import React from 'react';
import { 
  MessageSquare, Plus, Trash2, Calendar, 
  ChevronLeft, ChevronRight, Scale, Clock, Sparkles
} from 'lucide-react';
import type { Conversation } from '@/types';

interface ChatSidebarProps {
  conversations: Conversation[];
  activeConversationId?: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string, e: React.MouseEvent) => void;
  isOpen: boolean;
  onToggle: () => void;
  isLoading?: boolean;
}

export const ChatSidebar: React.FC<ChatSidebarProps> = ({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  isOpen,
  onToggle,
  isLoading,
}) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/40 z-30 md:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 flex flex-col bg-[#0f172a] text-slate-200 border-r border-slate-800 transition-all duration-300 ease-in-out ${
          isOpen ? 'w-72 sm:w-80 translate-x-0' : 'w-0 -translate-x-full md:w-0 md:translate-x-0 overflow-hidden'
        }`}
      >
        {/* Top Header & New Consultation Button */}
        <div className="p-3.5 border-b border-slate-800/80 shrink-0 space-y-2.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-[#1a365d] rounded-lg text-amber-400">
                <Scale className="w-4 h-4" />
              </div>
              <span className="font-semibold text-xs tracking-wider uppercase text-slate-300">
                Consultation History
              </span>
            </div>
            <button
              type="button"
              onClick={onToggle}
              className="p-1 text-slate-400 hover:text-white rounded-md hover:bg-slate-800 transition-colors"
              title="Close sidebar"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
          </div>

          <button
            type="button"
            onClick={onNewChat}
            className="w-full flex items-center justify-center gap-2 py-2 px-3 bg-[#2c7a7b] hover:bg-[#285e61] text-white rounded-lg text-xs font-semibold shadow-sm transition-all group"
          >
            <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform duration-200" />
            <span>New Legal Consultation</span>
          </button>
        </div>

        {/* Conversation List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1 scrollbar-thin scrollbar-thumb-slate-700">
          {isLoading ? (
            <div className="p-4 text-center text-xs text-slate-500">
              <div className="w-5 h-5 border-2 border-slate-600 border-t-amber-400 rounded-full animate-spin mx-auto mb-2" />
              Loading history...
            </div>
          ) : conversations.length === 0 ? (
            <div className="p-6 text-center text-slate-500 text-xs space-y-2">
              <MessageSquare className="w-8 h-8 mx-auto text-slate-600 opacity-60" />
              <p>No previous conversations yet.</p>
              <p className="text-[11px] text-slate-600">
                Ask a question about Section 3(p), ABS, or Ayurvedic patentability to begin.
              </p>
            </div>
          ) : (
            conversations.map((convo) => {
              const isActive = convo.id === activeConversationId;
              const dateStr = convo.created_at
                ? new Date(convo.created_at).toLocaleDateString(undefined, {
                    month: 'short',
                    day: 'numeric',
                  })
                : '';

              return (
                <div
                  key={convo.id}
                  onClick={() => onSelectConversation(convo.id)}
                  className={`group relative flex items-center justify-between p-2.5 rounded-lg text-xs cursor-pointer transition-colors ${
                    isActive
                      ? 'bg-[#1e293b] text-white font-medium border border-slate-700 shadow-xs'
                      : 'text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-start gap-2.5 min-w-0 pr-6">
                    <MessageSquare
                      className={`w-3.5 h-3.5 mt-0.5 shrink-0 ${
                        isActive ? 'text-amber-400' : 'text-slate-500 group-hover:text-slate-400'
                      }`}
                    />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-xs text-slate-200 leading-snug">
                        {convo.title || 'Untitled Consultation'}
                      </p>
                      <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-500">
                        <span className="flex items-center gap-0.5">
                          <Clock className="w-2.5 h-2.5" />
                          {dateStr}
                        </span>
                        {convo.jurisdiction && (
                          <span className="px-1 py-0.2 bg-slate-800 rounded text-[9px] text-slate-400">
                            {convo.jurisdiction}
                          </span>
                        )}
                        {typeof convo.message_count === 'number' && convo.message_count > 0 && (
                          <span className="text-[9px] text-slate-500">
                            {convo.message_count} msg{convo.message_count > 1 ? 's' : ''}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Delete Conversation Button */}
                  <button
                    type="button"
                    onClick={(e) => onDeleteConversation(convo.id, e)}
                    className="absolute right-2 top-2.5 p-1 rounded text-slate-500 hover:text-red-400 hover:bg-red-500/10 opacity-0 group-hover:opacity-100 transition-all"
                    title="Delete consultation"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Footer Note */}
        <div className="p-3 border-t border-slate-800/80 text-[10px] text-slate-500 flex items-center justify-between shrink-0">
          <span className="flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-amber-500" />
            <span>AyurLex AI History</span>
          </span>
          <span className="font-mono text-[9px] text-slate-600">Secure DB</span>
        </div>
      </aside>
    </>
  );
};
export default ChatSidebar;
