import React from 'react';
import { Users, FileText, Database, Activity } from 'lucide-react';

const AdminDashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-[#1a365d]">Admin Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">System overview and management.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Total Users', value: '1,245', icon: Users, color: 'text-blue-600' },
          { title: 'Active Documents', value: '8,432', icon: FileText, color: 'text-teal-600' },
          { title: 'Data Sources', value: '145', icon: Database, color: 'text-amber-600' },
          { title: 'Daily Queries', value: '3,892', icon: Activity, color: 'text-purple-600' },
        ].map((stat, i) => (
          <div key={i} className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">{stat.title}</p>
                <p className="text-3xl font-semibold text-gray-900 mt-2">{stat.value}</p>
              </div>
              <div className={`p-3 bg-gray-50 rounded-full ${stat.color}`}>
                <stat.icon className="w-6 h-6" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h2>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center text-gray-500">
          Activity Logs Placeholder
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
