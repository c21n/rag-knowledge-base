/**
 * Document type definitions
 * Following the backend Document model structure
 */

export type DocumentStatus = 'pending' | 'processing' | 'completed' | 'error';

export interface Document {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  status: DocumentStatus;
  chunk_count: number;
  created_at: string;
  updated_at: string;
}

export interface DocumentUploadResponse {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  status: DocumentStatus;
  message: string;
}

export interface DocumentListResponse {
  items: Document[];
  total: number;
}

export interface DocumentStatusResponse {
  id: string;
  status: DocumentStatus;
  chunk_count: number;
  message?: string;
}

export interface ApiError {
  detail: string;
}

export const ALLOWED_FILE_TYPES = ['.pdf', '.docx', '.md', '.txt'];

export const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB in bytes

export const MIME_TYPE_MAP: Record<string, string> = {
  '.pdf': 'application/pdf',
  '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  '.md': 'text/markdown',
  '.txt': 'text/plain',
};

export function isAllowedFileType(filename: string): boolean {
  const ext = filename.toLowerCase().slice(filename.lastIndexOf('.'));
  return ALLOWED_FILE_TYPES.includes(ext);
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export function getStatusColor(status: DocumentStatus): string {
  switch (status) {
    case 'pending':
      return 'default';
    case 'processing':
      return 'blue';
    case 'completed':
      return 'green';
    case 'error':
      return 'red';
    default:
      return 'default';
  }
}

export function getStatusText(status: DocumentStatus): string {
  switch (status) {
    case 'pending':
      return '待处理';
    case 'processing':
      return '处理中';
    case 'completed':
      return '已完成';
    case 'error':
      return '错误';
    default:
      return '未知';
  }
}
