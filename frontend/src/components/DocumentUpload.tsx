import React, { useState } from 'react';
import { Upload, Alert, Progress, Typography, Space } from 'antd';
import { InboxOutlined, FilePdfOutlined, FileWordOutlined, FileMarkdownOutlined, FileTextOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd/es/upload';
import { useDocuments } from '../hooks/useDocuments';
import {
  ALLOWED_FILE_TYPES,
  MAX_FILE_SIZE,
  isAllowedFileType,
  formatFileSize,
} from '../types/document';

const { Dragger } = Upload;
const { Text } = Typography;

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUploadSuccess,
}) => {
  const { uploadDocument, uploadProgress, isUploading } = useDocuments();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const getFileIcon = (filename: string) => {
    const ext = filename.toLowerCase().slice(filename.lastIndexOf('.'));
    switch (ext) {
      case '.pdf':
        return <FilePdfOutlined />;
      case '.docx':
        return <FileWordOutlined />;
      case '.md':
        return <FileMarkdownOutlined />;
      case '.txt':
        return <FileTextOutlined />;
      default:
        return <InboxOutlined />;
    }
  };

  const beforeUpload = (file: File): boolean => {
    setError(null);
    setSuccess(null);

    // Check file type
    if (!isAllowedFileType(file.name)) {
      setError(`不支持的文件类型: ${file.name}. 支持的格式: ${ALLOWED_FILE_TYPES.join(', ')}`);
      return false;
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
      setError(`文件过大: ${file.name}. 最大支持 ${formatFileSize(MAX_FILE_SIZE)}`);
      return false;
    }

    return true;
  };

  const customRequest: UploadProps['customRequest'] = async ({ file, onSuccess, onError }) => {
    const uploadFile = file as File;
    
    setError(null);
    setSuccess(null);

    try {
      const success = await uploadDocument(uploadFile);
      
      if (success) {
        setSuccess(`文件 "${uploadFile.name}" 上传成功！`);
        setFileList([]);
        onUploadSuccess?.();
        onSuccess?.('ok');
      } else {
        onError?.(new Error('上传失败'));
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '上传失败';
      setError(errorMessage);
      onError?.(new Error(errorMessage));
    }
  };

  const handleChange: UploadProps['onChange'] = (info) => {
    setFileList(info.fileList.slice(-1)); // Keep only the last file
  };

  return (
    <div>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        {error && (
          <Alert
            message="上传错误"
            description={error}
            type="error"
            showIcon
            closable
            onClose={() => setError(null)}
          />
        )}

        {success && (
          <Alert
            message="上传成功"
            description={success}
            type="success"
            showIcon
            closable
            onClose={() => setSuccess(null)}
          />
        )}

        <Dragger
          name="file"
          multiple={false}
          fileList={fileList}
          beforeUpload={beforeUpload}
          customRequest={customRequest}
          onChange={handleChange}
          disabled={isUploading}
          accept={ALLOWED_FILE_TYPES.join(',')}
          showUploadList={{
            showRemoveIcon: !isUploading,
          }}
        >
          <p className="ant-upload-drag-icon">
            {fileList.length > 0 && fileList[0].name
              ? getFileIcon(fileList[0].name)
              : <InboxOutlined />}
          </p>
          <p className="ant-upload-text">
            点击或拖拽文件到此区域上传
          </p>
          <p className="ant-upload-hint">
            支持单个文件上传，文件大小不超过 {formatFileSize(MAX_FILE_SIZE)}
          </p>
          <div style={{ marginTop: 16 }}>
            <Text type="secondary">
              支持的文件类型: {ALLOWED_FILE_TYPES.join(', ')}
            </Text>
          </div>
        </Dragger>

        {isUploading && (
          <div style={{ marginTop: 16 }}>
            <Text>正在上传...</Text>
            <Progress
              percent={uploadProgress}
              status="active"
              strokeColor={{ from: '#108ee9', to: '#87d068' }}
            />
          </div>
        )}
      </Space>
    </div>
  );
};

export default DocumentUpload;
