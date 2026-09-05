import React, { useState } from 'react';
import {
  Send,
  MapPin,
  AlertCircle,
  RefreshCw,
  Sparkles,
  ShieldCheck,
  BookOpen,
  Scale,
  ChevronRight,
  Bot,
  User,
} from 'lucide-react';
import toast from 'react-hot-toast';

import MessageBubble from './MessageBubble';
import LegalChamberPanel from '../LegalChamberPanel';
import { useAuthStore } from '../../store/authStore';
import { chatApi } from '../../api/chat';
import type { ChatMessage } from '../../types';

const exampleQuestions = [
  {
    icon: Scale,
    title: 'Patent protection',
    question: 'Can I patent my Ayurvedic formulation?',
  },
  {
    icon: ShieldCheck,
    title: 'Product permissions',
    question: 'What permissions are required for an Ayurvedic product?',
  },
  {
    icon: BookOpen,
    title: 'Traditional knowledge',
    question: 'Is this formulation traditional knowledge?',
  },
  {
    icon: ShieldCheck,
    title: 'Biodiversity compliance',
    question: 'Do I need biodiversity approval under the BD Act?',
  },
  {
    icon: ChevronRight,
    title: 'International export',
    question: 'Can I export this Ayurvedic product to Europe?',
  },
  {
    icon: BookOpen,
    title: 'Trademark protection',
    question: 'Can I register this Ayurvedic brand as a trademark?',
  },
];

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [activeDebateQuery, setActiveDebateQuery] = useState<string | null>(null);

  const { jurisdiction } = useAuthStore();

  const handleSend = async (question?: string) => {
    const messageText = (question ?? input).trim();

    if (!messageText || isLoading) return;

    setInput('');

    const userMessage: ChatMessage = {
      role: 'user',
      content: messageText,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chatApi.sendMessage({
        message: messageText,
        conversation_id: conversationId,
        jurisdiction,
      });

      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
        confidence: response.confidence,
        jurisdiction: response.jurisdiction,
        clarification_questions: response.clarification_questions,
        disclaimer: response.disclaimer,
        tier: response.tier,
        model_name: response.model_name,
        statutory_risk: response.statutory_risk,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (response.tier === 'debate') {
        setActiveDebateQuery(messageText);
      }
    } catch (err: any) {
      console.error(err);

      const errorMessage: ChatMessage = {
        role: 'assistant',
        content:
          err?.response?.data?.detail ||
          err?.message ||
          'Unable to process your request. Please try again.',
      };

      setMessages((prev) => [...prev, errorMessage]);

      toast.error('Unable to get an AI response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setConversationId(undefined);
    setInput('');
    setActiveDebateQuery(null);
  };

  return (
    <div className="flex h-full min-h-[calc(100vh-140px)] w-full flex-col lg:flex-row gap-4">
      {/* Chat Pane */}
      <div
        className={`flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-all duration-300 ${
          activeDebateQuery ? 'w-full lg:w-1/2' : 'w-full'
        }`}
      >
      {/* Header */}
      <div className="border-b border-slate-200 bg-white px-5 py-4 sm:px-7">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-teal-600 to-emerald-600 text-white shadow-sm">
              <Sparkles size={21} />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold text-slate-900">
                  AyurLegal AI
                </h1>

                <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-emerald-700">
                  AI Assistant
                </span>
              </div>

              <p className="text-xs text-slate-500">
                Evidence-backed IPR & regulatory intelligence
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 sm:flex">
              <MapPin size={14} className="text-teal-600" />
              <span className="text-xs font-medium text-slate-700">
                {jurisdiction || 'India'}
              </span>
            </div>

            <button
              onClick={handleReset}
              title="New conversation"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-500 transition hover:bg-slate-50 hover:text-teal-700"
            >
              <RefreshCw size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Chat body */}
      <div className="flex-1 overflow-y-auto bg-slate-50/70">
        {messages.length === 0 ? (
          <div className="mx-auto flex max-w-5xl flex-col px-5 py-10 sm:px-8 sm:py-14">
            {/* Welcome */}
            <div className="mx-auto max-w-2xl text-center">
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-teal-600 to-emerald-600 text-white shadow-lg shadow-teal-600/20">
                <Bot size={30} />
              </div>

              <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                How can I help protect your{' '}
                <span className="text-teal-700">Ayurvedic innovation?</span>
              </h2>

              <p className="mx-auto mt-3 max-w-xl text-sm leading-6 text-slate-500">
                Ask about patents, trademarks, traditional knowledge,
                biodiversity compliance, product regulations, or international
                requirements.
              </p>
            </div>

            {/* Trust strip */}
            <div className="mx-auto mt-8 flex max-w-3xl flex-wrap justify-center gap-2">
              <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-medium text-slate-600 shadow-sm">
                <ShieldCheck size={14} className="text-emerald-600" />
                Grounded in trusted sources
              </div>

              <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-medium text-slate-600 shadow-sm">
                <BookOpen size={14} className="text-teal-600" />
                Citation-backed answers
              </div>

              <div className="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-medium text-slate-600 shadow-sm">
                <Sparkles size={14} className="text-amber-500" />
                Multilingual intelligence
              </div>
            </div>

            {/* Suggested questions */}
            <div className="mt-10">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-semibold text-slate-900">
                    Explore the platform
                  </h3>
                  <p className="mt-1 text-xs text-slate-500">
                    Start with one of these common questions
                  </p>
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {exampleQuestions.map((item) => {
                  const Icon = item.icon;

                  return (
                    <button
                      key={item.question}
                      onClick={() => handleSend(item.question)}
                      className="group rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition duration-200 hover:-translate-y-0.5 hover:border-teal-300 hover:shadow-md"
                    >
                      <div className="mb-3 flex items-center justify-between">
                        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-50 text-teal-700 transition group-hover:bg-teal-600 group-hover:text-white">
                          <Icon size={17} />
                        </div>

                        <ChevronRight
                          size={16}
                          className="text-slate-300 transition group-hover:translate-x-1 group-hover:text-teal-600"
                        />
                      </div>

                      <p className="text-xs font-semibold text-teal-700">
                        {item.title}
                      </p>

                      <p className="mt-1 text-sm font-medium leading-5 text-slate-800">
                        {item.question}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          <div className="mx-auto max-w-4xl space-y-5 px-5 py-7 sm:px-8">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className="flex gap-3"
              >
                <div
                  className={`mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
                    message.role === 'user'
                      ? 'bg-slate-800 text-white'
                      : 'bg-teal-600 text-white'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User size={15} />
                  ) : (
                    <Bot size={15} />
                  )}
                </div>

                <div className="min-w-0 flex-1">
                  <div className="mb-1 text-xs font-semibold text-slate-500">
                    {message.role === 'user' ? 'You' : 'AyurLegal AI'}
                  </div>

                  <MessageBubble
                    message={message}
                    onLaunchDebate={(q) => setActiveDebateQuery(q || message.content)}
                  />
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3">
                <div className="mt-1 flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600 text-white">
                  <Bot size={15} />
                </div>

                <div className="rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2 w-2 animate-bounce rounded-full bg-teal-500" />
                    <span
                      className="h-2 w-2 animate-bounce rounded-full bg-teal-500"
                      style={{ animationDelay: '120ms' }}
                    />
                    <span
                      className="h-2 w-2 animate-bounce rounded-full bg-teal-500"
                      style={{ animationDelay: '240ms' }}
                    />
                    <span className="ml-2 text-xs text-slate-500">
                      Analyzing trusted sources...
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Composer */}
      <div className="border-t border-slate-200 bg-white p-4 sm:p-5">
        <div className="mx-auto max-w-4xl">
          <div className="relative rounded-xl border border-slate-300 bg-slate-50 transition focus-within:border-teal-500 focus-within:ring-2 focus-within:ring-teal-500/10">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              disabled={isLoading}
              rows={2}
              placeholder="Ask about Ayurvedic IPR, regulations, patents, trademarks..."
              className="w-full resize-none border-0 bg-transparent px-4 py-3 pr-14 text-sm text-slate-800 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed"
            />

            <button
              onClick={() => handleSend()}
              disabled={!input.trim() || isLoading}
              className="absolute bottom-3 right-3 flex h-9 w-9 items-center justify-center rounded-lg bg-teal-600 text-white shadow-sm transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <Send size={16} />
            </button>
          </div>

          <div className="mt-2 flex items-center justify-between gap-3">
            <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
              <AlertCircle size={12} />
              <span>
                AI-generated information should be verified with qualified
                professionals.
              </span>
            </div>

            <span className="hidden text-[11px] text-slate-400 sm:block">
              Enter to send · Shift + Enter for new line
            </span>
          </div>
        </div>
      </div>
    </div>

    {/* Legal Chamber Debate Pane (Mounted ONLY when activeDebateQuery is set) */}
    {activeDebateQuery && (
      <div className="flex w-full lg:w-1/2 flex-col rounded-2xl border border-slate-800 bg-slate-950 shadow-xl overflow-y-auto p-2 min-h-[600px] lg:min-h-0">
        <LegalChamberPanel
          query={activeDebateQuery}
          autoStart={true}
          isCompact={true}
          onClose={() => setActiveDebateQuery(null)}
        />
      </div>
    )}
  </div>
);
};

export default ChatInterface;