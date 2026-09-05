import React from 'react';
import { Link } from 'react-router-dom';
import { 
  MessageSquare, Layers, Shield, 
  Leaf, BookOpen, Database, FileText, Users, Scale
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const features = [
    { name: 'AI Assistant', desc: 'Chat with our legal AI for regulatory queries.', icon: MessageSquare, link: '/chat', color: 'text-blue-600', bg: 'bg-blue-100' },
    { name: 'Formulation Classification', desc: 'Determine regulatory category of your product.', icon: Layers, link: '/classify', color: 'text-indigo-600', bg: 'bg-indigo-100' },
    { name: 'Patent/IP Assessment', desc: 'Evaluate patentability and IP options.', icon: Shield, link: '/ip-assessment', color: 'text-purple-600', bg: 'bg-purple-100' },
    { name: 'Traditional Knowledge Search', desc: 'Check TKDL and state registers.', icon: BookOpen, link: '/tk', color: 'text-amber-600', bg: 'bg-amber-100' },
    { name: 'ABS Compliance', desc: 'Check National Biodiversity Authority rules.', icon: Leaf, link: '/abs', color: 'text-green-600', bg: 'bg-green-100' },
    { name: 'Regulatory Classification', desc: 'Check D&C Act and international rules.', icon: Scale, link: '/classify', color: 'text-teal-600', bg: 'bg-teal-100' },
    { name: 'Source Explorer', desc: 'Browse the repository of legal sources.', icon: Database, link: '/sources', color: 'text-gray-600', bg: 'bg-gray-100' },
    { name: 'Saved Assessments', desc: 'View past analysis and reports.', icon: FileText, link: '/assessments', color: 'text-[#1a365d]', bg: 'bg-blue-50' },
    { name: 'Human Facilitator', desc: 'Request expert review of AI analysis.', icon: Users, link: '/review', color: 'text-[#d69e2e]', bg: 'bg-yellow-50' },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className="bg-[#1a365d] rounded-2xl p-8 text-white shadow-lg relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10 transform translate-x-1/4 -translate-y-1/4">
          <Shield className="w-64 h-64" />
        </div>
        <div className="relative z-10 max-w-2xl">
          <h1 className="text-3xl font-bold mb-4">Welcome to AyurLex AI</h1>
          <p className="text-[#a0aec0] mb-8 text-lg">
            Your intelligent assistant for Ayurvedic Intellectual Property Rights and Regulatory Compliance in India and Worldwide.
          </p>
          <Link 
            to="/chat" 
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-[#1a365d] bg-[#d69e2e] hover:bg-[#b7791f] transition-colors shadow-md"
          >
            <MessageSquare className="w-5 h-5 mr-2" />
            Ask an Ayurvedic IPR & Regulatory Question
          </Link>
        </div>
      </div>

      {/* Grid */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4 px-1">Tools & Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map((item) => (
            <Link 
              key={item.name} 
              to={item.link}
              className="group bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col items-start"
            >
              <div className={`p-3 rounded-lg ${item.bg} mb-4 group-hover:scale-110 transition-transform`}>
                <item.icon className={`w-6 h-6 ${item.color}`} />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-1">{item.name}</h3>
              <p className="text-sm text-gray-500">{item.desc}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
