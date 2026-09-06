import { apiClient } from './client';

export interface HumanReviewItem {
  id: string;
  assessment_id?: string;
  user_id: string;
  facilitator_id?: string;
  status: 'new' | 'assigned' | 'in_review' | 'completed' | 'needs_info';
  topic?: string;
  user_question: string;
  ai_assessment?: Record<string, any>;
  facilitator_notes?: string;
  final_guidance?: string;
  priority: 'normal' | 'urgent' | string;
  assigned_at?: string;
  completed_at?: string;
  created_at: string;
}

export interface HumanReviewCreateRequest {
  topic: string;
  user_question: string;
  priority?: string;
  assessment_id?: string;
  ai_assessment?: Record<string, any>;
}

export interface HumanReviewUpdateRequest {
  status?: string;
  facilitator_notes?: string;
  final_guidance?: string;
  priority?: string;
  facilitator_id?: string;
}

export const humanReviewApi = {
  getReviews: async (status?: string): Promise<HumanReviewItem[]> => {
    const params = status ? { status } : {};
    const response = await apiClient.get<HumanReviewItem[]>('/human-review', { params });
    return response.data;
  },
  getReview: async (id: string): Promise<HumanReviewItem> => {
    const response = await apiClient.get<HumanReviewItem>(`/human-review/${id}`);
    return response.data;
  },
  createReview: async (data: HumanReviewCreateRequest): Promise<HumanReviewItem> => {
    const response = await apiClient.post<HumanReviewItem>('/human-review', data);
    return response.data;
  },
  updateReview: async (id: string, data: HumanReviewUpdateRequest): Promise<HumanReviewItem> => {
    const response = await apiClient.patch<HumanReviewItem>(`/human-review/${id}`, data);
    return response.data;
  },
};
