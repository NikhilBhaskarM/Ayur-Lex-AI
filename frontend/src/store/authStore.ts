import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  jurisdiction: string;
  login: (user: User, token: string) => void;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  setJurisdiction: (jurisdiction: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: {
        id: 'demo-user',
        email: 'researcher@ayurlex.ai',
        full_name: 'Ayur-Lex Researcher',
        role: 'ADMIN',
        preferred_language: 'en',
        is_active: true,
      },
      token: 'demo-access-token',
      isAuthenticated: true,
      jurisdiction: 'India',

      login: (user: User, token: string) =>
        set({ user, token, isAuthenticated: true }),
      setAuth: (user: User, token: string) =>
        set({ user, token, isAuthenticated: true }),
      logout: () =>
        set({ user: null, token: null, isAuthenticated: false }),
      setJurisdiction: (jurisdiction: string) =>
        set({ jurisdiction }),
    }),
    {
      name: 'ayurveda-auth-storage',
    }
  )
);
