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
import LoginPage from './components/Auth/LoginPage';
import Register from './pages/Register';
import Settings from './pages/Settings';
import TriageWizard from './pages/TriageWizard';
import SynergyCalculator from './pages/SynergyCalculator';
import LegalChamberPanel from './components/LegalChamberPanel';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/Auth/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<LoginPage initialRegister={true} />} />
        
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
          <Route
            path="admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminDashboard />
              </ProtectedRoute>
            }
          />
          <Route path="settings" element={<Settings />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
