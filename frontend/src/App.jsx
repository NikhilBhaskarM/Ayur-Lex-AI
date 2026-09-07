import React, { useState, useEffect } from 'react';
import { AuthProvider } from './context/AuthContext';
import LoginPage from './components/Auth/LoginPage';
import Navbar from './components/layout/Navbar';
import AdminDashboard from './components/Admin/AdminDashboard';
import TriageWizard from './pages/TriageWizard';
import SynergyCalculator from './pages/SynergyCalculator';
import LegalChamberPanel from './components/LegalChamberPanel';
import Dashboard from './pages/Dashboard';
import { Compass, Sparkles, Layers, ArrowRight } from 'lucide-react';

export const App = () => {
  // 1. State Management
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return Boolean(
      localStorage.getItem('ayur_token') || localStorage.getItem('token')
    );
  });

  const [userRole, setUserRole] = useState(() => {
    return (
      localStorage.getItem('ayur_role') ||
      localStorage.getItem('role') ||
      'user'
    ).toLowerCase();
  });

  const [currentView, setCurrentView] = useState(() => {
    const role = (
      localStorage.getItem('ayur_role') ||
      localStorage.getItem('role') ||
      'user'
    ).toLowerCase();
    return role === 'admin' ? 'admin' : 'dashboard';
  });

  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [dashboardTab, setDashboardTab] = useState('triage'); // 'triage' | 'synergy' | 'hub'

  // 2. Session Restoration & Auto-Verification
  useEffect(() => {
    const verifySession = async () => {
      const token =
        localStorage.getItem('ayur_token') || localStorage.getItem('token');

      if (!token) {
        setIsAuthenticated(false);
        setIsCheckingAuth(false);
        return;
      }

      try {
        const response = await fetch('/api/auth/verify', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          const verifiedRole = (
            data.role ||
            localStorage.getItem('ayur_role') ||
            'user'
          ).toLowerCase();

          setIsAuthenticated(true);
          setUserRole(verifiedRole);
          localStorage.setItem('ayur_role', verifiedRole);
        } else {
          // Token expired or invalid (401)
          localStorage.removeItem('ayur_token');
          localStorage.removeItem('ayur_role');
          localStorage.removeItem('ayur_username');
          localStorage.removeItem('token');
          localStorage.removeItem('access_token');
          localStorage.removeItem('role');
          localStorage.removeItem('user');
          setIsAuthenticated(false);
        }
      } catch (err) {
        console.warn('Session verification fallback (offline dev support):', err);
        // Graceful fallback for local development if network is disconnected
        setIsAuthenticated(true);
      } finally {
        setIsCheckingAuth(false);
      }
    };

    verifySession();
  }, []);

  const handleLoginSuccess = (role) => {
    const verifiedRole = (
      role ||
      localStorage.getItem('ayur_role') ||
      localStorage.getItem('role') ||
      'user'
    ).toLowerCase();

    setIsAuthenticated(true);
    setUserRole(verifiedRole);

    if (verifiedRole === 'admin') {
      setCurrentView('admin');
    } else {
      setCurrentView('dashboard');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('ayur_token');
    localStorage.removeItem('ayur_role');
    localStorage.removeItem('ayur_username');
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user');

    setIsAuthenticated(false);
    setUserRole('user');
    setCurrentView('dashboard');
  };

  // While verifying authentication status, render a sleek loader
  if (isCheckingAuth) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-slate-100">
        <div className="h-10 w-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-xs font-semibold tracking-wide text-slate-400">
          Verifying security token and session credentials...
        </p>
      </div>
    );
  }

  // 3. Conditional View Rendering
  if (!isAuthenticated) {
    return (
      <AuthProvider>
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      </AuthProvider>
    );
  }

  return (
    <AuthProvider>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
        {/* Top Navbar Component */}
        <Navbar
          currentView={currentView}
          onNavigate={(view) => {
            // Guard admin view
            if (view === 'admin' && userRole !== 'admin') {
              setCurrentView('dashboard');
            } else {
              setCurrentView(view);
            }
          }}
          onLogout={handleLogout}
          userRole={userRole}
        />

        {/* View Routing Body */}
        <main className="flex-1 overflow-y-auto">
          {currentView === 'admin' && userRole === 'admin' ? (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
              <AdminDashboard
                onSwitchToTriage={() => {
                  setCurrentView('dashboard');
                  setDashboardTab('triage');
                }}
              />
            </div>
          ) : currentView === 'debate' ? (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 pb-12">
              <LegalChamberPanel />
            </div>
          ) : (
            /* currentView === 'dashboard' */
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 pb-12">
              {/* Formulation Triage & Tools Sub-Nav Bar */}
              <div className="flex flex-wrap items-center justify-between gap-3 p-2 bg-slate-900/80 rounded-2xl border border-slate-800 backdrop-blur shadow-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setDashboardTab('triage')}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      dashboardTab === 'triage'
                        ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
                    }`}
                  >
                    <Compass className="h-4 w-4" />
                    <span>Patent Triage Stepper</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setDashboardTab('synergy')}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      dashboardTab === 'synergy'
                        ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
                    }`}
                  >
                    <Sparkles className="h-4 w-4" />
                    <span>Section 3(e) Synergy Calculator</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setDashboardTab('hub')}
                    className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                      dashboardTab === 'hub'
                        ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80'
                    }`}
                  >
                    <Layers className="h-4 w-4" />
                    <span>Regulatory Framework Hub</span>
                  </button>
                </div>

                <button
                  type="button"
                  onClick={() => setCurrentView('debate')}
                  className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-emerald-400 text-xs font-bold border border-emerald-900/40 transition cursor-pointer"
                >
                  <span>Launch Multi-Agent Debate Chamber</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </button>
              </div>

              {/* View Components */}
              <div className="mt-4">
                {dashboardTab === 'triage' && <TriageWizard />}
                {dashboardTab === 'synergy' && <SynergyCalculator />}
                {dashboardTab === 'hub' && <Dashboard />}
              </div>
            </div>
          )}
        </main>
      </div>
    </AuthProvider>
  );
};

export default App;
