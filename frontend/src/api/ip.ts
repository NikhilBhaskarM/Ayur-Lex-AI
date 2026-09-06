import { apiClient } from './client';

export interface IPAssessmentRequest {
  asset_id: string;
  formulation_name?: string;
  description?: string;
  ingredients?: string[];
  synergy_evidence?: string;
  biological_origin?: string;
  jurisdiction?: string;
}

export interface IPAssessmentResponse {
  id?: string;
  asset_id: string;
  title: string;
  ip_type: string;
  governing_act: string;
  key_sections: string;
  statutory_prerequisites: string[];
  ayurvedic_specific_nuances: string[];
  exclusion_risks: string[];
  action_steps: string[];
  rag_guidance?: string;
  citations?: Array<{
    source_title: string;
    section?: string;
    official_url?: string;
  }>;
  confidence?: {
    level: string;
    score: number;
    factors?: Record<string, any>;
  };
  created_at?: string;
}

export const ipApi = {
  evaluate: async (data: IPAssessmentRequest): Promise<IPAssessmentResponse> => {
    const response = await apiClient.post<IPAssessmentResponse>('/ip-assessment/evaluate', data);
    return response.data;
  },
  getAssessment: async (id: string): Promise<IPAssessmentResponse> => {
    const response = await apiClient.get<IPAssessmentResponse>(`/ip-assessment/${id}`);
    return response.data;
  },
};
