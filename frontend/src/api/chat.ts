import { apiClient } from './client';
import type { ChatMessageRequest, ChatMessageResponse, Conversation } from '../types';

export const chatApi = {
  sendMessage: async (data: ChatMessageRequest) => {
    const response = await apiClient.post<ChatMessageResponse>('/chat', data);
    return response.data;
  },
  getConversations: async () => {
    const response = await apiClient.get<Conversation[]>('/chat/conversations');
    return response.data;
  },
  getConversation: async (id: string) => {
    const response = await apiClient.get<Conversation>(`/chat/conversations/${id}`);
    return response.data;
  },
  deleteConversation: async (id: string) => {
    const response = await apiClient.delete<{ status: string }>(`/chat/conversations/${id}`);
    return response.data;
  },
};
