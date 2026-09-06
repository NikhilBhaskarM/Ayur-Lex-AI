import React, { useState, useRef, useEffect } from 'react';
import { Send, MapPin, AlertCircle, RefreshCw, PanelLeft, PanelLeftClose } from 'lucide-react';
import toast from 'react-hot-toast';
import MessageBubble from './MessageBubble';
import { useAuthStore } from '@/store/authStore';
import { chatApi } from '@/api/chat';
import type { Message, Citation, ConfidenceResponse } from '@/types';

interface ChatInterfaceProps {
  activeConversationId?: string;
  onConversationCreated?: (newId: string) => void;
  sidebarOpen?: boolean;
  onToggleSidebar?: () => void;
  onNewChat?: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  activeConversationId,
  onConversationCreated,
  sidebarOpen,
  onToggleSidebar,
  onNewChat,
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingConversation, setIsLoadingConversation] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(activeConversationId);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const jurisdiction = useAuthStore((s) => s.jurisdiction);
  const language = useAuthStore((s) => s.language);
  const llmProvider = useAuthStore((s) => s.llmProvider);
  const llmModel = useAuthStore((s) => s.llmModel);
  const llmApiKey = useAuthStore((s) => s.llmApiKey);
  const llmBaseUrl = useAuthStore((s) => s.llmBaseUrl);

  // Sync with prop when parent selects a conversation from history
  useEffect(() => {
    setConversationId(activeConversationId);
    if (activeConversationId) {
      loadConversationHistory(activeConversationId);
    } else {
      setMessages([]);
    }
  }, [activeConversationId]);

  const loadConversationHistory = async (id: string) => {
    setIsLoadingConversation(true);
    try {
      const data = await chatApi.getConversation(id);
      if (data && Array.isArray(data.messages)) {
        const mapped: Message[] = data.messages.map((m: any) => ({
          id: m.id,
          role: m.role,
          content: m.content,
          citations: m.citations || [],
          confidence: m.confidence
            ? {
                level: m.confidence,
                score: m.confidence_score ?? 0.5,
                factors: m.confidence_data || {},
              }
            : undefined,
          confidence_score: m.confidence_score,
          jurisdiction: data.jurisdiction || jurisdiction,
          timestamp: m.created_at,
          created_at: m.created_at,
        }));
        setMessages(mapped);
      }
    } catch (err) {
      toast.error('Could not load consultation history');
    } finally {
      setIsLoadingConversation(false);
    }
  };

  const exampleQuestions = [
    "Can I patent my Ayurvedic formulation?",
    "What permissions are required for an Ayurvedic product?",
    "Is this formulation traditional knowledge?",
    "Do I need biodiversity approval under the BD Act?",
    "Can I export this Ayurvedic product to Europe?",
    "Can I register this Ayurvedic brand as a trademark?",
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMessageText = text.trim();
    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: userMessageText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatApi.sendMessage({
        message: userMessageText,
        conversation_id: conversationId,
        jurisdiction: jurisdiction,
        language: language || 'en',
        llm_provider: llmProvider,
        llm_model: llmModel,
        llm_api_key: llmApiKey || undefined,
        llm_base_url: llmBaseUrl || undefined,
      });

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
        onConversationCreated?.(response.conversation_id);
      }

      const assistantMsg: Message = {
        id: response.message_id || `asst-${Date.now()}`,
        role: 'assistant',
        content: response.answer,
        citations: response.citations || [],
        confidence: response.confidence,
        jurisdiction: response.jurisdiction || jurisdiction,
        llm_provider: response.llm_provider || llmProvider,
        llm_model: response.llm_model || llmModel,
        clarification_questions: response.clarification_questions || [],
        disclaimer: response.disclaimer,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const detail =
        err.response?.data?.detail ||
        err.message ||
        'Unable to reach the legal AI service. Please ensure the backend is running.';
      toast.error(detail);

      const errorMsg: Message = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `**Error:** ${detail}\n\n*Please ensure the knowledge base and backend are initialized.*`,
        confidence: { level: 'LOW', score: 0.0 },
        jurisdiction: jurisdiction,
        disclaimer: 'This information is for informational purposes only and does not constitute legal advice.',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setConversationId(undefined);
    setInput('');
    onNewChat?.();
  };

  return (
    <div className="flex flex-col h-full max-h-full bg-white rounded-r-xl overflow-hidden">
      {/* Header Info */}
      <div className="bg-[#f8fafc] px-4 py-3 border-b border-gray-200 flex justify-between items-center shrink-0">
        <div className="flex items-center gap-2.5">
          {onToggleSidebar && (
            <button
              type="button"
              onClick={onToggleSidebar}
              className="p-1.5 rounded-lg border border-gray-200 bg-white text-gray-600 hover:text-[#1a365d] hover:bg-gray-50 transition-colors"
              title={sidebarOpen ? "Hide history" : "Show history"}
            >
              {sidebarOpen ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeft className="w-4 h-4" />}
            </button>
          )}
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base sm:text-lg font-semibold text-[#1a365d]">
                Ayurvedic IPR & Regulatory Assistant
              </h2>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-[#1a365d]/10 text-[#1a365d]">
                {jurisdiction === 'India' ? '🇮🇳 India Law' : '🌍 International'}
              </span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-mono bg-slate-100 text-slate-700 border border-slate-200">
                <span>🤖 {llmModel || 'llama3.1:8b'}</span>
              </span>
            </div>
            <p className="text-xs text-gray-500">
              Citation-grounded, version-aware intelligence for AYUSH innovators
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              type="button"
              onClick={startNewChat}
              className="flex items-center gap-1 text-xs text-gray-600 hover:text-[#1a365d] bg-white border border-gray-200 px-2.5 py-1.5 rounded-lg shadow-2xs hover:bg-gray-50 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>New Query</span>
            </button>
          )}
        </div>
      </div>

      {/* Message Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {isLoadingConversation ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-3 py-16 text-slate-500 text-xs">
            <div className="w-8 h-8 border-3 border-slate-200 border-t-[#2c7a7b] rounded-full animate-spin" />
            <p className="font-medium text-slate-600">Retrieving consultation transcript & citations...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center space-y-5 max-w-2xl mx-auto py-8">
            <div className="bg-[#1a365d]/5 p-4 rounded-2xl">
              <MapPin className="w-10 h-10 text-[#2c7a7b]" />
            </div>
            <div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-800">
                Ask an Ayurvedic IPR & Regulatory Question
              </h3>
              <p className="mt-1.5 text-xs sm:text-sm text-gray-500 max-w-md">
                Get answers backed by statutory citations from the Patents Act, Drugs & Cosmetics Act, Biological Diversity Act, and FSSAI Ayurveda-Aahara regulations.
              </p>
            </div>
            <div className="w-full">
              <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Suggested Questions
              </p>
              <div className="flex flex-wrap justify-center gap-2">
                {exampleQuestions.map((q, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => handleSend(q)}
                    className="text-left px-3.5 py-2 bg-white border border-gray-200 text-gray-700 text-xs sm:text-sm rounded-xl hover:border-[#2c7a7b] hover:text-[#2c7a7b] hover:bg-[#e6fffa]/30 transition-all shadow-2xs"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              message={msg}
              onSelectSuggestion={(q) => handleSend(q)}
            />
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 flex items-center space-x-2">
              <div className="w-2 h-2 bg-[#2c7a7b] rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-[#2c7a7b] rounded-full animate-bounce delay-75" />
              <div className="w-2 h-2 bg-[#2c7a7b] rounded-full animate-bounce delay-150" />
              <span className="text-xs text-gray-500 ml-1">Analyzing statutory sources & evidence...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 sm:p-4 bg-white border-t border-gray-200 shrink-0">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend(input);
          }}
          className="relative flex items-end border border-gray-300 rounded-xl overflow-hidden shadow-2xs focus-within:ring-2 focus-within:ring-[#2c7a7b] focus-within:border-transparent transition-all bg-white"
        >
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend(input);
              }
            }}
            placeholder={`Ask an Ayurvedic IPR, TK, ABS or regulatory question for ${jurisdiction}...`}
            className="w-full max-h-32 p-3 pb-3 pr-12 resize-none outline-hidden text-xs sm:text-sm text-gray-800"
            rows={2}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2.5 bottom-2.5 p-2 bg-[#1a365d] text-white rounded-lg disabled:opacity-40 disabled:bg-gray-300 hover:bg-[#0f2342] transition-colors"
            title="Send Query"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="flex items-center justify-center gap-1.5 text-[11px] text-gray-400 mt-2 text-center">
          <AlertCircle className="w-3 h-3 shrink-0" />
          <span>This information is for informational purposes only and does not constitute legal advice.</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
