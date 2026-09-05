import React, { useState } from 'react';
import { Menu, User, Settings, LogOut } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import JurisdictionSelector from '../common/JurisdictionSelector';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  const { user, logout } = useAuthStore();
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-4 sm:px-6 lg:px-8">
      <div className="flex items-center gap-4">
        <button
          type="button"
          className="lg:hidden -ml-2 p-2 text-gray-500 hover:text-gray-700"
          onClick={onMenuClick}
        >
          <Menu className="h-6 w-6" aria-hidden="true" />
        </button>
        <h1 className="text-xl font-semibold text-[#1a365d] hidden sm:block">
          Ayurvedic IPR & Regulatory AI Assistant
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <JurisdictionSelector />
        
        <select className="hidden sm:block rounded-md border-gray-300 text-sm shadow-sm focus:border-[#2c7a7b] focus:ring-[#2c7a7b]">
          <option>EN</option>
          <option>HI</option>
          <option>KN</option>
        </select>

        <div className="relative">
          <button
            onClick={() => setUserMenuOpen(!userMenuOpen)}
            className="flex h-9 w-9 items-center justify-center rounded-full bg-[#1a365d] text-white hover:bg-[#0f2342] focus:outline-none focus:ring-2 focus:ring-[#2c7a7b] focus:ring-offset-2"
          >
            <span className="sr-only">Open user menu</span>
            <User className="h-5 w-5" />
          </button>

          {userMenuOpen && (
            <div className="absolute right-0 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
              <div className="px-4 py-2 border-b border-gray-100">
                <p className="text-sm font-medium text-gray-900">{user?.full_name || 'User'}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <a href="/settings" className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                <Settings className="mr-2 h-4 w-4" /> Settings
              </a>
              <button
                onClick={() => { logout(); setUserMenuOpen(false); }}
                className="flex w-full items-center px-4 py-2 text-sm text-red-700 hover:bg-gray-100"
              >
                <LogOut className="mr-2 h-4 w-4" /> Sign out
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
