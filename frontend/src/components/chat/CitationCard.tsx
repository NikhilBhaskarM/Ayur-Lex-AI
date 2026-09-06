import React, { useState } from 'react';
import { ExternalLink, ChevronDown, ChevronUp, BookOpen, ShieldCheck } from 'lucide-react';
import type { Citation } from '@/types';

interface CitationCardProps {
  citation: Citation;
  index: number;
}

const CitationCard: React.FC<CitationCardProps> = ({ citation, index }) => {
  const [expanded, setExpanded] = useState(false);

  const title = citation.source_title || 'Authoritative Source';
  const authority = citation.authority;
  const sectionInfo = [citation.section, citation.rule, citation.article].filter(Boolean).join(' • ');
  const url = citation.official_url;
  const passage = citation.relevant_passage;

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-2xs hover:border-[#2c7a7b]/50 transition-colors">
      <div
        className="px-3.5 py-2.5 flex items-center justify-between cursor-pointer hover:bg-gray-50/80 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center space-x-2.5 min-w-0 pr-2">
          <span className="shrink-0 flex items-center justify-center w-5 h-5 rounded-full bg-[#1a365d]/10 text-[#1a365d] text-xs font-bold">
            [{index}]
          </span>
          <div className="min-w-0">
            <p className="text-xs sm:text-sm font-semibold text-gray-800 truncate">
              {title}
              {sectionInfo && <span className="font-normal text-gray-500 ml-1.5 text-xs">({sectionInfo})</span>}
            </p>
            {authority && (
              <p className="text-[11px] text-gray-500 flex items-center gap-1 mt-0.5">
                <ShieldCheck className="w-3 h-3 text-[#2c7a7b]" />
                <span className="truncate">{authority}</span>
                {citation.version_date && <span className="text-gray-400">• v.{citation.version_date}</span>}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-1.5 shrink-0">
          {url && (
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="p-1 text-gray-400 hover:text-[#2c7a7b] hover:bg-gray-100 rounded transition-colors"
              title="Open Official Government / Treaty Source"
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
          <button
            type="button"
            className="p-1 text-gray-400 hover:text-gray-600 rounded"
            aria-label="Toggle excerpt"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {expanded && (
        <div className="px-3.5 py-2.5 bg-gray-50 border-t border-gray-100 text-xs text-gray-700">
          {passage ? (
            <div className="flex items-start">
              <BookOpen className="w-3.5 h-3.5 mr-2 mt-0.5 text-gray-400 shrink-0" />
              <p className="italic leading-relaxed font-serif">"{passage}"</p>
            </div>
          ) : (
            <p className="text-gray-400 italic">No direct excerpt text available for this citation.</p>
          )}
          {url && (
            <div className="mt-2 pt-2 border-t border-gray-200/60 flex justify-end">
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-[11px] text-[#2c7a7b] hover:underline flex items-center gap-1 font-medium"
              >
                <span>Verify at Official Portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CitationCard;
