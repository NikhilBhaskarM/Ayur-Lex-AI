import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, MessageSquare, Layers, Shield, 
  Leaf, BookOpen, Database, FileText, Users, Settings, X
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

interface SidebarProps {
  onClose?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onClose }) => {
  const user = useAuthStore(state => state.user);
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'AI Assistant', path: '/chat', icon: MessageSquare },
    { name: 'Classification', path: '/classify', icon: Layers },
    { name: 'IP Assessment', path: '/ip-assessment', icon: Shield },
    { name: 'ABS Compliance', path: '/abs', icon: Leaf },
    { name: 'TK Search', path: '/tk', icon: BookOpen },
    { name: 'Sources', path: '/sources', icon: Database },
    { name: 'Assessments', path: '/assessments', icon: FileText },
    { name: 'Human Review', path: '/review', icon: Users },
  ];

  return (
    <div className="flex h-full flex-col bg-[#1a365d] text-white">
      <div className="flex h-16 shrink-0 items-center px-4 justify-between border-b border-[#2a4a7f]">
        <div className="flex items-center gap-2">
          <Shield className="h-8 w-8 text-[#d69e2e]" />
          <span className="text-lg font-bold leading-tight tracking-tight">AyurLex AI</span>
        </div>
        <button onClick={onClose} className="lg:hidden text-gray-300 hover:text-white">
          <X className="h-6 w-6" />
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="flex-1 space-y-1 px-2">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `group flex items-center rounded-md px-2 py-2 text-sm font-medium ${
                  isActive
                    ? 'bg-[#0f2342] text-white'
                    : 'text-gray-300 hover:bg-[#2a4a7f] hover:text-white'
                }`
              }
            >
              <item.icon className="mr-3 h-5 w-5 shrink-0 text-[#2c7a7b]" aria-hidden="true" />
              {item.name}
            </NavLink>
          ))}
          
          {user?.role === 'ADMIN' && (
            <div className="pt-4 mt-4 border-t border-[#2a4a7f]">
              <NavLink
                to="/admin"
                className={({ isActive }) =>
                  `group flex items-center rounded-md px-2 py-2 text-sm font-medium ${
                    isActive
                      ? 'bg-[#0f2342] text-white'
                      : 'text-gray-300 hover:bg-[#2a4a7f] hover:text-white'
                  }`
                }
              >
                <Settings className="mr-3 h-5 w-5 shrink-0 text-[#d69e2e]" aria-hidden="true" />
                Admin Dashboard
              </NavLink>
            </div>
          )}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
