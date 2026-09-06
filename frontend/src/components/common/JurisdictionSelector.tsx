import React from 'react';
import { Globe, MapPin } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const JurisdictionSelector: React.FC = () => {
  const jurisdiction = useAuthStore((s) => s.jurisdiction);
  const setJurisdiction = useAuthStore((s) => s.setJurisdiction);

  return (
    <div className="flex items-center bg-gray-100 rounded-lg p-1 border border-gray-200 shadow-sm">
      <button
        type="button"
        onClick={() => setJurisdiction('India')}
        className={`flex items-center px-3 py-1.5 text-xs sm:text-sm font-medium rounded-md transition-all ${
          jurisdiction === 'India'
            ? 'bg-white text-[#1a365d] shadow-sm ring-1 ring-gray-200 font-semibold'
            : 'text-gray-500 hover:text-gray-900'
        }`}
      >
        <MapPin className="w-3.5 h-3.5 mr-1.5 text-[#d69e2e]" />
        India 🇮🇳
      </button>
      <button
        type="button"
        onClick={() => setJurisdiction('International')}
        className={`flex items-center px-3 py-1.5 text-xs sm:text-sm font-medium rounded-md transition-all ${
          jurisdiction === 'International'
            ? 'bg-white text-[#1a365d] shadow-sm ring-1 ring-gray-200 font-semibold'
            : 'text-gray-500 hover:text-gray-900'
        }`}
      >
        <Globe className="w-3.5 h-3.5 mr-1.5 text-[#2c7a7b]" />
        International 🌍
      </button>
    </div>
  );
};

export default JurisdictionSelector;
