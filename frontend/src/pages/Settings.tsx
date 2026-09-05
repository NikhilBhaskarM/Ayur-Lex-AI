import React, { useState } from 'react';
import { Settings as SettingsIcon, Globe, Shield, User, Bell, Check, LogOut } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';

const Settings: React.FC = () => {
  const { user, jurisdiction, setJurisdiction, logout } = useAuthStore();
  const [language, setLanguage] = useState(user?.preferred_language || 'en');
  const [aiProvider, setAiProvider] = useState('ollama');

  const handleSave = () => {
    toast.success('Settings updated successfully');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gray-100 rounded-xl">
            <SettingsIcon className="w-6 h-6 text-[#1a365d]" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-[#1a365d]">Platform Settings</h1>
            <p className="text-xs sm:text-sm text-gray-500 mt-0.5">
              Manage your language, jurisdiction preferences, and AI assistant configurations.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-6">
        {/* User Profile */}
        <div>
          <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2 flex items-center gap-2">
            <User className="w-4 h-4 text-[#2c7a7b]" />
            <span>User Account</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3 text-xs sm:text-sm">
            <div>
              <span className="text-gray-500 block text-xs">Full Name</span>
              <span className="font-semibold text-gray-900">{user?.full_name || 'Practitioner'}</span>
            </div>
            <div>
              <span className="text-gray-500 block text-xs">Email Address</span>
              <span className="font-semibold text-gray-900">{user?.email || 'user@ayurveda.org'}</span>
            </div>
            <div>
              <span className="text-gray-500 block text-xs">Account Role</span>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-blue-50 text-blue-800">
                {user?.role || 'USER'}
              </span>
            </div>
          </div>
        </div>

        {/* Jurisdiction Preference */}
        <div>
          <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2 flex items-center gap-2">
            <Globe className="w-4 h-4 text-[#2c7a7b]" />
            <span>Default Legal Jurisdiction</span>
          </h2>
          <div className="grid grid-cols-2 gap-3 mt-3">
            <button
              type="button"
              onClick={() => setJurisdiction('India')}
              className={`p-3 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                jurisdiction === 'India'
                  ? 'border-orange-500 bg-orange-50/50 text-orange-900 ring-1 ring-orange-500'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="font-bold">🇮🇳 India (Domestic Law)</div>
              <div className="text-xs text-gray-500 mt-0.5">Patents Act, D&C Act, BD Act 2002/2023, FSSAI</div>
            </button>
            <button
              type="button"
              onClick={() => setJurisdiction('International')}
              className={`p-3 border rounded-xl text-left text-xs sm:text-sm font-medium transition-all ${
                jurisdiction === 'International'
                  ? 'border-blue-500 bg-blue-50/50 text-blue-900 ring-1 ring-blue-500'
                  : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <div className="font-bold">🌍 International Framework</div>
              <div className="text-xs text-gray-500 mt-0.5">PCT, WIPO GRATK Treaty, Nagoya Protocol, EU THMPD</div>
            </button>
          </div>
        </div>

        {/* Language Preference */}
        <div>
          <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2 flex items-center gap-2">
            <Shield className="w-4 h-4 text-[#2c7a7b]" />
            <span>Preferred Language</span>
          </h2>
          <div className="grid grid-cols-3 gap-3 mt-3">
            {[
              { code: 'en', label: 'English', desc: 'Default Interface' },
              { code: 'hi', label: 'हिन्दी (Hindi)', desc: 'आयुर्वेद पारिभाषिक' },
              { code: 'kn', label: 'ಕನ್ನಡ (Kannada)', desc: 'ಪ್ರಾದೇಶಿಕ ಭಾಷೆ' },
            ].map((lang) => (
              <button
                key={lang.code}
                type="button"
                onClick={() => setLanguage(lang.code)}
                className={`p-3 border rounded-xl text-left text-xs font-medium transition-all ${
                  language === lang.code
                    ? 'border-[#2c7a7b] bg-[#e6fffa]/40 text-[#2c7a7b] ring-1 ring-[#2c7a7b]'
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                <div className="font-bold">{lang.label}</div>
                <div className="text-[11px] text-gray-500 mt-0.5">{lang.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* AI Provider Configuration */}
        <div>
          <h2 className="text-sm font-bold text-gray-900 border-b border-gray-100 pb-2 flex items-center gap-2">
            <Bell className="w-4 h-4 text-[#2c7a7b]" />
            <span>LLM Backend Provider Mode</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-3 text-xs">
            <button
              type="button"
              onClick={() => setAiProvider('ollama')}
              className={`p-3 border rounded-xl text-left ${
                aiProvider === 'ollama' ? 'border-[#1a365d] bg-gray-50 ring-1 ring-[#1a365d]' : 'border-gray-200'
              }`}
            >
              <div className="font-bold text-gray-900">Ollama (Local Private)</div>
              <div className="text-gray-500 mt-0.5">qwen2.5:7b / mistral (Zero data leakage)</div>
            </button>
            <button
              type="button"
              onClick={() => setAiProvider('openai')}
              className={`p-3 border rounded-xl text-left ${
                aiProvider === 'openai' ? 'border-[#1a365d] bg-gray-50 ring-1 ring-[#1a365d]' : 'border-gray-200'
              }`}
            >
              <div className="font-bold text-gray-900">OpenAI API (Cloud)</div>
              <div className="text-gray-500 mt-0.5">gpt-4o / text-embedding-3-small</div>
            </button>
            <button
              type="button"
              onClick={() => setAiProvider('lmstudio')}
              className={`p-3 border rounded-xl text-left ${
                aiProvider === 'lmstudio' ? 'border-[#1a365d] bg-gray-50 ring-1 ring-[#1a365d]' : 'border-gray-200'
              }`}
            >
              <div className="font-bold text-gray-900">LM Studio (Local)</div>
              <div className="text-gray-500 mt-0.5">Localhost:1234 inference</div>
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between pt-4 border-t border-gray-100">
          <button
            type="button"
            onClick={logout}
            className="flex items-center gap-1.5 px-4 py-2 border border-red-200 text-red-700 rounded-lg text-xs font-semibold hover:bg-red-50 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
          <button
            type="button"
            onClick={handleSave}
            className="flex items-center gap-1.5 px-6 py-2.5 bg-[#1a365d] text-white rounded-lg text-xs font-bold hover:bg-[#0f2342] transition-colors shadow-2xs"
          >
            <Check className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
