import React, { useState, useEffect } from 'react';
import ChatInterface from '../components/chat/ChatInterface';
import { ChatSidebar } from '../components/chat/ChatSidebar';
import { chatApi } from '../api/chat';
import type { Conversation } from '../types';
import toast from 'react-hot-toast';

const Chat: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>(undefined);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  const fetchConversations = async () => {
    setIsLoadingHistory(true);
    try {
      const data = await chatApi.getConversations();
      if (Array.isArray(data)) {
        setConversations(data);
      }
    } catch (err) {
      console.warn('Could not fetch conversations:', err);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const handleSelectConversation = (id: string) => {
    setActiveConversationId(id);
    // On mobile, auto-close sidebar on select
    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  };

  const handleNewChat = () => {
    setActiveConversationId(undefined);
    if (window.innerWidth < 768) {
      setSidebarOpen(false);
    }
  };

  const handleDeleteConversation = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await chatApi.deleteConversation(id);
      setConversations((prev) => prev.filter((c) => c.id !== id));
      if (activeConversationId === id) {
        setActiveConversationId(undefined);
      }
      toast.success('Consultation deleted');
    } catch (err) {
      toast.error('Failed to delete consultation');
    }
  };

  return (
    <div className="flex h-full max-h-[calc(100vh-8rem)] rounded-xl overflow-hidden border border-gray-200 shadow-sm bg-white">
      <ChatSidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
        onDeleteConversation={handleDeleteConversation}
        isOpen={sidebarOpen}
        onToggle={() => setSidebarOpen((prev) => !prev)}
        isLoading={isLoadingHistory}
      />
      <div className="flex-1 min-w-0 flex flex-col h-full">
        <ChatInterface
          activeConversationId={activeConversationId}
          onConversationCreated={(newId) => {
            setActiveConversationId(newId);
            fetchConversations();
          }}
          sidebarOpen={sidebarOpen}
          onToggleSidebar={() => setSidebarOpen((prev) => !prev)}
          onNewChat={handleNewChat}
        />
      </div>
    </div>
  );
};

export default Chat;
