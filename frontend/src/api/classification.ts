import { apiClient } from './client';
import type { ClassificationRequest, ClassificationResponse } from '../types';

export const classificationApi = {
  classify: async (data: ClassificationRequest) => {
    const response = await apiClient.post<ClassificationResponse>('/classification', data);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<ClassificationResponse>(`/classification/${id}`);
    return response.data;
  },
};
