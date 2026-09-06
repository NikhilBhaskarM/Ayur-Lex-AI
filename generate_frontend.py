import os
import json

base_dir = r"f:\rag2\frontend"

directories = [
    "",
    "src",
    "src/types",
    "src/api",
    "src/store",
    "src/hooks",
    "src/utils",
    "src/components",
    "src/components/layout",
    "src/components/common",
    "src/components/chat",
    "src/pages",
    "public",
    "public/locales",
    "public/locales/en",
    "public/locales/hi",
    "public/locales/kn",
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d.replace("/", os.sep)), exist_ok=True)

files = {}

files["Dockerfile"] = """FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
"""

files["package.json"] = """{
  "name": "rag2-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.62.0",
    "axios": "^1.7.0",
    "clsx": "^2.1.1",
    "i18next": "^23.11.0",
    "lucide-react": "^0.378.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-hot-toast": "^2.4.1",
    "react-i18next": "^14.1.1",
    "react-markdown": "^9.0.1",
    "react-router-dom": "^6.28.0",
    "tailwind-merge": "^2.3.0",
    "zustand": "^5.0.0-rc.2"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.2.2",
    "vite": "^5.2.0"
  }
}
"""

files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
"""

files["vite.config.ts"] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
"""

files["tailwind.config.ts"] = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1a365d',
        secondary: '#d69e2e',
        accent: '#2c7a7b',
        background: '#fafaf5',
        surface: '#ffffff',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
"""

files["postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

files["index.html"] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <title>Ayurvedic IPR & Regulatory AI Assistant</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

files["src/index.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-background text-gray-900 font-sans;
  }
}

/* Custom Scrollbar for a polished look */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
"""

files["src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from './App.tsx';
import './index.css';
import './i18n';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
);
"""

files["src/App.tsx"] = """import { Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
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
import { useAuthStore } from './store/authStore';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="chat" element={<Chat />} />
          <Route path="classify" element={<Classify />} />
          <Route path="ip-assessment" element={<IPAssessment />} />
          <Route path="abs" element={<ABSCompliance />} />
          <Route path="tk" element={<TKSearch />} />
          <Route path="sources" element={<Sources />} />
          <Route path="assessments" element={<Assessments />} />
          <Route path="review" element={<HumanReview />} />
          <Route path="admin" element={<AdminDashboard />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
"""

files["src/i18n.ts"] = """import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import translationEN from '../public/locales/en/translation.json';
import translationHI from '../public/locales/hi/translation.json';
import translationKN from '../public/locales/kn/translation.json';

const resources = {
  en: { translation: translationEN },
  hi: { translation: translationHI },
  kn: { translation: translationKN },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
"""

files["src/types/index.ts"] = """export interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}
export interface TokenResponse {
  token: string;
  user: User;
}
export type JurisdictionType = 'INDIA' | 'INTERNATIONAL';
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Citation {
  id: string;
  title: string;
  authority: string;
  url?: string;
  passage: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  jurisdiction?: JurisdictionType;
  confidence?: ConfidenceLevel;
  citations?: Citation[];
  timestamp: string;
}

export interface Conversation {
  id: string;
  title: string;
  updatedAt: string;
}

export interface ChatRequest {
  message: string;
  jurisdiction: JurisdictionType;
}

export interface Source {
  id: string;
  name: string;
  authority: string;
  jurisdiction: JurisdictionType;
  type: string;
  status: string;
  lastCrawled: string;
}
"""

files["src/api/client.ts"] = """import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
"""

files["src/api/auth.ts"] = """import apiClient from './client';
export const login = async (data: any) => apiClient.post('/auth/login', data).then(res => res.data);
export const register = async (data: any) => apiClient.post('/auth/register', data).then(res => res.data);
export const getMe = async () => apiClient.get('/auth/me').then(res => res.data);
"""

files["src/api/chat.ts"] = """import apiClient from './client';
export const sendMessage = async (data: any) => apiClient.post('/chat', data).then(res => res.data);
export const getConversations = async () => apiClient.get('/chat/conversations').then(res => res.data);
export const getConversation = async (id: string) => apiClient.get(`/chat/conversations/${id}`).then(res => res.data);
export const deleteConversation = async (id: string) => apiClient.delete(`/chat/conversations/${id}`).then(res => res.data);
"""

files["src/api/sources.ts"] = """import apiClient from './client';
export const getSources = async () => apiClient.get('/sources').then(res => res.data);
export const getSource = async (id: string) => apiClient.get(`/sources/${id}`).then(res => res.data);
"""

files["src/api/admin.ts"] = """import apiClient from './client';
export const getStats = async () => apiClient.get('/admin/stats').then(res => res.data);
export const getUsers = async () => apiClient.get('/admin/users').then(res => res.data);
export const getIngestionStatus = async () => apiClient.get('/admin/ingestion').then(res => res.data);
export const triggerIngestion = async () => apiClient.post('/admin/ingestion').then(res => res.data);
"""

files["src/store/authStore.ts"] = """import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
      setUser: (user) => set({ user }),
    }),
    { name: 'auth-storage' }
  )
);
"""

files["src/hooks/useAuth.ts"] = """import { useQuery } from '@tanstack/react-query';
import { getMe } from '../api/auth';
import { useAuthStore } from '../store/authStore';
import { useEffect } from 'react';

