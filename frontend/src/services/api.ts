// Centralized API client with interceptors and error handling
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

export interface ApiError {
  message: string;
  status: number;
  data?: unknown;
}

export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }
  
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: ApiError = {
        message: 'An error occurred',
        status: response.status,
      };
      
      try {
        const data = await response.json();
        error.message = data.detail || data.message || `HTTP ${response.status}`;
        error.data = data;
      } catch {
        error.message = `HTTP ${response.status}: ${response.statusText}`;
      }
      
      throw error;
    }
    
    if (response.status === 204) {
      return undefined as T;
    }
    
    return response.json();
  }
  
  async get<T>(path: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`);
    return this.handleResponse<T>(response);
  }
  
  async post<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return this.handleResponse<T>(response);
  }
  
  async delete<T>(path: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'DELETE',
    });
    return this.handleResponse<T>(response);
  }
  
  async postForm<T>(path: string, formData: FormData): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      body: formData,
    });
    return this.handleResponse<T>(response);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
