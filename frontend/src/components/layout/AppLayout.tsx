import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import DisclaimerBanner from '../common/DisclaimerBanner';

const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 font-sans text-gray-900">
      {/* Sidebar for Mobile */}
      <div 
        className={`fixed inset-0 z-20 bg-gray-900/50 transition-opacity lg:hidden ${sidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`} 
        onClick={() => setSidebarOpen(false)}
      />
      
      <div className={`fixed inset-y-0 left-0 z-30 w-64 transform bg-[#1a365d] transition-transform duration-300 lg:static lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <Sidebar onClose={() => setSidebarOpen(false)} />
      </div>

      {/* Main Content */}
      <div className="flex flex-1 flex-col w-0 overflow-hidden">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 overflow-y-auto bg-gray-50 relative pb-10">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-6 h-full">
            <Outlet />
          </div>
        </main>
        <DisclaimerBanner />
      </div>
    </div>
  );
};

export default AppLayout;
