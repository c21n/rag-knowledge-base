/**
 * Chat API service
 * Handles all chat-related API calls
 */
import type { ChatRequest, ChatResponse } from '../types/chat';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Send a chat message to the backend
 * @param request - Chat request payload
 * @returns Chat response with answer and sources
 */
export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Send a streaming chat message
 * @param request - Chat request payload
 * @param onChunk - Callback for each chunk received
 * @param onComplete - Callback when streaming completes
 * @param onError - Callback when an error occurs
 */
export async function sendStreamingChatMessage(
  request: ChatRequest,
  onChunk: (chunk: string) => void,
  onComplete: (fullResponse: ChatResponse) => void,
  onError: (error: Error) => void
): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullAnswer = '';

    if (!reader) {
      throw new Error('No response body');
    }

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') {
            // Stream complete
            onComplete({
              answer: fullAnswer,
              sources: [],
              response_time: 0,
              retrieved_count: 0,
            });
            return;
          }
          try {
            const parsed = JSON.parse(data);
            if (parsed.content) {
              fullAnswer += parsed.content;
              onChunk(parsed.content);
            }
          } catch {
            // Ignore parse errors for non-JSON data
          }
        }
      }
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
  }
}
