/**
 * Document API service
 * Handles all document-related API calls
 */

import axios from 'axios';
import type { AxiosProgressEvent } from 'axios';
import type {
  Document,
  DocumentUploadResponse,
  DocumentListResponse,
  DocumentStatusResponse,
} from '../types/document';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload a document file
 * @param file - The file to upload
 * @param onProgress - Optional callback for upload progress
 * @returns DocumentUploadResponse
 */
export async function uploadDocument(
  file: File,
  onProgress?: (progress: number) => void
): Promise<DocumentUploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<DocumentUploadResponse>('/documents', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent: AxiosProgressEvent) => {
      if (onProgress && progressEvent.total) {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      }
    },
  });

  return response.data;
}

/**
 * List all documents
 * @returns DocumentListResponse
 */
export async function listDocuments(): Promise<DocumentListResponse> {
  const response = await api.get<DocumentListResponse>('/documents');
  return response.data;
}

/**
 * Get a single document by ID
 * @param id - Document ID
 * @returns Document
 */
export async function getDocument(id: string): Promise<Document> {
  const response = await api.get<Document>(`/documents/${id}`);
  return response.data;
}

/**
 * Delete a document by ID
 * @param id - Document ID
 */
export async function deleteDocument(id: string): Promise<void> {
  await api.delete(`/documents/${id}`);
}

/**
 * Get document processing status
 * @param id - Document ID
 * @returns DocumentStatusResponse
 */
export async function getDocumentStatus(id: string): Promise<DocumentStatusResponse> {
  const response = await api.get<DocumentStatusResponse>(`/documents/${id}/status`);
  return response.data;
}

/**
 * Process a document (trigger processing pipeline)
 * @param id - Document ID
 * @returns DocumentStatusResponse
 */
export async function processDocument(id: string): Promise<DocumentStatusResponse> {
  const response = await api.post<DocumentStatusResponse>(`/documents/${id}/process`);
  return response.data;
}

export default {
  uploadDocument,
  listDocuments,
  getDocument,
  deleteDocument,
  getDocumentStatus,
  processDocument,
};
