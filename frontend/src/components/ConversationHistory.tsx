import React from 'react';
import { List, Card, Typography, Tag, Empty, Spin, Space } from 'antd';
import { MessageOutlined, ClockCircleOutlined, RobotOutlined } from '@ant-design/icons';
import { useConversations } from '../hooks/useConversations';
import type { ConversationPreview } from '../types/conversation';

const { Text, Paragraph } = Typography;

interface ConversationHistoryProps {
  onSelectConversation?: (sessionId: string) => void;
}

export const ConversationHistory: React.FC<ConversationHistoryProps> = ({ 
  onSelectConversation 
}) => {
  const { conversations, loading } = useConversations();
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
      return '昨天';
    } else if (diffDays < 7) {
      const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
      return weekdays[date.getDay()];
    } else {
      return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
    }
  };
  
  const truncateText = (text: string, maxLength: number = 60) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };
  
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <Spin size="large" />
      </div>
    );
  }
  
  if (conversations.length === 0) {
    return (
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        description="暂无对话历史"
      />
    );
  }
  
  return (
    <div>
      <List
        dataSource={conversations}
        renderItem={(item: ConversationPreview) => (
          <List.Item style={{ padding: '8px 0' }}>
            <Card
              hoverable
              onClick={() => onSelectConversation?.(item.session_id)}
              style={{ width: '100%' }}
              bodyStyle={{ padding: '12px 16px' }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                <div style={{ 
                  padding: '8px', 
                  backgroundColor: '#f0f0f0', 
                  borderRadius: '8px',
                  flexShrink: 0
                }}>
                  <MessageOutlined style={{ fontSize: 20, color: '#1890ff' }} />
                </div>
                
                <div style={{ flex: 1, minWidth: 0 }}>
                  <Paragraph 
                    style={{ margin: 0, fontWeight: 500 }}
                    ellipsis={{ rows: 1 }}
                  >
                    {truncateText(item.preview)}
                  </Paragraph>
                  
                  <div style={{ marginTop: 4 }}>
                    <Space size="middle">
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        <ClockCircleOutlined style={{ marginRight: 4 }} />
                        {formatDate(item.last_updated)}
                      </Text>
                      
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        <MessageOutlined style={{ marginRight: 4 }} />
                        {item.message_count} 条消息
                      </Text>
                      
                      {item.role_name && (
                        <Tag icon={<RobotOutlined />}>
                          {item.role_name}
                        </Tag>
                      )}
                    </Space>
                  </div>
                </div>
              </div>
            </Card>
          </List.Item>
        )}
      />
    </div>
  );
};
