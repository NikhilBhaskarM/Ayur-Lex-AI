import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Classify from './pages/Classify';
import IPAssessment from './pages/IPAssessment';
import ABSCompliance from './pages/ABSCompliance';
import TKSearch from './pages/TKSearch';
import Sources from './pages/Sources';
import Assessments from './pages/Assessments';
import HumanReview from './pages/HumanReview';
import AdminDashboard from './pages/AdminDashboard';
import Login from './pages/Login';
import Register from './pages/Register';
import Settings from './pages/Settings';
import TriageWizard from './pages/TriageWizard';
import SynergyCalculator from './pages/SynergyCalculator';
import LegalChamberPanel from './components/LegalChamberPanel';
import { useAuthStore } from '@/store/authStore';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="chamber" element={<div className="pb-10"><LegalChamberPanel /></div>} />
        <Route path="chat" element={<Chat />} />
        <Route path="classify" element={<Classify />} />
        <Route path="triage" element={<TriageWizard />} />
        <Route path="synergy" element={<SynergyCalculator />} />
        <Route path="ip-assessment" element={<IPAssessment />} />

        <Route path="abs" element={<ABSCompliance />} />
        <Route path="tk" element={<TKSearch />} />
        <Route path="sources" element={<Sources />} />
        <Route path="assessments" element={<Assessments />} />
        <Route path="review" element={<HumanReview />} />
        <Route path="admin" element={<AdminDashboard />} />
        <Route path="settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
