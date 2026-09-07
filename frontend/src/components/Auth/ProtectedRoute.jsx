import React from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useAuthStore } from '../../store/authStore';
import { ShieldAlert, ArrowLeft, LogOut, KeyRound } from 'lucide-react';

export const ProtectedRoute = ({ children, requiredRole = '' }) => {
  const navigate = useNavigate();
  const authContext = useAuth();
  const zustandStore = useAuthStore();

  // Combine AuthContext and zustand store for robust fallback
  const token = authContext?.token || zustandStore?.token || localStorage.getItem('ayur_token') || localStorage.getItem('token');
  const role = (authContext?.role || zustandStore?.user?.role || localStorage.getItem('ayur_role') || localStorage.getItem('role') || '').toLowerCase();
  const user = authContext?.user || zustandStore?.user;
  const isAuthenticated = Boolean(token);

  // 1. Unauthenticated check
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // 2. Role restriction check (e.g., requiredRole === 'admin')
  if (requiredRole && role !== requiredRole.toLowerCase()) {
    return (
      <div className="min-h-[70vh] flex items-center justify-center p-6 text-slate-100">
        <div className="max-w-md w-full bg-slate-900/90 backdrop-blur-md rounded-2xl border border-red-900/40 p-8 shadow-2xl text-center relative overflow-hidden">
          <div className="absolute -top-16 -right-16 w-32 h-32 bg-red-500/10 rounded-full blur-2xl pointer-events-none" />

          <div className="mx-auto w-14 h-14 rounded-2xl bg-red-950/80 border border-red-800/60 flex items-center justify-center mb-5 text-red-400 shadow-lg shadow-red-950/50">
            <ShieldAlert className="w-8 h-8" />
          </div>

          <span className="inline-block px-2.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-red-950 border border-red-800/80 text-red-300 mb-2">
            HTTP 403 Forbidden
          </span>

          <h2 className="text-2xl font-bold text-white mb-2">Access Denied</h2>
          <p className="text-sm text-slate-400 mb-6 leading-relaxed">
            Insufficient permissions. Your current account (<strong className="text-slate-200">{user?.username || 'Current User'}</strong>) is assigned the <span className="text-amber-400 font-semibold uppercase">{role || 'user'}</span> role. Administrative privileges (<code className="text-emerald-400 font-mono text-xs">admin</code>) are required to access this portal.
          </p>

          <div className="flex flex-col gap-2.5">
            <button
              onClick={() => navigate('/')}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
              Return to Main Dashboard
            </button>
            <button
              onClick={() => {
                authContext.logout();
                navigate('/login');
              }}
              className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-red-950/40 hover:bg-red-900/50 text-red-300 text-xs font-semibold border border-red-800/50 transition-all"
            >
              <KeyRound className="w-4 h-4" />
              Switch Account / Admin Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 3. Authorized
  return <>{children}</>;
};

export default ProtectedRoute;
