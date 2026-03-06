import { useState, useCallback } from 'react';
import type { Conversation, ConversationPreview, FeedbackRequest } from '../types/conversation';
import { conversationApi } from '../services/conversationApi';

export function useConversations() {
  const [conversations] = useState<ConversationPreview[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const loadConversation = useCallback(async (sessionId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const conversation = await conversationApi.getConversationHistory(sessionId);
      setCurrentConversation(conversation);
      return conversation;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);
  
  const submitFeedback = useCallback(async (feedback: FeedbackRequest) => {
    setError(null);
    
    try {
      const response = await conversationApi.submitFeedback(feedback);
      return response;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit feedback');
      throw err;
    }
  }, []);
  
  const clearCurrentConversation = useCallback(() => {
    setCurrentConversation(null);
  }, []);
  
  return {
    conversations,
    currentConversation,
    loading,
    error,
    loadConversation,
    submitFeedback,
    clearCurrentConversation,
  };
}
