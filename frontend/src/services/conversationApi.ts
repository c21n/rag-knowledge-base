import type { 
  Conversation, 
  FeedbackRequest, 
  FeedbackResponse,
  ConversationPreview 
} from '../types/conversation';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export const conversationApi = {
  async getConversationHistory(sessionId: string): Promise<Conversation> {
    const response = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`);
    
    if (!response.ok) {
      throw new Error('Failed to load conversation history');
    }
    
    return response.json();
  },
  
  async submitFeedback(feedback: FeedbackRequest): Promise<FeedbackResponse> {
    const response = await fetch(`${API_BASE_URL}/chat/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedback),
    });
    
    if (!response.ok) {
      throw new Error('Failed to submit feedback');
    }
    
    return response.json();
  },
  
  // Mock function for listing conversations (if backend doesn't have this endpoint)
  async listConversations(): Promise<ConversationPreview[]> {
    // For now, return empty array or mock data
    // In real implementation, this would call GET /api/conversations
    return [];
  }
};
