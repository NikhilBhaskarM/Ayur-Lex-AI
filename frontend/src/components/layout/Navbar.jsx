import React from 'react';
import {
  Scale,
  Compass,
  Cpu,
  Server,
  LogOut,
  User,
  Shield,
  Layers,
  MessageSquare,
  Sparkles,
} from 'lucide-react';

export const Navbar = ({
  currentView = 'dashboard',
  onNavigate = () => {},
  onLogout = () => {},
  userRole = 'user',
}) => {
  const username =
    localStorage.getItem('ayur_username') ||
    localStorage.getItem('user') ? (JSON.parse(localStorage.getItem('user') || '{}').username || 'Researcher') : 'Researcher';

  const role = (
    userRole ||
    localStorage.getItem('ayur_role') ||
    localStorage.getItem('role') ||
    'user'
  ).toLowerCase();

  const isAdmin = role === 'admin';

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/90 backdrop-blur-md px-4 sm:px-6 lg:px-8 py-3 shadow-lg">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4">
        {/* Brand / Logo */}
        <div
          onClick={() => onNavigate('dashboard')}
          className="flex items-center gap-3 cursor-pointer select-none group"
        >
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white shadow-md shadow-emerald-950/40 group-hover:scale-105 transition-transform">
            <Scale className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-base font-black tracking-tight text-white group-hover:text-emerald-300 transition-colors">
                Ayur-Lex-AI
              </span>
              <span className="rounded bg-emerald-950 px-1.5 py-0.2 text-[10px] font-bold text-emerald-400 border border-emerald-800/60">
                v1.0
              </span>
            </div>
            <p className="text-[10.5px] font-medium text-slate-400 hidden sm:block">
              Ayurvedic IPR &amp; Statutory Regulatory Platform
            </p>
          </div>
        </div>

        {/* Center View Navigation Switcher */}
        <nav className="flex items-center gap-1.5 p-1 bg-slate-900/90 rounded-xl border border-slate-800 shadow-inner">
          {/* Dashboard & Triage View */}
          <button
            type="button"
            onClick={() => onNavigate('dashboard')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              currentView === 'dashboard'
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Compass className="h-3.5 w-3.5" />
            <span>Patent Triage</span>
          </button>

          {/* Multi-Agent Chamber View */}
          <button
            type="button"
            onClick={() => onNavigate('debate')}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
              currentView === 'debate'
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Cpu className="h-3.5 w-3.5" />
            <span>Debate Chamber</span>
          </button>

          {/* Admin Telemetry View (Role Protected) */}
          {isAdmin && (
            <button
              type="button"
              onClick={() => onNavigate('admin')}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                currentView === 'admin'
                  ? 'bg-amber-600 text-white shadow-md shadow-amber-950'
                  : 'text-amber-400/80 hover:text-amber-300 hover:bg-slate-800/60'
              }`}
            >
              <Server className="h-3.5 w-3.5" />
              <span>Admin Telemetry</span>
            </button>
          )}
        </nav>

        {/* Right: Active Session Badges & Logout Action */}
        <div className="flex items-center gap-3">
          {/* User & Role Badge */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs">
            <div className="flex h-6 w-6 items-center justify-center rounded-lg bg-slate-800 text-slate-300">
              <User className="h-3.5 w-3.5" />
            </div>
            <span className="font-semibold text-slate-200 max-w-[110px] truncate">
              {username}
            </span>
            <span
              className={`rounded-md px-1.5 py-0.5 text-[10px] font-extrabold uppercase tracking-wide border ${
                isAdmin
                  ? 'bg-amber-950/80 text-amber-300 border-amber-800/80'
                  : 'bg-emerald-950/80 text-emerald-300 border-emerald-800/80'
              }`}
            >
              [{isAdmin ? 'Admin' : 'User'}]
            </span>
          </div>

          {/* Sign Out Button */}
          <button
            type="button"
            onClick={onLogout}
            title="Sign out of Ayur-Lex-AI"
            className="flex items-center gap-1.5 rounded-xl border border-red-900/60 bg-red-950/40 px-3 py-1.5 text-xs font-semibold text-red-300 hover:bg-red-900/50 hover:text-red-100 hover:border-red-700 transition cursor-pointer"
          >
            <LogOut className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
