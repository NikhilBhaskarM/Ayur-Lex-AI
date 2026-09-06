import React from 'react';
import { Globe, MapPin } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const JurisdictionSelector: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);
  const setJurisdiction = useAuthStore((s) => s.setJurisdiction);

  const isNational = (jurisdiction || '').toLowerCase() === 'india' || (jurisdiction || '').toLowerCase() === 'national';
  const isInternational = (jurisdiction || '').toLowerCase() === 'international';

  return (
    <div className="flex items-center bg-slate-100/90 rounded-lg p-1 border border-slate-200/80 shadow-2xs">
      <button
        type="button"
        onClick={() => setJurisdiction('India')}
        title="National Track: Indian Patents Act 1970 §3(p)/§3(e), BDA 2002 §6, Drugs & Cosmetics Act"
        className={`flex items-center px-3 py-1.5 text-xs sm:text-sm font-medium rounded-md transition-all ${
          isNational
            ? 'bg-white text-orange-950 shadow-xs ring-1 ring-orange-200/80 font-bold'
            : 'text-slate-500 hover:text-slate-900'
        }`}
      >
        <MapPin className="w-3.5 h-3.5 mr-1.5 text-orange-600" />
        <span>India 🇮🇳</span>
      </button>
      <button
        type="button"
        onClick={() => setJurisdiction('International')}
        title="International Track: WIPO GRATK Treaty 2024, CBD/Nagoya ABS, US FDA Botanical Guidance, EMA Monograph"
        className={`flex items-center px-3 py-1.5 text-xs sm:text-sm font-medium rounded-md transition-all ${
          isInternational
            ? 'bg-white text-teal-950 shadow-xs ring-1 ring-teal-200/80 font-bold'
            : 'text-slate-500 hover:text-slate-900'
        }`}
      >
        <Globe className="w-3.5 h-3.5 mr-1.5 text-teal-600" />
        <span>International 🌍</span>
      </button>
    </div>
  );
};

export default JurisdictionSelector;
