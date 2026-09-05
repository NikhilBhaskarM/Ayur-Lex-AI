import { apiClient } from './client';

export const adminApi = {
  getStats: async () => {
    const response = await apiClient.get('/admin/stats');
    return response.data;
  },
  getUsers: async () => {
    const response = await apiClient.get('/admin/users');
    return response.data;
  },
  getIngestionStatus: async () => {
    const response = await apiClient.get('/admin/ingestion/status');
    return response.data;
  },
  triggerIngestion: async () => {
    const response = await apiClient.post('/admin/ingestion/trigger');
    return response.data;
  }
};
