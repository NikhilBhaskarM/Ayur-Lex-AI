import React, { useState } from 'react';
import { Settings as SettingsIcon, Globe, Shield, User, Bell, Check, LogOut, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/api/auth';
import { useTranslation } from 'react-i18next';

const Settings: React.FC = () => {
  const { 
    user, 
    jurisdiction, 
    setJurisdiction, 
    setLanguage: setStoreLanguage, 
    updateUser, 
    logout,
    llmProvider: storeLlmProvider,
    llmModel: storeLlmModel,
    llmApiKey: storeLlmApiKey,
    llmBaseUrl: storeLlmBaseUrl,
    setLLMConfig,
  } = useAuthStore();
  const { i18n } = useTranslation();
  const [language, setLanguage] = useState(user?.preferred_language || 'en');
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [aiProvider, setAiProvider] = useState(storeLlmProvider || 'ollama');
  const [modelName, setModelName] = useState(storeLlmModel || 'llama3.1:8b');
  const [apiKey, setApiKey] = useState(storeLlmApiKey || '');
  const [baseUrl, setBaseUrl] = useState(storeLlmBaseUrl || '');
  const [isSaving, setIsSaving] = useState(false);

  const handleProviderSelect = (prov: string) => {
    setAiProvider(prov);
    if (prov === 'ollama') {
      setModelName('llama3.1:8b');
      setBaseUrl('http://localhost:11434/v1');
    } else if (prov === 'openai') {
      setModelName('gpt-4o');
      setBaseUrl('https://api.openai.com/v1');
    } else if (prov === 'lmstudio') {
      setModelName('local-model');
      setBaseUrl('http://localhost:1234/v1');
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // 1. Update backend profile if authenticated
      if (user) {
        const updated = await authApi.updateProfile({
          full_name: fullName.trim() || user.full_name,
          preferred_language: language,
        });
        updateUser(updated);
      }

      // 2. Sync client-side stores and i18n
      setStoreLanguage(language);
      i18n.changeLanguage(language);

      // 3. Persist LLM configuration
      setLLMConfig({
        provider: aiProvider,
        model: modelName,
        apiKey: apiKey,
        baseUrl: baseUrl,
      });

      toast.success('All settings & LLM configuration updated successfully');
    } catch (err: any) {
      console.warn('Backend update error, saving locally:', err);
      setStoreLanguage(language);
      i18n.changeLanguage(language);
      if (fullName.trim() && user) {
        updateUser({ full_name: fullName.trim(), preferred_language: language });
      }
      setLLMConfig({
        provider: aiProvider,
        model: modelName,
        apiKey: apiKey,
        baseUrl: baseUrl,
      });
      toast.success('Preferences updated in current session');
    } finally {
      setIsSaving(false);
    }
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
            <span>User Account & Identity</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-3 text-xs sm:text-sm">
            <div>
              <label className="text-gray-500 block text-xs mb-1 font-medium">Full Name</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Dr. Ayurvedic Practitioner"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs sm:text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              />
            </div>
            <div>
              <span className="text-gray-500 block text-xs mb-1 font-medium">Email Address</span>
              <div className="px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg font-semibold text-gray-700 text-xs sm:text-sm">
                {user?.email || 'user@ayurveda.org'}
              </div>
            </div>
            <div>
              <span className="text-gray-500 block text-xs mb-1 font-medium">Account Role</span>
              <div className="mt-1">
                <span className="inline-flex items-center px-2.5 py-1 rounded text-xs font-bold bg-blue-50 text-blue-800 border border-blue-200">
                  {user?.role || 'USER'}
                </span>
              </div>
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
              onClick={() => handleProviderSelect('ollama')}
              className={`p-3.5 border rounded-xl text-left transition-all ${
                aiProvider === 'ollama'
                  ? 'border-[#2c7a7b] bg-[#e6fffa]/30 ring-1 ring-[#2c7a7b] text-slate-900 font-medium'
                  : 'border-gray-200 hover:bg-gray-50 text-gray-700'
              }`}
            >
              <div className="font-bold text-sm">🦙 Ollama (Local Private)</div>
              <div className="text-gray-500 mt-1 text-[11px]">Zero cloud data leakage. Best for secret formulations.</div>
              <div className="mt-2 text-[10px] text-emerald-700 font-mono bg-emerald-50 px-1.5 py-0.5 rounded w-fit">
                http://localhost:11434
              </div>
            </button>
            <button
              type="button"
              onClick={() => handleProviderSelect('openai')}
              className={`p-3.5 border rounded-xl text-left transition-all ${
                aiProvider === 'openai'
                  ? 'border-[#2c7a7b] bg-[#e6fffa]/30 ring-1 ring-[#2c7a7b] text-slate-900 font-medium'
                  : 'border-gray-200 hover:bg-gray-50 text-gray-700'
              }`}
            >
              <div className="font-bold text-sm">⚡ OpenAI API (Cloud)</div>
              <div className="text-gray-500 mt-1 text-[11px]">Fast reasoning with GPT-4o / GPT-4o-mini.</div>
              <div className="mt-2 text-[10px] text-blue-700 font-mono bg-blue-50 px-1.5 py-0.5 rounded w-fit">
                https://api.openai.com
              </div>
            </button>
            <button
              type="button"
              onClick={() => handleProviderSelect('lmstudio')}
              className={`p-3.5 border rounded-xl text-left transition-all ${
                aiProvider === 'lmstudio'
                  ? 'border-[#2c7a7b] bg-[#e6fffa]/30 ring-1 ring-[#2c7a7b] text-slate-900 font-medium'
                  : 'border-gray-200 hover:bg-gray-50 text-gray-700'
              }`}
            >
              <div className="font-bold text-sm">🖥️ LM Studio / Local GGUF</div>
              <div className="text-gray-500 mt-1 text-[11px]">Localhost inference server with custom models.</div>
              <div className="mt-2 text-[10px] text-purple-700 font-mono bg-purple-50 px-1.5 py-0.5 rounded w-fit">
                http://localhost:1234
              </div>
            </button>
          </div>

          {/* Detailed LLM Parameters for Selected Provider */}
          <div className="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-xl space-y-3.5 text-xs">
            <div className="flex items-center justify-between">
              <span className="font-bold text-gray-800">
                Configure Active Model ({aiProvider.toUpperCase()})
              </span>
              <span className="text-[11px] text-gray-500">
                Applied dynamically to all statutory RAG queries
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-gray-600 block text-xs mb-1 font-medium">Model Name / Tag</label>
                {aiProvider === 'ollama' ? (
                  <div className="space-y-1.5">
                    <select
                      value={['llama3.1:8b', 'qwen2.5:7b', 'mistral:7b', 'gemma2:9b'].includes(modelName) ? modelName : 'custom'}
                      onChange={(e) => {
                        if (e.target.value !== 'custom') {
                          setModelName(e.target.value);
                        }
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs bg-white text-gray-800 outline-hidden focus:ring-2 focus:ring-[#2c7a7b]"
                    >
                      <option value="llama3.1:8b">llama3.1:8b (Meta LLaMA 3.1 - Recommended)</option>
                      <option value="qwen2.5:7b">qwen2.5:7b (Alibaba Qwen 2.5 - Strong Multilingual)</option>
                      <option value="mistral:7b">mistral:7b (Mistral AI)</option>
                      <option value="gemma2:9b">gemma2:9b (Google Gemma 2)</option>
                      <option value="custom">Custom Tag / Pull</option>
                    </select>
                    <input
                      type="text"
                      value={modelName}
                      onChange={(e) => setModelName(e.target.value)}
                      placeholder="e.g. llama3.1:8b, deepseek-r1:8b"
                      className="w-full px-3 py-1.5 border border-gray-300 rounded-lg text-xs font-mono bg-white text-gray-800 outline-hidden"
                    />
                  </div>
                ) : aiProvider === 'openai' ? (
                  <div className="space-y-1.5">
                    <select
                      value={['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'].includes(modelName) ? modelName : 'custom'}
                      onChange={(e) => {
                        if (e.target.value !== 'custom') {
                          setModelName(e.target.value);
                        }
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs bg-white text-gray-800 outline-hidden focus:ring-2 focus:ring-[#2c7a7b]"
                    >
                      <option value="gpt-4o">gpt-4o (Most Intelligent)</option>
                      <option value="gpt-4o-mini">gpt-4o-mini (Fast & Cost-Effective)</option>
                      <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                      <option value="custom">Custom Model Name</option>
                    </select>
                    <input
                      type="text"
                      value={modelName}
                      onChange={(e) => setModelName(e.target.value)}
                      placeholder="e.g. gpt-4o, gpt-4-turbo"
                      className="w-full px-3 py-1.5 border border-gray-300 rounded-lg text-xs font-mono bg-white text-gray-800 outline-hidden"
                    />
                  </div>
                ) : (
                  <input
                    type="text"
                    value={modelName}
                    onChange={(e) => setModelName(e.target.value)}
                    placeholder="e.g. local-model or huggingface/repo"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs font-mono bg-white text-gray-800 outline-hidden"
                  />
                )}
              </div>

              <div>
                <label className="text-gray-600 block text-xs mb-1 font-medium">Base URL / Endpoint</label>
                <input
                  type="text"
                  value={baseUrl}
                  onChange={(e) => setBaseUrl(e.target.value)}
                  placeholder={
                    aiProvider === 'ollama'
                      ? 'http://localhost:11434/v1'
                      : aiProvider === 'openai'
                      ? 'https://api.openai.com/v1'
                      : 'http://localhost:1234/v1'
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs font-mono bg-white text-gray-800 outline-hidden"
                />
              </div>
            </div>

            {aiProvider === 'openai' && (
              <div>
                <label className="text-gray-600 block text-xs mb-1 font-medium">OpenAI API Key</label>
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-xs font-mono bg-white text-gray-800 outline-hidden"
                />
                <p className="text-[11px] text-gray-500 mt-1">
                  Your key is sent over HTTPS directly in the authorization header and is never logged in plaintext.
                </p>
              </div>
            )}
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
            disabled={isSaving}
            className="flex items-center gap-1.5 px-6 py-2.5 bg-[#1a365d] hover:bg-[#0f2342] text-white rounded-lg text-xs font-bold transition-colors shadow-2xs disabled:opacity-50"
          >
            {isSaving ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Saving...</span>
              </>
            ) : (
              <>
                <Check className="w-4 h-4" />
                <span>Save Preferences</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
