import { apiClient } from './client';

export interface ClassicalTreatiseCitation {
  treatise: string;
  verse_or_chapter?: string;
  indications: string[];
  sanskrit_sloka?: string;
}

export interface KnownPriorArtCase {
  patent_number: string;
  patent_office: string;
  applicant: string;
  disputed_claims: string;
  outcome: string;
  key_prior_art_cited: string;
}

export interface HerbPriorArtResult {
  herb_name: string;
  sanskrit_name: string;
  botanical_name: string;
  family: string;
  tkrc_class: string;
  classical_treatises: ClassicalTreatiseCitation[];
  famous_revocation_case?: KnownPriorArtCase;
  section_3p_rejection_risk: string;
  defensive_search_guidance: string;
}

export interface TKSearchResponse {
  query: string;
  matched_herbs: HerbPriorArtResult[];
  rag_retrieved_provisions: Array<{
    chunk_id?: string;
    content: string;
    score: number;
    source_title: string;
    section?: string;
    portal_url?: string;
  }>;
  total_matches: number;
  defensive_advice: string;
}

export interface TKSearchRequest {
  query: string;
  herb_name?: string;
  therapeutic_claim?: string;
  jurisdiction?: string;
  top_k?: number;
}

export const tkApi = {
  search: async (data: TKSearchRequest): Promise<TKSearchResponse> => {
    const response = await apiClient.post<TKSearchResponse>('/tk/search', data);
    return response.data;
  },
};
