import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  Layers,
  Shield,
  Leaf,
  BookOpen,
  Database,
  FileText,
  Users,
  Settings,
  X,
  Sparkles,
  Scale,
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

interface SidebarProps {
  onClose?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const user = useAuthStore((state) => state.user);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Legal Chamber', path: '/chamber', icon: Scale },
    { name: 'AI Assistant', path: '/chat', icon: MessageSquare },
    { name: 'Classification', path: '/classify', icon: Layers },
    { name: 'IP Assessment', path: '/ip-assessment', icon: Shield },
    { name: 'ABS Compliance', path: '/abs', icon: Leaf },
    { name: 'Traditional Knowledge', path: '/tk', icon: BookOpen },
    { name: 'Source Explorer', path: '/sources', icon: Database },
    { name: 'Assessments', path: '/assessments', icon: FileText },
    { name: 'Human Review', path: '/review', icon: Users },
  ];


  return (
    <aside className="flex h-full flex-col bg-slate-950 text-white">

      {/* BRAND */}
      <div className="flex h-16 shrink-0 items-center justify-between border-b border-white/10 px-4">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-600 shadow-lg shadow-teal-900/30">
            <Leaf className="h-5 w-5" />
          </div>

          <div>
            <p className="text-sm font-bold tracking-tight">
              AyurLegal AI
            </p>
            <p className="text-[10px] text-slate-500">
              Regulatory Intelligence
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="rounded-lg p-1.5 text-slate-500 hover:bg-white/10 hover:text-white lg:hidden"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* NEW CHAT */}
      <div className="px-3 pt-4">
        <NavLink
          to="/chat"
          className="flex items-center justify-center gap-2 rounded-xl bg-teal-600 px-3 py-2.5 text-sm font-bold shadow-lg shadow-teal-950/30 transition hover:bg-teal-500"
        >
          <Sparkles className="h-4 w-4" />
          New AI Query
        </NavLink>
      </div>

      {/* NAV */}
      <div className="flex-1 overflow-y-auto px-3 py-5">
        <p className="mb-2 px-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
          Workspace
        </p>

        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                    isActive
                      ? 'bg-teal-500/15 text-teal-300 ring-1 ring-teal-500/20'
                      : 'text-slate-400 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon
                      className={`h-[18px] w-[18px] ${
                        isActive
                          ? 'text-teal-400'
                          : 'text-slate-600 group-hover:text-slate-300'
                      }`}
                    />
                    <span>{item.name}</span>
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {user?.role === 'ADMIN' && (
          <div className="mt-6 border-t border-white/10 pt-5">
            <p className="mb-2 px-2 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
              Administration
            </p>

            <NavLink
              to="/admin"
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium ${
                  isActive
                    ? 'bg-amber-500/10 text-amber-300'
                    : 'text-slate-400 hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <Settings className="h-[18px] w-[18px]" />
              Admin Dashboard
            </NavLink>
          </div>
        )}
      </div>

      {/* FOOTER */}
      <div className="border-t border-white/10 p-3">
        <div className="rounded-xl bg-white/[0.03] p-3">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/50" />
            <span className="text-xs font-semibold text-slate-300">
              AI Knowledge Base
            </span>
          </div>
          <p className="mt-1 text-[10px] leading-4 text-slate-600">
            Citation-grounded regulatory intelligence
          </p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;