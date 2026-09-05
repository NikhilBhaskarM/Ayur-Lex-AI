import React, { useState } from 'react';
import { Menu, User, Settings, LogOut, ChevronDown } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import JurisdictionSelector from '../common/JurisdictionSelector';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user, logout } = useAuthStore();
  const [userMenuOpen, setUserMenuOpen] = useState(false);

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
                {user?.full_name || 'User'}
              </p>
              <p className="text-[10px] text-slate-400">
                {user?.role || 'USER'}
              </p>
            </div>

            <ChevronDown className="hidden h-3.5 w-3.5 text-slate-400 sm:block" />
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 z-50 mt-2 w-56 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
              <div className="border-b border-slate-100 px-4 py-3">
                <p className="text-sm font-bold text-slate-900">
                  {user?.full_name || 'User'}
                </p>
                <p className="mt-0.5 truncate text-xs text-slate-500">
                  {user?.email}
                </p>
              </div>

              <a
                href="/settings"
                className="flex items-center gap-3 px-4 py-3 text-sm text-slate-700 hover:bg-slate-50"
              >
                <Settings className="h-4 w-4 text-slate-400" />
                Settings
              </a>

              <button
                onClick={() => {
                  logout();
                  setUserMenuOpen(false);
                }}
                className="flex w-full items-center gap-3 border-t border-slate-100 px-4 py-3 text-sm text-red-600 hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" />
                Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;