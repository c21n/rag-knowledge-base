/**
 * Custom hook for document management
 * Handles document CRUD operations and upload state
 */

import { useState, useCallback, useEffect } from 'react';
import type { Document } from '../types/document';
import {
  isAllowedFileType,
  MAX_FILE_SIZE,
  formatFileSize,
} from '../types/document';
import * as documentApi from '../services/documentApi';

export interface UseDocumentsReturn {
  documents: Document[];
  loading: boolean;
  error: string | null;
  uploadProgress: number;
  isUploading: boolean;
  fetchDocuments: () => Promise<void>;
  uploadDocument: (file: File) => Promise<boolean>;
  deleteDocument: (id: string) => Promise<boolean>;
  refreshDocumentStatus: (id: string) => Promise<void>;
  validateFile: (file: File) => { valid: boolean; error?: string };
}

export function useDocuments(): UseDocumentsReturn {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  /**
   * Validate file before upload
   */
  const validateFile = useCallback((file: File): { valid: boolean; error?: string } => {
    // Check file type
    if (!isAllowedFileType(file.name)) {
      return {
        valid: false,
        error: `不支持的文件类型。支持的类型: PDF, DOCX, MD, TXT`,
      };
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      return {
        valid: false,
        error: `文件大小超过限制 (最大 ${formatFileSize(MAX_FILE_SIZE)})`,
      };
    }

    return { valid: true };
  }, []);

  /**
   * Fetch all documents
   */
  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await documentApi.listDocuments();
      setDocuments(response.items);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '获取文档列表失败';
      setError(errorMessage);
      console.error('Failed to fetch documents:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Upload a new document
   */
  const uploadDocument = useCallback(async (file: File): Promise<boolean> => {
    // Validate file first
    const validation = validateFile(file);
    if (!validation.valid) {
      setError(validation.error || '文件验证失败');
      return false;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      await documentApi.uploadDocument(file, (progress) => {
        setUploadProgress(progress);
      });

      // Refresh document list after successful upload
      await fetchDocuments();
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '上传文档失败';
      setError(errorMessage);
      console.error('Failed to upload document:', err);
      return false;
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  }, [fetchDocuments, validateFile]);

  /**
   * Delete a document
   */
  const deleteDocument = useCallback(async (id: string): Promise<boolean> => {
    try {
      await documentApi.deleteDocument(id);
      // Update local state
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '删除文档失败';
      setError(errorMessage);
      console.error('Failed to delete document:', err);
      return false;
    }
  }, []);

  /**
   * Refresh status of a specific document
   */
  const refreshDocumentStatus = useCallback(async (id: string) => {
    try {
      const statusResponse = await documentApi.getDocumentStatus(id);
      
      // Update the document in the list
      setDocuments((prev) =>
        prev.map((doc) =>
          doc.id === id
            ? {
                ...doc,
                status: statusResponse.status,
                chunk_count: statusResponse.chunk_count,
              }
            : doc
        )
      );
    } catch (err) {
      console.error('Failed to refresh document status:', err);
    }
  }, []);

  // Auto-refresh documents on mount
  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  return {
    documents,
    loading,
    error,
    uploadProgress,
    isUploading,
    fetchDocuments,
    uploadDocument,
    deleteDocument,
    refreshDocumentStatus,
    validateFile,
  };
}

export default useDocuments;
