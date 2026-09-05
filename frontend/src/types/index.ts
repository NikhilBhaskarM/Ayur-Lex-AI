export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'USER' | 'FACILITATOR' | 'ADMIN';
  preferred_language: string;
  is_active: boolean;
  created_at?: string;
}

export interface LoginRequest {
  email: string;
  password?: string;
}

export interface RegisterRequest {
  email: string;
  full_name: string;
  password?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
}

export interface Citation {
  chunk_id?: string;
  source_title: string;
  authority?: string;
  section?: string;
  rule?: string;
  article?: string;
  version_date?: string;
  official_url?: string;
  retrieved_at?: string;
  relevant_passage?: string;
}

export interface ConfidenceResponse {
  level: 'HIGH' | 'MEDIUM' | 'LOW';
  score: number;
  factors?: Record<string, number | string>;
}

export interface ChatMessageRequest {
  message: string;
  conversation_id?: string;
  jurisdiction?: string;
}

export interface ChatMessageResponse {
  conversation_id: string;
  message_id: string;
  answer: string;
  citations: Citation[];
  confidence: ConfidenceResponse;
  jurisdiction: string;
  requires_clarification: boolean;
  clarification_questions: string[];
  disclaimer: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  confidence?: ConfidenceResponse;
  jurisdiction?: string;
  clarification_questions?: string[];
  disclaimer?: string;
  timestamp?: string;
}

export interface Conversation {
  id: string;
  title?: string;
  jurisdiction?: string;
  status: string;
  created_at: string;
  updated_at?: string;
  message_count?: number;
  messages?: Message[];
}

export type JurisdictionType = 'India' | 'International' | string;

export interface Assessment {
  id: string;
  assessment_type: string;
  jurisdiction: string;
  formulation_data?: Record<string, any>;
  classification_result?: Record<string, any>;
  ip_assessment?: Record<string, any>;
  abs_assessment?: Record<string, any>;
  sources_used?: any[];
  confidence?: string;
  status: string;
  created_at: string;
}

export interface ClassificationRequest {
  formulation_name: string;
  description: string;
  ingredients: string[];
  intended_use: string;
  is_classical_text_based?: boolean;
  has_been_modified?: boolean;
  marketed_as?: string;
  jurisdiction?: string;
  biological_resources_involved?: boolean;
}

export interface ClassificationResponse {
  classification: string;
  reasoning: string;
  evidence: string[];
  confidence: ConfidenceResponse;
  missing_information: string[];
  regulatory_implications: string[];
  ip_implications: string[];
  abs_implications: string[];
  recommended_next_steps: string[];
  disclaimer: string;
}

export interface Source {
  id: string;
  name: string;
  authority: string;
  source_type: string;
  url: string;
  jurisdiction: string;
  country?: string;
  authority_level: number;
  crawl_frequency: string;
  is_active: boolean;
  last_crawled?: string;
  created_at?: string;
}

export interface AdminStatsResponse {
  total_documents: number;
  total_sources: number;
  total_users: number;
  total_conversations: number;
  total_assessments: number;
  active_ingestion_jobs: number;
  recent_ingestion_jobs?: any[];
}

export interface HumanReview {
  id: string;
  status: 'new' | 'assigned' | 'in_review' | 'completed' | 'needs_info';
  user_question: string;
  ai_assessment?: Record<string, any>;
  facilitator_notes?: string;
  final_guidance?: string;
  priority?: string;
  created_at: string;
}
