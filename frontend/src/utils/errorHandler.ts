import { message } from 'antd';
import type { ApiError } from '../services/api';

export interface ErrorDetails {
  message: string;
  description?: string;
  action?: string;
}

export function getUserFriendlyMessage(error: unknown): ErrorDetails {
  if (error && typeof error === 'object' && 'status' in error) {
    const apiError = error as ApiError;
    
    switch (apiError.status) {
      case 400:
        return {
          message: 'Invalid request',
          description: apiError.message,
          action: 'Please check your input and try again.',
        };
      case 401:
        return {
          message: 'Authentication required',
          description: 'Your session has expired.',
          action: 'Please refresh the page and try again.',
        };
      case 403:
        return {
          message: 'Access denied',
          description: 'You do not have permission to perform this action.',
          action: 'Please contact your administrator.',
        };
      case 404:
        return {
          message: 'Not found',
          description: 'The requested resource could not be found.',
          action: 'Please check the URL or try again.',
        };
      case 413:
        return {
          message: 'File too large',
          description: 'The uploaded file exceeds the size limit.',
          action: 'Please upload a smaller file (max 50MB).',
        };
      case 429:
        return {
          message: 'Too many requests',
          description: 'Please slow down and try again later.',
          action: 'Wait a moment before making another request.',
        };
      case 500:
      case 502:
      case 503:
      case 504:
        return {
          message: 'Server error',
          description: 'Something went wrong on our end.',
          action: 'Please try again later or contact support.',
        };
      default:
        return {
          message: 'An error occurred',
          description: apiError.message,
          action: 'Please try again.',
        };
    }
  }
  
  if (error instanceof Error) {
    if (error.message.includes('NetworkError') || error.message.includes('fetch')) {
      return {
        message: 'Connection error',
        description: 'Unable to connect to the server.',
        action: 'Please check your internet connection and try again.',
      };
    }
    return {
      message: 'An error occurred',
      description: error.message,
      action: 'Please try again.',
    };
  }
  
  return {
    message: 'An unexpected error occurred',
    description: 'Something went wrong.',
    action: 'Please try again or refresh the page.',
  };
}

export function handleApiError(error: unknown, showNotification = true): ErrorDetails {
  const details = getUserFriendlyMessage(error);
  
  if (showNotification) {
    message.error({
      content: details.message,
      duration: 5,
    });
  }
  
  return details;
}

export function logError(error: unknown, context?: string): void {
  console.error(`[Error${context ? ` - ${context}` : ''}]:`, error);
}
