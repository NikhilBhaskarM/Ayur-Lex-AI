import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, UserCheck, Lock, User, AlertCircle, Sparkles, Scale, ArrowRight } from 'lucide-react';

export const LoginPage = () => {
  const [portalType, setPortalType] = useState('user'); // 'user' | 'admin'
  const [username, setUsername] = useState('ayur_user');
  const [password, setPassword] = useState('UserAyur@2026');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handlePortalSwitch = (type) => {
    setPortalType(type);
    setError(null);
    if (type === 'admin') {
      setUsername('admin');
      setPassword('AdminAyur@2026');
    } else {
      setUsername('ayur_user');
      setPassword('UserAyur@2026');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const result = await login(username, password);
      if (result.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/');
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-950 to-emerald-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 text-slate-100">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="mx-auto h-14 w-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 p-0.5 shadow-xl shadow-emerald-500/20 flex items-center justify-center">
          <div className="h-full w-full bg-slate-900 rounded-[14px] flex items-center justify-center">
            <Scale className="h-7 w-7 text-emerald-400" />
          </div>
        </div>
        <h2 className="mt-4 text-3xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-300 via-teal-200 to-amber-200 bg-clip-text text-transparent">
          Ayur-Lex-AI
        </h2>
        <p className="mt-1 text-sm text-slate-400 font-medium">
          Ayurvedic IPR & Statutory Regulatory Intelligence Platform
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-slate-900/80 backdrop-blur-xl py-8 px-6 shadow-2xl border border-slate-800/80 rounded-2xl sm:px-10 relative overflow-hidden">
          {/* Subtle glow accent */}
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

          {/* Dual-Portal Toggle: [User Login] vs [Administrator Login] */}
          <div className="mb-6">
            <div className="grid grid-cols-2 p-1 bg-slate-800/80 rounded-xl border border-slate-700/60">
              <button
                type="button"
                onClick={() => handlePortalSwitch('user')}
                className={`flex items-center justify-center gap-2 py-2.5 text-xs font-semibold rounded-lg transition-all ${
                  portalType === 'user'
                    ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <UserCheck className="h-4 w-4" />
                User Login
              </button>
              <button
                type="button"
                onClick={() => handlePortalSwitch('admin')}
                className={`flex items-center justify-center gap-2 py-2.5 text-xs font-semibold rounded-lg transition-all ${
                  portalType === 'admin'
                    ? 'bg-amber-600 text-white shadow-md shadow-amber-900/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <ShieldCheck className="h-4 w-4" />
                Administrator Login
              </button>
            </div>
            <p className="text-[11px] text-center mt-2 text-slate-400">
              {portalType === 'admin'
                ? 'Protected portal: Access system telemetry, metrics, and compliance oversight.'
                : 'Standard portal: Access statutory chat, triage, synergy tools, and NBA copilot.'}
            </p>
          </div>

          {error && (
            <div className="mb-5 rounded-xl bg-red-950/60 border border-red-800/50 p-3.5 text-xs text-red-300 flex items-start gap-2.5">
              <AlertCircle className="h-4 w-4 text-red-400 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Username / Identifier
              </label>
              <div className="relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <User className="h-4 w-4" />
                </div>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2.5 bg-slate-950/60 border border-slate-700/80 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                  placeholder="Enter username or email"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                Password
              </label>
              <div className="relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                  <Lock className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-2.5 bg-slate-950/60 border border-slate-700/80 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                  placeholder="••••••••••••"
                />
              </div>
            </div>

            {/* Seeded Quick-Fill Preset Helper */}
            <div className="rounded-xl border border-slate-700/60 bg-slate-800/40 p-3 text-[11px] text-slate-300">
              <div className="flex items-center justify-between font-semibold">
                <span className="flex items-center gap-1.5 text-emerald-400">
                  <Sparkles className="h-3.5 w-3.5" />
                  Pre-configured Demo Credentials:
                </span>
                <button
                  type="button"
                  onClick={() => {
                    if (portalType === 'admin') {
                      setUsername('admin');
                      setPassword('AdminAyur@2026');
                    } else {
                      setUsername('ayur_user');
                      setPassword('UserAyur@2026');
                    }
                  }}
                  className="text-xs text-teal-400 hover:text-teal-300 underline font-medium"
                >
                  Quick Fill
                </button>
              </div>
              <div className="mt-1 font-mono text-[10.5px] text-slate-400">
                {portalType === 'admin' ? (
                  <span>User: <strong className="text-slate-200">admin</strong> &bull; Pass: <strong className="text-slate-200">AdminAyur@2026</strong> (role: admin)</span>
                ) : (
                  <span>User: <strong className="text-slate-200">ayur_user</strong> &bull; Pass: <strong className="text-slate-200">UserAyur@2026</strong> (role: user)</span>
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl text-sm font-semibold text-white shadow-lg transition-all ${
                portalType === 'admin'
                  ? 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 shadow-amber-900/40'
                  : 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 shadow-emerald-900/40'
              } disabled:opacity-50`}
            >
              {loading ? (
                <span>Authenticating...</span>
              ) : (
                <>
                  <span>Sign in as {portalType === 'admin' ? 'Administrator' : 'User'}</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
