import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { chatApi } from '../api/chat';
import type { ChatMessageRequest } from '../types';

export const useChat = (conversationId?: string) => {
  const queryClient = useQueryClient();

  const conversationsQuery = useQuery({
    queryKey: ['conversations'],
    queryFn: chatApi.getConversations,
  });

  const currentConversationQuery = useQuery({
    queryKey: ['conversation', conversationId],
    queryFn: () => (conversationId ? chatApi.getConversation(conversationId) : null),
    enabled: !!conversationId,
  });

  const sendMessageMutation = useMutation({
    mutationFn: (data: ChatMessageRequest) => chatApi.sendMessage(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
      if (data.conversation_id) {
        queryClient.invalidateQueries({ queryKey: ['conversation', data.conversation_id] });
      }
    },
  });

  return {
    conversations: conversationsQuery.data,
    currentConversation: currentConversationQuery.data,
    isLoading: conversationsQuery.isLoading || currentConversationQuery.isLoading,
    sendMessage: sendMessageMutation.mutate,
    isSending: sendMessageMutation.isPending,
  };
};
