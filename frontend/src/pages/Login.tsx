import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  ShieldCheck,
  AlertCircle,
  Mail,
  Lock,
  ArrowRight,
  Sparkles,
  Leaf,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/api/auth';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    setErrorMessage('');
    setLoading(true);

    try {
      const tokenData = await authApi.login({ email, password });

      useAuthStore.getState().setAuth(
        {
          id: '',
          email,
          full_name: 'User',
          role: 'USER',
          preferred_language: 'en',
          is_active: true,
        },
        tokenData.access_token
      );

      try {
        const userProfile = await authApi.getMe();
        login(userProfile, tokenData.access_token);
      } catch {
        login(
          {
            id: '',
            email,
            full_name: email.split('@')[0],
            role: 'USER',
            preferred_language: 'en',
            is_active: true,
          },
          tokenData.access_token
        );
      }

      toast.success('Signed in successfully');
      navigate('/');
    } catch (err: any) {
      const detail =
        err.response?.data?.detail ||
        err.message ||
        'Failed to sign in. Please check your credentials.';

      setErrorMessage(detail);
      toast.error(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* LEFT BRAND PANEL */}
        <div className="relative hidden overflow-hidden bg-gradient-to-br from-teal-950 via-emerald-950 to-slate-950 p-12 text-white lg:flex lg:flex-col lg:justify-between">
          <div className="absolute -right-24 -top-24 h-72 w-72 rounded-full bg-teal-500/20 blur-3xl" />
          <div className="absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-emerald-400/10 blur-3xl" />

          <div className="relative z-10">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/10 ring-1 ring-white/20">
                <Leaf className="h-6 w-6 text-emerald-300" />
              </div>

              <div>
                <p className="text-lg font-bold">AyurLegal AI</p>
                <p className="text-xs text-teal-200">
                  IPR • Regulatory Intelligence
                </p>
              </div>
            </div>
          </div>

          <div className="relative z-10 max-w-xl">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-teal-100 backdrop-blur">
              <Sparkles className="h-3.5 w-3.5" />
              RAG-powered legal intelligence
            </div>

            <h1 className="text-5xl font-bold leading-tight">
              Protecting
              <span className="block text-emerald-300">
                Ayurvedic innovation.
              </span>
            </h1>

            <p className="mt-6 max-w-lg text-base leading-7 text-slate-300">
              Understand patents, trademarks, traditional knowledge,
              biodiversity requirements and Ayurvedic regulations with
              evidence-backed AI assistance.
            </p>

            <div className="mt-8 grid grid-cols-3 gap-3">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <p className="text-xl font-bold">RAG</p>
                <p className="mt-1 text-xs text-slate-400">Grounded answers</p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <p className="text-xl font-bold">Citations</p>
                <p className="mt-1 text-xs text-slate-400">Trusted sources</p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <p className="text-xl font-bold">3+</p>
                <p className="mt-1 text-xs text-slate-400">Languages</p>
              </div>
            </div>
          </div>

          <p className="relative z-10 text-xs text-slate-500">
            Built for Ayurvedic innovators, researchers and IPR professionals.
          </p>
        </div>

        {/* LOGIN PANEL */}
        <div className="flex items-center justify-center bg-slate-50 px-5 py-12 sm:px-8">
          <div className="w-full max-w-md">

            <div className="mb-8 lg:hidden">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-teal-700 text-white shadow-lg">
                  <Leaf className="h-6 w-6" />
                </div>
                <div>
                  <p className="text-xl font-bold text-slate-900">
                    AyurLegal AI
                  </p>
                  <p className="text-xs text-slate-500">
                    IPR & Regulatory Intelligence
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-7">
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-teal-100">
                <ShieldCheck className="h-6 w-6 text-teal-700" />
              </div>

              <h2 className="text-3xl font-bold text-slate-950">
                Welcome back
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Sign in to your AyurLegal intelligence workspace.
              </p>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/50 sm:p-8">

              {errorMessage && (
                <div className="mb-5 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                  <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
                  <span>{errorMessage}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">

                <div>
                  <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Email address
                  </label>

                  <div className="relative">
                    <Mail className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />

                    <input
                      id="email"
                      type="email"
                      autoComplete="email"
                      required
                      placeholder="you@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="password"
                    className="mb-2 block text-sm font-semibold text-slate-700"
                  >
                    Password
                  </label>

                  <div className="relative">
                    <Lock className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />

                    <input
                      id="password"
                      type="password"
                      autoComplete="current-password"
                      required
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full rounded-xl border border-slate-200 bg-slate-50 py-3 pl-10 pr-4 text-sm outline-none transition focus:border-teal-500 focus:bg-white focus:ring-4 focus:ring-teal-500/10"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-teal-700 py-3.5 text-sm font-bold text-white shadow-lg shadow-teal-700/20 transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {loading ? 'Signing in...' : 'Sign in'}
                  {!loading && <ArrowRight className="h-4 w-4" />}
                </button>
              </form>

              <div className="my-6 flex items-center gap-3">
                <div className="h-px flex-1 bg-slate-200" />
                <span className="text-xs text-slate-400">NEW USER?</span>
                <div className="h-px flex-1 bg-slate-200" />
              </div>

              <p className="text-center text-sm text-slate-500">
                Don't have an account?{' '}
                <Link
                  to="/register"
                  className="font-bold text-teal-700 hover:text-teal-800"
                >
                  Create one →
                </Link>
              </p>
            </div>

            <p className="mt-6 text-center text-xs text-slate-400">
              Your regulatory intelligence workspace
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;