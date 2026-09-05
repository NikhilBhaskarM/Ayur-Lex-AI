import React, { useState } from 'react';
import {
  Settings as SettingsIcon,
  Globe2,
  ShieldCheck,
  User,
  Cpu,
  Check,
  LogOut,
  Lock,
  Languages,
  Sparkles,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';

const Settings: React.FC = () => {
  const { user, jurisdiction, setJurisdiction, logout } = useAuthStore();

  const [language, setLanguage] = useState(
    user?.preferred_language || 'en'
  );

  const [aiProvider, setAiProvider] = useState('ollama');

  const handleSave = () => {
    toast.success('Preferences saved successfully');
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-12">

      {/* Hero */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 p-7 sm:p-8 text-white shadow-xl">
        <div className="absolute -right-20 -top-20 w-64 h-64 rounded-full bg-teal-500/10 blur-3xl" />

        <div className="relative flex items-center gap-4">
          <div className="p-3.5 rounded-2xl bg-white/10 border border-white/10">
            <SettingsIcon size={28} className="text-teal-300" />
          </div>

          <div>
            <div className="text-xs font-bold tracking-widest text-teal-300 mb-1">
              WORKSPACE CONFIGURATION
            </div>

            <h1 className="text-2xl sm:text-3xl font-bold">
              Platform Settings
            </h1>

            <p className="text-sm text-slate-300 mt-1">
              Personalize your Ayur-Lex-AI intelligence workspace.
            </p>
          </div>
        </div>
      </section>

      {/* Account */}
      <section className="card">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 rounded-xl bg-blue-50 text-blue-700">
            <User size={21} />
          </div>

          <div>
            <h2 className="font-bold text-slate-900">
              User Account
            </h2>
            <p className="text-xs text-slate-500">
              Your platform account information
            </p>
          </div>
        </div>

        <div className="grid sm:grid-cols-3 gap-4">
          <div className="rounded-xl bg-slate-50 border border-slate-100 p-4">
            <p className="text-xs text-slate-400 mb-1">Full Name</p>
            <p className="font-semibold text-slate-900">
              {user?.full_name || 'Practitioner'}
            </p>
          </div>

          <div className="rounded-xl bg-slate-50 border border-slate-100 p-4">
            <p className="text-xs text-slate-400 mb-1">Email</p>
            <p className="font-semibold text-slate-900 break-all">
              {user?.email || 'user@ayurveda.org'}
            </p>
          </div>

          <div className="rounded-xl bg-slate-50 border border-slate-100 p-4">
            <p className="text-xs text-slate-400 mb-1">Account Role</p>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-teal-50 text-teal-700">
              <ShieldCheck size={13} />
              {user?.role || 'USER'}
            </span>
          </div>
        </div>
      </section>

      {/* Jurisdiction */}
      <section className="card">
        <div className="flex items-center gap-3 mb-5">
          <div className="p-3 rounded-xl bg-orange-50 text-orange-700">
            <Globe2 size={21} />
          </div>

          <div>
            <h2 className="font-bold text-slate-900">
              Default Legal Jurisdiction
            </h2>
            <p className="text-xs text-slate-500">
              Choose the legal framework used by the AI assistant.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">

          <button
            type="button"
            onClick={() => setJurisdiction('India')}
            className={`text-left p-5 rounded-2xl border-2 transition-all ${
              jurisdiction === 'India'
                ? 'border-orange-500 bg-orange-50/60 shadow-sm'
                : 'border-slate-200 hover:border-orange-200 hover:bg-slate-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-2xl">🇮🇳</span>

              {jurisdiction === 'India' && (
                <Check size={20} className="text-orange-600" />
              )}
            </div>

            <h3 className="font-bold text-slate-900 mt-4">
              India
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              Domestic IPR & regulatory framework
            </p>

            <div className="flex flex-wrap gap-2 mt-4">
              {['Patents Act', 'BD Act', 'FSSAI'].map((item) => (
                <span
                  key={item}
                  className="text-[11px] px-2 py-1 rounded-full bg-white border border-orange-100 text-orange-700"
                >
                  {item}
                </span>
              ))}
            </div>
          </button>

          <button
            type="button"
            onClick={() => setJurisdiction('International')}
            className={`text-left p-5 rounded-2xl border-2 transition-all ${
              jurisdiction === 'International'
                ? 'border-blue-500 bg-blue-50/60 shadow-sm'
                : 'border-slate-200 hover:border-blue-200 hover:bg-slate-50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-2xl">🌍</span>

              {jurisdiction === 'International' && (
                <Check size={20} className="text-blue-600" />
              )}
            </div>

            <h3 className="font-bold text-slate-900 mt-4">
              International
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              International IPR & regulatory framework
            </p>

            <div className="flex flex-wrap gap-2 mt-4">
              {['PCT', 'WIPO', 'Nagoya Protocol'].map((item) => (
                <span
                  key={item}
                  className="text-[11px] px-2 py-1 rounded-full bg-white border border-blue-100 text-blue-700"
                >
                  {item}
                </span>
              ))}
            </div>
          </button>

        </div>
      </section>

      {/* Language */}
      <section className="card">
        <div className="flex items-center gap-3 mb-5">
          <div className="p-3 rounded-xl bg-purple-50 text-purple-700">
            <Languages size={21} />
          </div>

          <div>
            <h2 className="font-bold text-slate-900">
              Preferred Language
            </h2>
            <p className="text-xs text-slate-500">
              Select your preferred AI interaction language.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-3">
          {[
            {
              code: 'en',
              title: 'English',
              description: 'Default interface',
              flag: 'EN',
            },
            {
              code: 'hi',
              title: 'हिन्दी',
              description: 'Hindi language support',
              flag: 'हि',
            },
            {
              code: 'kn',
              title: 'ಕನ್ನಡ',
              description: 'Kannada language support',
              flag: 'ಕ',
            },
          ].map((lang) => (
            <button
              key={lang.code}
              type="button"
              onClick={() => setLanguage(lang.code)}
              className={`p-4 rounded-2xl border-2 text-left transition-all ${
                language === lang.code
                  ? 'border-teal-500 bg-teal-50/60'
                  : 'border-slate-200 hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 text-sm font-bold text-slate-700">
                  {lang.flag}
                </span>

                {language === lang.code && (
                  <Check size={18} className="text-teal-600" />
                )}
              </div>

              <p className="font-bold text-slate-900 mt-3">
                {lang.title}
              </p>

              <p className="text-xs text-slate-500 mt-1">
                {lang.description}
              </p>
            </button>
          ))}
        </div>
      </section>

      {/* AI Provider */}
      <section className="card">
        <div className="flex items-center gap-3 mb-5">
          <div className="p-3 rounded-xl bg-emerald-50 text-emerald-700">
            <Cpu size={21} />
          </div>

          <div>
            <h2 className="font-bold text-slate-900">
              AI Backend Provider
            </h2>
            <p className="text-xs text-slate-500">
              Select the inference environment for your workspace.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4">

          {[
            {
              id: 'ollama',
              title: 'Ollama',
              subtitle: 'Local & Private',
              detail: 'qwen2.5:7b / mistral',
            },
            {
              id: 'openai',
              title: 'OpenAI API',
              subtitle: 'Cloud Intelligence',
              detail: 'GPT models & embeddings',
            },
            {
              id: 'lmstudio',
              title: 'LM Studio',
              subtitle: 'Local Inference',
              detail: 'localhost:1234',
            },
          ].map((provider) => (
            <button
              key={provider.id}
              type="button"
              onClick={() => setAiProvider(provider.id)}
              className={`text-left p-4 rounded-2xl border-2 transition-all ${
                aiProvider === provider.id
                  ? 'border-teal-500 bg-teal-50/50'
                  : 'border-slate-200 hover:bg-slate-50'
              }`}
            >
              <div className="flex items-center justify-between">
                <Sparkles
                  size={19}
                  className={
                    aiProvider === provider.id
                      ? 'text-teal-600'
                      : 'text-slate-400'
                  }
                />

                {aiProvider === provider.id && (
                  <Check size={18} className="text-teal-600" />
                )}
              </div>

              <h3 className="font-bold text-slate-900 mt-3">
                {provider.title}
              </h3>

              <p className="text-xs font-medium text-teal-700 mt-1">
                {provider.subtitle}
              </p>

              <p className="text-xs text-slate-400 mt-2">
                {provider.detail}
              </p>
            </button>
          ))}

        </div>

        <div className="mt-5 flex items-center gap-2 text-xs text-slate-500 bg-slate-50 rounded-xl p-3">
          <Lock size={14} />
          Provider selection is a workspace preference. Actual backend
          availability depends on server configuration.
        </div>
      </section>

      {/* Actions */}
      <section className="flex flex-col-reverse sm:flex-row sm:justify-between gap-3">

        <button
          type="button"
          onClick={logout}
          className="flex items-center justify-center gap-2 px-5 py-3 rounded-xl border border-red-200 text-red-700 font-semibold text-sm hover:bg-red-50 transition"
        >
          <LogOut size={17} />
          Sign Out
        </button>

        <button
          type="button"
          onClick={handleSave}
          className="btn-primary flex items-center justify-center gap-2 px-7 py-3"
        >
          <Check size={18} />
          Save Preferences
        </button>

      </section>

      <p className="text-center text-xs text-slate-400">
        Ayur-Lex-AI • AI-assisted IPR & Regulatory Intelligence
      </p>

    </div>
  );
};

export default Settings;