import React from 'react';
import { Card, Typography, Tag, Space, Tooltip } from 'antd';
import { UserOutlined, RobotOutlined, FileTextOutlined } from '@ant-design/icons';
import type { ChatMessage as ChatMessageType } from '../types/chat';

const { Text } = Typography;

interface ChatMessageProps {
  message: ChatMessageType;
}

/**
 * Format timestamp to readable string
 */
function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * ChatMessage component
 * Displays a single chat message with styling based on role
 */
const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        marginBottom: '16px',
        padding: '0 8px',
      }}
    >
      <Card
        size="small"
        style={{
          maxWidth: '80%',
          backgroundColor: isUser ? '#1890ff' : '#52c41a',
          border: 'none',
          borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
        }}
        bodyStyle={{
          padding: '12px 16px',
        }}
      >
        <Space direction="vertical" size="small" style={{ width: '100%' }}>
          {/* Message header with icon and timestamp */}
          <Space style={{ justifyContent: isUser ? 'flex-end' : 'flex-start' }}>
            {isUser ? (
              <>
                <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: '12px' }}>
                  {formatTimestamp(message.timestamp)}
                </Text>
                <UserOutlined style={{ color: '#fff' }} />
              </>
            ) : (
              <>
                <RobotOutlined style={{ color: '#fff' }} />
                <Text style={{ color: 'rgba(255,255,255,0.85)', fontSize: '12px' }}>
                  {formatTimestamp(message.timestamp)}
                </Text>
              </>
            )}
          </Space>

          {/* Message content */}
          <Text
            style={{
              color: '#fff',
              fontSize: '14px',
              lineHeight: '1.6',
              whiteSpace: 'pre-wrap',
              wordBreak: 'break-word',
            }}
          >
            {message.content}
          </Text>

          {/* Source citations for assistant messages */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div style={{ marginTop: '8px' }}>
              <Space size={[4, 4]} wrap>
                {message.sources.map((source, index) => (
                  <Tooltip
                    key={`${source.document_id}-${source.chunk_index}-${index}`}
                    title={
                      <div style={{ maxWidth: '300px' }}>
                        <Text style={{ color: '#fff', fontSize: '12px' }}>
                          来源文档: {source.document_id}
                          <br />
                          相关度: {(source.score * 100).toFixed(1)}%
                          <br />
                          {source.content_preview}
                        </Text>
                      </div>
                    }
                    placement="bottom"
                    color="#333"
                  >
                    <Tag
                      icon={<FileTextOutlined />}
                      color="gold"
                      style={{ cursor: 'pointer' }}
                    >
                      来源 {index + 1}
                    </Tag>
                  </Tooltip>
                ))}
              </Space>
            </div>
          )}
        </Space>
      </Card>
    </div>
  );
};

export default ChatMessage;
