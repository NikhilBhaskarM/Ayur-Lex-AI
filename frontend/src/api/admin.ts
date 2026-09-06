import { apiClient } from './client';

export interface IngestionJob {
  id: string;
  source_id: string;
  source_name?: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  job_type: string;
  documents_found: number;
  documents_processed: number;
  documents_failed: number;
  chunks_created: number;
  started_at?: string;
  completed_at?: string;
}

export interface IngestionLog {
  id: string;
  job_id: string;
  document_id?: string;
  level: string;
  message: string;
  details?: Record<string, any>;
  created_at: string;
}

export interface CrawlJobDetail extends IngestionJob {
  errors?: any[];
  logs: IngestionLog[];
}

export interface AdminStats {
  total_documents: number;
  total_sources: number;
  total_users: number;
  total_conversations: number;
  total_assessments: number;
  active_ingestion_jobs: number;
  recent_ingestion_jobs: IngestionJob[];
}

export const adminApi = {
  getStats: async (): Promise<AdminStats> => {
    const response = await apiClient.get<AdminStats>('/admin/stats');
    return response.data;
  },
  getUsers: async () => {
    const response = await apiClient.get('/admin/users');
    return response.data;
  },
  getIngestionStatus: async (limit: number = 20): Promise<IngestionJob[]> => {
    const response = await apiClient.get<IngestionJob[]>(`/admin/ingestion-status?limit=${limit}`);
    return response.data;
  },
  getJobDetail: async (jobId: string): Promise<CrawlJobDetail> => {
    const response = await apiClient.get<CrawlJobDetail>(`/admin/ingestion-status/${jobId}`);
    return response.data;
  },
  triggerIngestion: async (sourceId: string, forceReindex: boolean = false) => {
    const response = await apiClient.post('/admin/ingest', {
      source_id: sourceId,
      force_reindex: forceReindex,
    });
    return response.data;
  },
  crawlAll: async (forceReindex: boolean = false) => {
    const response = await apiClient.post('/admin/crawl-all', {
      force_reindex: forceReindex,
    });
    return response.data;
  },
};