export const useAuth = () => {
  const { token, logout, setUser, isAuthenticated, user } = useAuthStore();

  const { data, error, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: getMe,
    enabled: !!token,
  });

  useEffect(() => {
    if (data) setUser(data);
    if (error) logout();
  }, [data, error, logout, setUser]);

  return { user, isAuthenticated, isLoading };
};
"""

files["src/hooks/useChat.ts"] = """import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { sendMessage, getConversations, getConversation } from '../api/chat';

export const useChat = (conversationId?: string) => {
  const queryClient = useQueryClient();

  const sendMsgMutation = useMutation({
    mutationFn: sendMessage,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      if (conversationId) {
        queryClient.invalidateQueries({ queryKey: ['conversation', conversationId] });
      }
    },
  });

  return { sendMsgMutation };
};
"""

files["src/utils/constants.ts"] = """export const JURISDICTIONS = [
  { id: 'INDIA', label: 'India', flag: '🇮🇳' },
  { id: 'INTERNATIONAL', label: 'International', flag: '🌍' }
];
"""

files["src/utils/helpers.ts"] = """import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString();
}

export function truncateText(text: string, length: number) {
  return text.length > length ? text.substring(0, length) + '...' : text;
}
"""

files["src/components/layout/AppLayout.tsx"] = """import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import DisclaimerBanner from '../common/DisclaimerBanner';

export default function AppLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
      <div className="flex flex-col flex-1 w-full overflow-hidden">
        <Header toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-auto bg-background p-4 md:p-6 relative">
          <Outlet />
        </main>
        <DisclaimerBanner />
      </div>
    </div>
  );
}
"""

files["src/components/layout/Sidebar.tsx"] = """import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Tags, ShieldAlert, FileText, Search, Library, CheckSquare, Users, Settings, X } from 'lucide-react';
import { cn } from '../../utils/helpers';
import { useAuthStore } from '../../store/authStore';

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'AI Assistant', path: '/chat', icon: MessageSquare },
  { name: 'Classification', path: '/classify', icon: Tags },
  { name: 'IP Assessment', path: '/ip-assessment', icon: ShieldAlert },
  { name: 'ABS Compliance', path: '/abs', icon: FileText },
  { name: 'TK Search', path: '/tk', icon: Search },
  { name: 'Sources', path: '/sources', icon: Library },
  { name: 'Assessments', path: '/assessments', icon: CheckSquare },
  { name: 'Human Review', path: '/review', icon: Users },
];

export default function Sidebar({ isOpen, setIsOpen }: { isOpen: boolean, setIsOpen: (val: boolean) => void }) {
  const user = useAuthStore(s => s.user);
  const items = user?.role === 'admin' ? [...navItems, { name: 'Admin', path: '/admin', icon: Settings }] : navItems;

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && <div className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" onClick={() => setIsOpen(false)} />}
      <div className={cn("fixed inset-y-0 left-0 z-50 w-64 bg-primary text-white transition-transform duration-300 md:relative md:translate-x-0", isOpen ? "translate-x-0" : "-translate-x-full")}>
        <div className="flex items-center justify-between h-16 px-4 border-b border-white/10">
          <span className="font-bold text-lg text-secondary">AyurLegal AI</span>
          <button className="md:hidden text-white" onClick={() => setIsOpen(false)}><X size={20} /></button>
        </div>
        <nav className="p-4 space-y-2">
          {items.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => cn("flex items-center px-4 py-2.5 rounded-md transition-colors", isActive ? "bg-white/10 text-secondary font-medium" : "text-gray-300 hover:bg-white/5 hover:text-white")}
              onClick={() => setIsOpen(false)}
            >
              <item.icon className="w-5 h-5 mr-3" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </div>
    </>
  );
}
"""

files["src/components/layout/Header.tsx"] = """import React from 'react';
import { Menu, LogOut, User } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import JurisdictionSelector from '../common/JurisdictionSelector';

