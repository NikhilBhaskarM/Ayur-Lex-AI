import { apiClient } from './client';
import type { Source } from '../types';

export const sourcesApi = {
  getSources: async () => {
    const response = await apiClient.get<Source[]>('/sources');
    return response.data;
  },
  getSource: async (id: string) => {
    const response = await apiClient.get<Source>(`/sources/${id}`);
    return response.data;
  }
};
