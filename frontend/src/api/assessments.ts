import { apiClient } from './client';
import type { Assessment } from '../types';

export const assessmentsApi = {
  getAssessments: async (page: number = 1, pageSize: number = 20): Promise<Assessment[]> => {
    const response = await apiClient.get<Assessment[]>('/assessments', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  },
  getAssessment: async (id: string): Promise<Assessment> => {
    const response = await apiClient.get<Assessment>(`/assessments/${id}`);
    return response.data;
  },
};
