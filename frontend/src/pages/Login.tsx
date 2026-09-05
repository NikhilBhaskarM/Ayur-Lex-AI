import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/api/auth';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');
    setLoading(true);

    try {
      const tokenData = await authApi.login({ email, password });
      // Fetch user profile with the token
      useAuthStore.getState().setAuth(
        { id: '', email, full_name: 'User', role: 'USER', preferred_language: 'en', is_active: true },
        tokenData.access_token
      );
      
      try {
        const userProfile = await authApi.getMe();
        login(userProfile, tokenData.access_token);
      } catch {
        // Use basic user if me call fails
        login(
          { id: '', email, full_name: email.split('@')[0], role: 'USER', preferred_language: 'en', is_active: true },
          tokenData.access_token
        );
      }

      toast.success('Signed in successfully');
      navigate('/');
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Failed to sign in. Please check your credentials.';
      setErrorMessage(detail);
      toast.error(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="p-3 bg-[#1a365d]/10 rounded-2xl">
            <Shield className="h-10 w-10 text-[#1a365d]" />
          </div>
        </div>
        <h2 className="mt-4 text-center text-2xl sm:text-3xl font-bold text-gray-900">
          Sign in to AyurLegal AI
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Ayurvedic IPR & Regulatory Intelligence Platform
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-sm sm:rounded-xl sm:px-10 border border-gray-200">
          {errorMessage && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg flex items-start gap-2">
              <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <div className="mt-1">
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  placeholder="practitioner@ayurveda.org"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#2c7a7b] focus:border-[#2c7a7b] sm:text-sm"
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="mt-1">
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-[#2c7a7b] focus:border-[#2c7a7b] sm:text-sm"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-[#1a365d] hover:bg-[#0f2342] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#1a365d] disabled:opacity-50 transition-colors"
              >
                {loading ? 'Signing in...' : 'Sign in'}
              </button>
            </div>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">New to the platform?</span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <Link to="/register" className="font-medium text-[#2c7a7b] hover:text-[#235e5f]">
                Create an account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
