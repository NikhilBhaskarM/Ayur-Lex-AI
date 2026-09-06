import { apiClient } from './client';
import type { LoginRequest, RegisterRequest, TokenResponse, User, UserUpdateRequest } from '../types';

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
  updateProfile: async (data: UserUpdateRequest) => {
    const response = await apiClient.patch<User>('/auth/me', data);
    return response.data;
  },
  refreshToken: async () => {
    const response = await apiClient.post<TokenResponse>('/auth/refresh');
    return response.data;
  },
};
