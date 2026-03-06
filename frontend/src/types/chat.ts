/**
 * Chat type definitions
 * Following the backend chat API structure
 */

/**
 * Source citation from retrieved documents
 */
export interface SourceCitation {
  /** Document ID that the chunk belongs to */
  document_id: string;
  /** Index of the chunk within the document */
  chunk_index: number;
  /** Preview of the chunk content */
  content_preview: string;
  /** Relevance score (0-1) */
  score: number;
}

/**
 * Chat message representing a single interaction
 */
export interface ChatMessage {
  /** Unique message ID */
  id: string;
  /** Message role: 'user' or 'assistant' */
  role: 'user' | 'assistant';
  /** Message content */
  content: string;
  /** ISO timestamp */
  timestamp: string;
  /** Source citations for assistant messages */
  sources?: SourceCitation[];
}

/**
 * Request payload for chat API
 */
export interface ChatRequest {
  /** User query text */
  query: string;
  /** Optional role ID for customized system prompt */
  role_id?: string;
  /** Optional session ID for conversation continuity */
  session_id?: string;
  /** Number of documents to retrieve (default: 4) */
  top_k?: number;
}

/**
 * Response from chat API
 */
export interface ChatResponse {
  /** AI-generated answer */
  answer: string;
  /** Source citations used to generate the answer */
  sources: SourceCitation[];
  /** Response time in seconds */
  response_time: number;
  /** Number of documents retrieved */
  retrieved_count: number;
  /** Session ID for conversation continuity */
  session_id?: string;
}
/**
 * Chat session for conversation management
 */
export interface ChatSession {
  /** Unique session ID */
  id: string;
  /** Session title */
  title: string;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string;
  /** Message count in session */
  message_count: number;
}

/**
 * Chat state for useChat hook
 */
export interface ChatState {
  /** Array of chat messages */
  messages: ChatMessage[];
  /** Whether a message is being sent */
  loading: boolean;
  /** Error message if any */
  error: string | null;
  /** Current session ID */
  sessionId: string | null;
}

/**
 * Hook return type for useChat
 */
export interface UseChatReturn extends ChatState {
  /** Send a message */
  sendMessage: (content: string) => Promise<void>;
  /** Clear all messages */
  clearMessages: () => void;
  /** Clear error state */
  clearError: () => void;
}