export default function Header({ toggleSidebar }: { toggleSidebar: () => void }) {
  const logout = useAuthStore(s => s.logout);
  return (
    <header className="h-16 bg-surface border-b border-gray-200 flex items-center justify-between px-4 z-10 shrink-0">
      <div className="flex items-center gap-4">
        <button onClick={toggleSidebar} className="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-md"><Menu size={20} /></button>
        <h1 className="font-bold text-primary hidden md:block">IPR & Regulatory Assistant</h1>
      </div>
      <div className="flex items-center gap-4">
        <JurisdictionSelector />
        <div className="flex items-center gap-3 border-l pl-4">
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary"><User size={16} /></div>
          <button onClick={logout} className="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"><LogOut size={18} /></button>
        </div>
      </div>
    </header>
  );
}
"""

files["src/components/common/JurisdictionSelector.tsx"] = """import React, { useState } from 'react';
import { JURISDICTIONS } from '../../utils/constants';

export default function JurisdictionSelector() {
  const [selected, setSelected] = useState(JURISDICTIONS[0]);
  return (
    <div className="flex items-center bg-gray-50 border border-gray-200 rounded-lg p-1">
      {JURISDICTIONS.map(j => (
        <button
          key={j.id}
          onClick={() => setSelected(j)}
          className={`px-3 py-1.5 text-sm font-medium rounded-md flex items-center gap-2 transition-colors ${selected.id === j.id ? 'bg-white shadow-sm text-primary border border-gray-200' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'}`}
        >
          <span>{j.flag}</span>
          <span className="hidden sm:inline">{j.label}</span>
        </button>
      ))}
    </div>
  );
}
"""

files["src/components/common/ConfidenceBadge.tsx"] = """import React from 'react';
import { ConfidenceLevel } from '../../types';

