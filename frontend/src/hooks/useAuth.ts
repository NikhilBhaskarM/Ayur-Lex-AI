import { useAuthStore } from '../store/authStore';

export const useAuth = () => {
  const { user, token, setAuth, logout, isAuthenticated } = useAuthStore();
  const isAdmin = user?.role === 'ADMIN';

  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    setAuth,
    logout,
  };
};
