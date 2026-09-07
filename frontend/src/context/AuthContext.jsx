import React, { createContext, useContext, useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token') || null);
  const [role, setRole] = useState(() => localStorage.getItem('role') || null);
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const isAuthenticated = Boolean(token);

  // Sync token to Zustand auth store for backward compatibility across all existing pages
  useEffect(() => {
    if (token && role && user) {
      useAuthStore.getState().setAuth(
        {
          id: user.username || 'user-id',
          email: user.email || `${user.username}@ayurlex.ai`,
          full_name: user.full_name || user.username,
          role: role.toUpperCase(),
          preferred_language: 'en',
          is_active: true,
        },
        token
      );
    }
  }, [token, role, user]);

  const login = async (username, password) => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        let errorDetail = 'Invalid username or password';
        try {
          const errData = await response.json();
          if (errData?.detail) errorDetail = errData.detail;
        } catch {
          // fallback to default error message
        }
        throw new Error(errorDetail);
      }

      const data = await response.json();
      const accessToken = data.access_token;
      const userRole = (data.role || 'user').toLowerCase();
      const userInfo = {
        username: data.username,
        role: userRole,
        email: data.email || `${data.username}@ayurlex.ai`,
      };

      // Store in localStorage
      localStorage.setItem('token', accessToken);
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('role', userRole);
      localStorage.setItem('user', JSON.stringify(userInfo));

      // Update state
      setToken(accessToken);
      setRole(userRole);
      setUser(userInfo);

      // Sync Zustand store
      useAuthStore.getState().login(
        {
          id: data.username,
          email: userInfo.email,
          full_name: data.username,
          role: userRole.toUpperCase(),
          preferred_language: 'en',
          is_active: true,
        },
        accessToken
      );

      return { success: true, role: userRole, user: userInfo, token: accessToken };
    } catch (err) {
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user');
    setToken(null);
    setRole(null);
    setUser(null);
    useAuthStore.getState().logout();
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        role,
        user,
        isAuthenticated,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
