import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  jurisdiction: string;
  language: string;
  login: (user: User, token: string) => void;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  setJurisdiction: (jurisdiction: string) => void;
  setLanguage: (language: string) => void;
  updateUser: (partialUser: Partial<User>) => void;
  llmProvider: string;
  llmModel: string;
  llmApiKey: string;
  llmBaseUrl: string;
  setLLMConfig: (config: {
    provider?: string;
    model?: string;
    apiKey?: string;
    baseUrl?: string;
  }) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      jurisdiction: 'India',
      language: 'en',
      llmProvider: 'ollama',
      llmModel: 'llama3.1:8b',
      llmApiKey: '',
      llmBaseUrl: '',
      login: (user: User, token: string) =>
        set({ user, token, isAuthenticated: true, language: user.preferred_language || 'en' }),
      setAuth: (user: User, token: string) =>
        set({ user, token, isAuthenticated: true, language: user.preferred_language || 'en' }),
      logout: () =>
        set({ user: null, token: null, isAuthenticated: false }),
      setJurisdiction: (jurisdiction: string) =>
        set({ jurisdiction }),
      setLanguage: (language: string) =>
        set({ language }),
      updateUser: (partialUser: Partial<User>) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...partialUser } : null,
          language: partialUser.preferred_language || state.language,
        })),
      setLLMConfig: (config) =>
        set((state) => ({
          llmProvider: config.provider ?? state.llmProvider,
          llmModel: config.model ?? state.llmModel,
          llmApiKey: config.apiKey ?? state.llmApiKey,
          llmBaseUrl: config.baseUrl ?? state.llmBaseUrl,
        })),
    }),
    {
      name: 'ayurveda-auth-storage',
    }
  )
);
