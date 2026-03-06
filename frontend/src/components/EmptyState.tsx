import React from 'react';
import { Empty, Button, Typography } from 'antd';
import {
  InboxOutlined,
  MessageOutlined,
  FileTextOutlined,
  HistoryOutlined,
  SearchOutlined,
} from '@ant-design/icons';

const { Title, Text } = Typography;

interface EmptyStateProps {
  type?: 'documents' | 'chat' | 'history' | 'search' | 'generic';
  title?: string;
  description?: string;
  actionText?: string;
  onAction?: () => void;
}

const emptyStateConfigs = {
  documents: {
    icon: <InboxOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />,
    title: '暂无文档',
    description: '上传文档开始使用知识库',
  },
  chat: {
    icon: <MessageOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />,
    title: '开始对话',
    description: '输入问题，从您的文档中获取 AI 驱动的答案',
  },
  history: {
    icon: <HistoryOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />,
    title: '暂无对话历史',
    description: '您的历史对话将显示在这里',
  },
  search: {
    icon: <SearchOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />,
    title: '未找到结果',
    description: '尝试调整您的搜索词或筛选条件',
  },
  generic: {
    icon: <FileTextOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />,
    title: '暂无数据',
    description: '当前没有可显示的内容',
  },
};

export const EmptyState: React.FC<EmptyStateProps> = ({
  type = 'generic',
  title,
  description,
  actionText,
  onAction,
}) => {
  const config = emptyStateConfigs[type];

  return (
    <Empty
      image={config.icon}
      description={
        <div style={{ textAlign: 'center' }}>
          <Title level={5} style={{ marginTop: 16, marginBottom: 8 }}>
            {title || config.title}
          </Title>
          <Text type="secondary">
            {description || config.description}
          </Text>
          {actionText && onAction && (
            <div style={{ marginTop: 24 }}>
              <Button type="primary" onClick={onAction}>
                {actionText}
              </Button>
            </div>
          )}
        </div>
      }
    />
  );
};
