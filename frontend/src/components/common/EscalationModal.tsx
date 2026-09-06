import React, { useState } from 'react';
import SanitizedMarkdown from './SanitizedMarkdown';
import { 
  ShieldCheck, 
  Download, 
  Copy, 
  Check, 
  X, 
  FileText, 
  Scale, 
  AlertCircle,
  FileCode
} from 'lucide-react';

export interface EscalationDossierData {
  dossier_id: string;
  timestamp: string;
  jurisdiction: string;
  applicant_name: string;
  overall_risk_label: string;
  overall_risk_score: number;
  confidence_score: number;
  citations_count: number;
  dossier_markdown: string;
  [key: string]: any;
}

interface EscalationModalProps {
  isOpen: boolean;
  onClose: () => void;
  dossier: EscalationDossierData | null;
  isLoading?: boolean;
}

export const EscalationModal: React.FC<EscalationModalProps> = ({
  isOpen,
  onClose,
  dossier,
  isLoading = false
}) => {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'preview' | 'markdown' | 'json'>('preview');

  if (!isOpen) return null;

  const handleCopy = () => {
    if (!dossier) return;
    const textToCopy = activeTab === 'json' 
      ? JSON.stringify(dossier, null, 2) 
      : dossier.dossier_markdown;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadMarkdown = () => {
    if (!dossier) return;
    const blob = new Blob([dossier.dossier_markdown], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${dossier.dossier_id || 'attorney_dossier'}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDownloadJson = () => {
    if (!dossier) return;
    const blob = new Blob([JSON.stringify(dossier, null, 2)], { type: 'application/json;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${dossier.dossier_id || 'attorney_dossier'}.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getRiskBadgeColor = (label: string) => {
    switch (label?.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'MODERATE':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      default:
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-teal-950 p-5 text-white flex items-center justify-between border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-teal-500/20 rounded-xl border border-teal-500/30 text-teal-300">
              <Scale size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-bold">Attorney Escalation Dossier</h3>
                <span className="inline-flex items-center gap-1 text-[11px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-medium">
                  <ShieldCheck size={12} />
                  DPDP Act 2023 Redacted
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                Structured handover brief for Registered Patent Agents & Legal Counsel
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition"
          >
            <X size={20} />
          </button>
        </div>

        {/* Content Body */}
        {isLoading ? (
          <div className="p-12 flex flex-col items-center justify-center gap-3">
            <div className="w-10 h-10 border-4 border-teal-600 border-t-transparent rounded-full animate-spin" />
            <p className="text-sm font-semibold text-slate-700">Assembling Statutory Intelligence Dossier...</p>
            <p className="text-xs text-slate-500">Checking DPDP Act 2023 PII sanitization and formatting citations</p>
          </div>
        ) : !dossier ? (
          <div className="p-10 text-center text-slate-500">
            <AlertCircle size={32} className="mx-auto text-amber-500 mb-2" />
            <p className="font-semibold">Unable to generate dossier data</p>
          </div>
        ) : (
          <>
            {/* Metadata Bar */}
            <div className="bg-slate-50 border-b border-slate-200 px-6 py-3 flex flex-wrap items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-4 text-slate-600">
                <span><strong>ID:</strong> {dossier.dossier_id}</span>
                <span><strong>Jurisdiction:</strong> {dossier.jurisdiction?.toUpperCase()}</span>
                <span><strong>Authorities:</strong> {dossier.citations_count} verified</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-slate-500 font-medium">Statutory Risk:</span>
                <span className={`px-2.5 py-0.5 rounded-md font-bold text-xs border ${getRiskBadgeColor(dossier.overall_risk_label)}`}>
                  {dossier.overall_risk_label} ({dossier.overall_risk_score?.toFixed(1)}/100)
                </span>
              </div>
            </div>

            {/* Tab Navigation */}
            <div className="border-b border-slate-200 px-6 flex items-center gap-2 bg-white">
              <button
                type="button"
                onClick={() => setActiveTab('preview')}
                className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-bold border-b-2 transition ${
                  activeTab === 'preview'
                    ? 'border-teal-600 text-teal-800'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                <FileText size={14} />
                Rendered Brief
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('markdown')}
                className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-bold border-b-2 transition ${
                  activeTab === 'markdown'
                    ? 'border-teal-600 text-teal-800'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                <FileCode size={14} />
                Raw Markdown (.md)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('json')}
                className={`flex items-center gap-1.5 py-2.5 px-3 text-xs font-bold border-b-2 transition ${
                  activeTab === 'json'
                    ? 'border-teal-600 text-teal-800'
                    : 'border-transparent text-slate-500 hover:text-slate-800'
                }`}
              >
                <FileCode size={14} />
                Structured JSON
              </button>
            </div>

            {/* Main Scrollable View */}
            <div className="flex-1 overflow-y-auto p-6 bg-slate-50/50">
              {activeTab === 'preview' && (
                <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-xs prose prose-sm max-w-none text-slate-800 leading-relaxed">
                  <SanitizedMarkdown>{dossier.dossier_markdown}</SanitizedMarkdown>
                </div>
              )}

              {activeTab === 'markdown' && (
                <pre className="bg-slate-900 text-slate-100 p-4 rounded-xl text-xs font-mono whitespace-pre-wrap overflow-x-auto">
                  {dossier.dossier_markdown}
                </pre>
              )}

              {activeTab === 'json' && (
                <pre className="bg-slate-900 text-emerald-400 p-4 rounded-xl text-xs font-mono whitespace-pre-wrap overflow-x-auto">
                  {JSON.stringify(dossier, null, 2)}
                </pre>
              )}
            </div>

            {/* Footer Toolbar */}
            <div className="bg-white border-t border-slate-200 px-6 py-4 flex flex-wrap items-center justify-between gap-3">
              <div className="text-xs text-slate-500 flex items-center gap-1">
                <ShieldCheck size={14} className="text-emerald-600" />
                <span>Confidential — Prepared exclusively for Patent Agent Escalation</span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleCopy}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition"
                >
                  {copied ? <Check size={14} className="text-emerald-600" /> : <Copy size={14} />}
                  {copied ? 'Copied!' : 'Copy'}
                </button>

                <button
                  type="button"
                  onClick={handleDownloadMarkdown}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-teal-800 bg-teal-50 border border-teal-300 rounded-lg hover:bg-teal-100 transition"
                >
                  <Download size={14} />
                  Export .MD
                </button>

                <button
                  type="button"
                  onClick={handleDownloadJson}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-800 bg-slate-100 border border-slate-300 rounded-lg hover:bg-slate-200 transition"
                >
                  <Download size={14} />
                  Export JSON
                </button>

                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-1.5 text-xs font-bold text-white bg-slate-800 rounded-lg hover:bg-slate-900 transition"
                >
                  Done
                </button>
              </div>
            </div>
          </>
        )}

      </div>
    </div>
  );
};
export default EscalationModal;
