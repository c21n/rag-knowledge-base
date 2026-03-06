export interface Conversation {
  session_id: string;
  messages: ConversationMessage[];
  created_at: string;
  updated_at: string;
  role_id?: string;
  role_name?: string;
}

export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  feedback?: Feedback;
}

export interface Feedback {
  id: string;
  message_id: string;
  rating: 'thumbs_up' | 'thumbs_down';
  comment?: string;
  created_at: string;
}

export interface FeedbackRequest {
  message_id: string;
  rating: 'thumbs_up' | 'thumbs_down';
  comment?: string;
}

export interface FeedbackResponse {
  id: string;
  message_id: string;
  rating: string;
  created_at: string;
}

export interface ConversationPreview {
  session_id: string;
  preview: string;
  message_count: number;
  last_updated: string;
  role_name?: string;
}
