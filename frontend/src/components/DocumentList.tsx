import React from 'react';
import {
  Table,
  Tag,
  Button,
  Popconfirm,
  Space,
  Empty,
  Tooltip,
  Typography,
} from 'antd';
import {
  FilePdfOutlined,
  FileWordOutlined,
  FileMarkdownOutlined,
  FileTextOutlined,
  DeleteOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Document, DocumentStatus } from '../types/document';
import { useDocuments } from '../hooks/useDocuments';
import {
  formatFileSize,
  getStatusColor,
  getStatusText,
} from '../types/document';

const { Text } = Typography;

interface DocumentListProps {
  onRefresh?: () => void;
}

const DocumentList: React.FC<DocumentListProps> = ({
  onRefresh,
}) => {
  const { documents, loading, deleteDocument, fetchDocuments } = useDocuments();

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return <FilePdfOutlined style={{ color: '#ff4d4f', fontSize: 20 }} />;
      case 'docx':
        return <FileWordOutlined style={{ color: '#1890ff', fontSize: 20 }} />;
      case 'md':
        return <FileMarkdownOutlined style={{ color: '#13c2c2', fontSize: 20 }} />;
      case 'txt':
        return <FileTextOutlined style={{ color: '#52c41a', fontSize: 20 }} />;
      default:
        return <FileTextOutlined style={{ color: '#8c8c8c', fontSize: 20 }} />;
    }
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const columns: ColumnsType<Document> = [
    {
      title: '文件',
      dataIndex: 'original_filename',
      key: 'filename',
      render: (_, record) => (
        <Space>
          {getFileIcon(record.file_type)}
          <Text strong>{record.original_filename}</Text>
        </Space>
      ),
    },
    {
      title: '类型',
      dataIndex: 'file_type',
      key: 'type',
      width: 100,
      render: (type: string) => type.toUpperCase(),
    },
    {
      title: '大小',
      dataIndex: 'file_size',
      key: 'size',
      width: 120,
      render: (size: number) => formatFileSize(size),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: DocumentStatus) => (
        <Tag color={getStatusColor(status)}>{getStatusText(status)}</Tag>
      ),
    },
    {
      title: '分块数',
      dataIndex: 'chunk_count',
      key: 'chunks',
      width: 100,
      render: (count: number) => count || '-',
    },
    {
      title: '上传时间',
      dataIndex: 'created_at',
      key: 'created',
      width: 180,
      render: (date: string) => formatDate(date),
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Space>
          <Popconfirm
            title="删除文档"
            description={`确定要删除 "${record.original_filename}" 吗？`}
            onConfirm={async () => {
              await deleteDocument(record.id);
              onRefresh?.();
            }}
            okText="确定"
            cancelText="取消"
          >
            <Tooltip title="删除">
              <Button
                type="text"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Table
        columns={columns}
        dataSource={documents}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showTotal: (total) => `共 ${total} 个文档`,
        }}
        locale={{
          emptyText: <Empty description="暂无文档" />,
        }}
        title={() => (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Text strong>文档列表</Text>
            <Button
              type="text"
              icon={<ReloadOutlined />}
              onClick={() => {
                fetchDocuments();
                onRefresh?.();
              }}
              loading={loading}
            >
              刷新
            </Button>
          </div>
        )}
      />
    </div>
  );
};

export default DocumentList;
