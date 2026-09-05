import { apiClient } from './client';
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types';

export const authApi = {
  login: async (data: LoginRequest) => {
    const response = await apiClient.post<TokenResponse>('/auth/login', data);
    return response.data;
  },
  register: async (data: RegisterRequest) => {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },
  getMe: async () => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
  refreshToken: async () => {
    const response = await apiClient.post<TokenResponse>('/auth/refresh');
    return response.data;
  },
};
