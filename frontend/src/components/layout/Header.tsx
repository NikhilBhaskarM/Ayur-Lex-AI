import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, User, Settings, LogOut, ChevronDown } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { useAuth } from '@/context/AuthContext';
import JurisdictionSelector from '../common/JurisdictionSelector';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user, logout: zustandLogout } = useAuthStore();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const navigate = useNavigate();

  let authContext: any = null;
  try {
    authContext = useAuth();
  } catch {
    authContext = null;
  }

  const handleLogout = () => {
    if (authContext?.logout) {
      authContext.logout();
    }
    zustandLogout();
    localStorage.removeItem('ayur_token');
    localStorage.removeItem('ayur_role');
    localStorage.removeItem('ayur_username');
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user');
    setUserMenuOpen(false);
    navigate('/login');
  };

  const displayRole = (
    authContext?.role ||
    localStorage.getItem('ayur_role') ||
    user?.role ||
    localStorage.getItem('role') ||
    'USER'
  ).toUpperCase();

  const displayName =
    authContext?.user?.username ||
    localStorage.getItem('ayur_username') ||
    user?.full_name ||
    user?.email?.split('@')[0] ||
    'User';

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 bg-white/95 px-4 shadow-sm backdrop-blur sm:px-6">

      <div className="flex items-center gap-4">
        <button
          type="button"
          className="rounded-xl p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-800 lg:hidden"
          onClick={onMenuClick}
        >
          <Menu className="h-5 w-5" />
        </button>

        <div className="hidden sm:block">
          <p className="text-sm font-bold text-slate-900">
            Ayurvedic IPR Intelligence
          </p>
          <p className="text-[11px] text-slate-400">
            Research • Assess • Protect
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden sm:block">
          <JurisdictionSelector />
        </div>

        <select className="rounded-xl border border-slate-200 bg-slate-50 px-2.5 py-2 text-xs font-semibold text-slate-600 outline-none focus:border-teal-500 sm:hidden">
          <option>EN</option>
          <option>HI</option>
          <option>KN</option>
        </select>

        {/* Prominent Active Session Info with Username & Role Badge */}
        <div className="hidden md:flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 shadow-sm">
          <span className="text-xs font-bold text-slate-800 max-w-[130px] truncate">
            {displayName}
          </span>
          <span
            className={`inline-flex items-center rounded-md px-1.5 py-0.5 text-[11px] font-bold tracking-wide border ${
              displayRole === 'ADMIN'
                ? 'bg-amber-100 text-amber-900 border-amber-300'
                : 'bg-emerald-100 text-emerald-900 border-emerald-300'
            }`}
          >
            [{displayRole === 'ADMIN' ? 'Admin' : 'User'}]
          </span>
        </div>

        {/* User profile dropdown button */}
        <div className="relative">
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-2 py-1.5 shadow-sm transition hover:border-teal-200"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-teal-700 to-emerald-600 text-white">
              <User className="h-4 w-4" />
            </div>

            <div className="hidden text-left sm:block">
              <p className="max-w-[120px] truncate text-xs font-bold text-slate-800">
                {displayName}
              </p>
              <p className={`text-[10px] font-bold ${displayRole === 'ADMIN' ? 'text-amber-600' : 'text-emerald-600'}`}>
                [{displayRole === 'ADMIN' ? 'Admin' : 'User'}]
              </p>
            </div>

            <ChevronDown className="hidden h-3.5 w-3.5 text-slate-400 sm:block" />
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 z-50 mt-2 w-56 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
              <div className="border-b border-slate-100 px-4 py-3">
                <p className="text-sm font-bold text-slate-900">
                  {displayName}
                </p>
                <p className="mt-0.5 truncate text-xs text-slate-500">
                  {user?.email || `${displayName.toLowerCase()}@ayurlex.ai`}
                </p>
                <span className="mt-1.5 inline-block rounded-md bg-emerald-50 px-2 py-0.5 text-[10px] font-bold text-emerald-700 border border-emerald-200">
                  Role: {displayRole}
                </span>
              </div>

              <a
                href="/settings"
                className="flex items-center gap-3 px-4 py-3 text-sm text-slate-700 hover:bg-slate-50"
              >
                <Settings className="h-4 w-4 text-slate-400" />
                Settings
              </a>

              <button
                onClick={handleLogout}
                className="flex w-full items-center gap-3 border-t border-slate-100 px-4 py-3 text-sm font-semibold text-red-600 hover:bg-red-50 cursor-pointer"
              >
                <LogOut className="h-4 w-4" />
                Sign out
              </button>
            </div>
          )}
        </div>

        {/* Dedicated Prominent Header Logout Button */}
        <button
          type="button"
          onClick={handleLogout}
          title="Sign out of Ayur-Lex-AI"
          className="flex items-center gap-1.5 rounded-xl border border-red-200 bg-red-50/80 px-3 py-2 text-xs font-semibold text-red-700 shadow-sm transition hover:bg-red-100 hover:border-red-300 hover:text-red-900 cursor-pointer"
        >
          <LogOut className="h-4 w-4 text-red-600" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
};

export default Header;