import { apiClient } from './client';

export interface ABSChecklistItem {
  question: string;
  user_answer: string;
  relevant_provision: string;
  why_it_matters: string;
  required_action: string;
  authority: string;
  confidence: string;
  needs_human_review: boolean;
}

export interface ABSEvaluationRequest {
  involves_bio_resource: boolean;
  source_is_india: boolean;
  entity_type: string;
  purpose: string;
  is_cultivated: boolean;
  is_ayush_practitioner: boolean;
  is_codified_tk: boolean;
  applies_for_ipr: boolean;
  plant_names?: string[];
  jurisdiction?: string;
}

export interface ABSEvaluationResponse {
  id?: string;
  overall_status: string;
  summary: string;
  required_forms: string[];
  benefit_sharing_applicable: boolean;
  estimated_benefit_sharing_rate?: string;
  checklist: ABSChecklistItem[];
  created_at?: string;
}

export const absApi = {
  evaluate: async (data: ABSEvaluationRequest): Promise<ABSEvaluationResponse> => {
    const response = await apiClient.post<ABSEvaluationResponse>('/abs/evaluate', data);
    return response.data;
  },
  getAssessment: async (id: string): Promise<ABSEvaluationResponse> => {
    const response = await apiClient.get<ABSEvaluationResponse>(`/abs/${id}`);
    return response.data;
  },
};