export default function ConfidenceBadge({ level }: { level: ConfidenceLevel }) {
  const colors = {
    HIGH: 'bg-green-100 text-green-800 border-green-200',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    LOW: 'bg-red-100 text-red-800 border-red-200',
  };
  const icon = { HIGH: '🟢', MEDIUM: '🟡', LOW: '🔴' };
  
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${colors[level]}`} title={`${level} Confidence`}>
      {icon[level]} {level} CONFIDENCE
    </span>
  );
}
"""

files["src/components/common/DisclaimerBanner.tsx"] = """import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function DisclaimerBanner() {
  return (
    <div className="bg-amber-50 border-t border-amber-200 p-2 text-center text-xs text-amber-800 flex items-center justify-center gap-2 shrink-0">
      <AlertCircle size={14} />
      This information is for informational purposes only and does not constitute legal advice.
    </div>
  );
}
"""

files["src/components/common/LoadingSpinner.tsx"] = """import React from 'react';
export default function LoadingSpinner() {
  return <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>;
}
"""

files["src/components/common/ErrorBoundary.tsx"] = """import React, { Component, ErrorInfo, ReactNode } from 'react';
export default class ErrorBoundary extends Component<{children: ReactNode}, {hasError: boolean}> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, errorInfo: ErrorInfo) { console.error('Error caught by boundary:', error, errorInfo); }
  render() {
    if (this.state.hasError) return <div className="p-4 text-red-600">Something went wrong. Please refresh the page.</div>;
    return this.props.children;
  }
}
"""

files["src/components/chat/ChatInterface.tsx"] = """import React, { useState } from 'react';
import { Send } from 'lucide-react';
import MessageBubble from './MessageBubble';
import { Message } from '../../types';

export default function ChatInterface() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I am your Ayurvedic IPR & Regulatory Assistant. How can I help you today?',
      timestamp: new Date().toISOString()
    }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMsg: Message = { id: Date.now().toString(), role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, newMsg]);
    setInput('');
    setLoading(true);
    
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Based on the provided information, the formulation would be classified under Section 3(a) of the Drugs and Cosmetics Act.',
        jurisdiction: 'INDIA',
        confidence: 'HIGH',
        citations: [{ id: 'c1', title: 'Drugs and Cosmetics Act, 1940', authority: 'Ministry of Ayush', passage: 'Section 3(a) defines...' }],
        timestamp: new Date().toISOString()
      }]);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => <MessageBubble key={msg.id} message={msg} />)}
        {loading && <div className="text-gray-500 italic text-sm p-4 bg-gray-50 rounded-lg inline-block">Assistant is typing...</div>}
      </div>
      <div className="p-4 border-t bg-gray-50">
        <div className="relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
            placeholder="Ask an Ayurvedic IPR & Regulatory Question..."
            className="w-full resize-none rounded-lg border-gray-300 pr-12 p-3 focus:ring-primary focus:border-primary shadow-sm"
            rows={2}
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="absolute bottom-3 right-3 p-2 bg-primary text-white rounded-md hover:bg-primary/90 disabled:opacity-50"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
"""

files["src/components/chat/MessageBubble.tsx"] = """import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Message } from '../../types';
import ConfidenceBadge from '../common/ConfidenceBadge';
import CitationCard from './CitationCard';

export default function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';
  
  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="bg-primary text-white p-3 rounded-2xl rounded-tr-sm max-w-[80%]">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="bg-surface border border-gray-200 p-4 rounded-2xl rounded-tl-sm max-w-[90%] shadow-sm w-full space-y-4">
        <div className="flex items-center justify-between border-b pb-2">
          <div className="flex items-center gap-2">
            {message.jurisdiction === 'INDIA' ? '🇮🇳' : '🌍'}
            <span className="text-xs font-semibold text-gray-500">{message.jurisdiction || 'GENERAL'}</span>
          </div>
          {message.confidence && <ConfidenceBadge level={message.confidence} />}
        </div>
        
        <div className="prose prose-sm max-w-none text-gray-800">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {message.citations && message.citations.length > 0 && (
          <div className="border-t pt-3 mt-3">
            <h4 className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wider">Sources</h4>
            <div className="space-y-2">
              {message.citations.map(c => <CitationCard key={c.id} citation={c} />)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
"""

files["src/components/chat/CitationCard.tsx"] = """import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, BookOpen } from 'lucide-react';
import { Citation } from '../../types';

export default function CitationCard({ citation }: { citation: Citation }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="border border-gray-200 rounded-md bg-gray-50 overflow-hidden text-sm">
      <div 
        className="p-2.5 flex items-center justify-between cursor-pointer hover:bg-gray-100 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2 overflow-hidden">
          <BookOpen size={16} className="text-secondary shrink-0" />
          <span className="font-medium text-gray-700 truncate">{citation.title}</span>
          <span className="text-xs text-gray-500 shrink-0 px-2 py-0.5 bg-gray-200 rounded-full">{citation.authority}</span>
        </div>
        {expanded ? <ChevronUp size={16} className="text-gray-400" /> : <ChevronDown size={16} className="text-gray-400" />}
      </div>
      {expanded && (
        <div className="p-3 bg-white border-t border-gray-200 text-gray-600 text-xs leading-relaxed space-y-2">
          <div className="pl-2 border-l-2 border-secondary italic">{citation.passage}</div>
          {citation.url && (
            <a href={citation.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-primary hover:underline font-medium">
              View official source <ExternalLink size={12} />
            </a>
          )}
        </div>
      )}
    </div>
  );
}
"""

files["src/components/chat/SourceReference.tsx"] = """import React from 'react';
export default function SourceReference() {
  return <span></span>; // Placeholder if needed
}
"""

files["src/pages/Dashboard.tsx"] = """import React from 'react';
import { Link } from 'react-router-dom';
import { MessageSquare, Tags, ShieldAlert, FileText, Search } from 'lucide-react';

const features = [
  { title: 'AI Assistant', desc: 'Ask complex regulatory questions', icon: MessageSquare, path: '/chat' },
  { title: 'Classification', desc: 'Classify ayurvedic formulations', icon: Tags, path: '/classify' },
  { title: 'IP Assessment', desc: 'Check patentability & novelty', icon: ShieldAlert, path: '/ip-assessment' },
  { title: 'ABS Compliance', desc: 'Verify biological diversity acts', icon: FileText, path: '/abs' },
  { title: 'TK Search', desc: 'Search Traditional Knowledge databases', icon: Search, path: '/tk' },
];

export default function Dashboard() {
  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div className="text-center space-y-4 py-8">
        <h1 className="text-3xl md:text-4xl font-bold text-primary">Ayurvedic IPR & Regulatory AI</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">Navigate complex Ayurvedic regulatory frameworks, classify products, and ensure IP compliance with AI-powered insights.</p>
        <Link to="/chat" className="inline-flex items-center gap-2 bg-secondary hover:bg-secondary/90 text-white px-6 py-3 rounded-lg font-medium shadow-sm transition-all mt-4">
          <MessageSquare size={20} /> Ask a Question
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {features.map(f => (
          <Link key={f.path} to={f.path} className="group bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md hover:border-primary/30 transition-all flex flex-col items-center text-center space-y-3">
            <div className="p-3 bg-primary/5 text-primary rounded-full group-hover:bg-primary group-hover:text-white transition-colors">
              <f.icon size={24} />
            </div>
            <h3 className="font-semibold text-gray-900">{f.title}</h3>
            <p className="text-sm text-gray-500">{f.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
"""

files["src/pages/Chat.tsx"] = """import React from 'react';
import ChatInterface from '../components/chat/ChatInterface';

export default function Chat() {
  return (
    <div className="h-full max-w-4xl mx-auto flex flex-col">
      <ChatInterface />
    </div>
  );
}
"""

files["src/pages/Classify.tsx"] = """import React from 'react';
export default function Classify() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Formulation Classification (Coming Soon)</h2></div>; }
"""
files["src/pages/IPAssessment.tsx"] = """import React from 'react';
export default function IPAssessment() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>IP Assessment (Coming Soon)</h2></div>; }
"""
files["src/pages/ABSCompliance.tsx"] = """import React from 'react';
export default function ABSCompliance() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>ABS Compliance (Coming Soon)</h2></div>; }
"""
files["src/pages/TKSearch.tsx"] = """import React from 'react';
export default function TKSearch() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>TK Search (Coming Soon)</h2></div>; }
"""
files["src/pages/Sources.tsx"] = """import React from 'react';
export default function Sources() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Knowledge Base Sources (Coming Soon)</h2></div>; }
"""
files["src/pages/Assessments.tsx"] = """import React from 'react';
export default function Assessments() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Saved Assessments (Coming Soon)</h2></div>; }
"""
files["src/pages/HumanReview.tsx"] = """import React from 'react';
export default function HumanReview() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Human Review Dashboard (Coming Soon)</h2></div>; }
"""
files["src/pages/AdminDashboard.tsx"] = """import React from 'react';
export default function AdminDashboard() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Admin Dashboard (Coming Soon)</h2></div>; }
"""
files["src/pages/Settings.tsx"] = """import React from 'react';
export default function Settings() { return <div className="p-6 bg-white rounded-xl shadow-sm border border-gray-200"><h2>Settings (Coming Soon)</h2></div>; }
"""

files["src/pages/Login.tsx"] = """import React from 'react';
import { useAuthStore } from '../store/authStore';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const login = useAuthStore(s => s.login);
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    login({ id: '1', email: 'user@example.com', name: 'Demo User', role: 'user' }, 'fake-token');
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-200 w-full max-w-md">
        <h2 className="text-2xl font-bold text-primary mb-6 text-center">Login to AyurLegal AI</h2>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" required className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input type="password" required className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary" />
          </div>
          <button type="submit" className="w-full bg-primary text-white py-2.5 rounded-lg font-medium hover:bg-primary/90 transition-colors">Sign In</button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account? <Link to="/register" className="text-secondary hover:underline">Register</Link>
        </p>
      </div>
    </div>
  );
}
"""

files["src/pages/Register.tsx"] = """import React from 'react';
import { Link } from 'react-router-dom';

export default function Register() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="bg-white p-8 rounded-xl shadow-lg border border-gray-200 w-full max-w-md">
        <h2 className="text-2xl font-bold text-primary mb-6 text-center">Create an Account</h2>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
            <input type="text" required className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" required className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input type="password" required className="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary" />
          </div>
          <button type="submit" className="w-full bg-primary text-white py-2.5 rounded-lg font-medium hover:bg-primary/90 transition-colors">Register</button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account? <Link to="/login" className="text-secondary hover:underline">Login</Link>
        </p>
      </div>
    </div>
  );
}
"""

files["public/locales/en/translation.json"] = """{
  "welcome": "Welcome to Ayurvedic IPR & Regulatory AI"
}"""
files["public/locales/hi/translation.json"] = """{
  "welcome": "आयुर्वेदिक आईपीआर और विनियामक एआई में आपका स्वागत है"
}"""
files["public/locales/kn/translation.json"] = """{
  "welcome": "ಆಯುರ್ವೇದ ಐಪಿಆರ್ ಮತ್ತು ನಿಯಂತ್ರಕ ಎಐಗೆ ಸುಸ್ವಾಗತ"
}"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path.replace("/", os.sep))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Files generated successfully.")
