/**
 * ChatInterface component
 * Main chat interface with message list, input area, and error handling
 */
import React, { useRef, useEffect, useState } from 'react';
import type { InputRef } from 'antd';
import {
  Card,
  Input,
  Button,
  Space,
  Alert,
  Spin,
  Empty,
  Typography,
  Tooltip,
} from 'antd';
import { SendOutlined, ClearOutlined, LoadingOutlined } from '@ant-design/icons';
import { useChat } from '../hooks/useChat';
import ChatMessage from './ChatMessage';

const { TextArea } = Input;
const { Text } = Typography;

/**
 * ChatInterface component
 * Provides full chat functionality with message history and input
 */
export const ChatInterface: React.FC = () => {
  const { messages, loading, error, sendMessage, clearMessages, clearError } = useChat();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<InputRef>(null);

  /**
   * Auto-scroll to bottom when new messages arrive
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * Handle send message
   */
  const handleSend = async (): Promise<void> => {
    if (!inputValue.trim() || loading) return;

    const message = inputValue;
    setInputValue('');
    await sendMessage(message);
  };

  /**
   * Handle keyboard shortcuts
   * Enter: send message
   * Shift+Enter: new line
   */
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>): void => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /**
   * Handle clear messages
   */
  const handleClear = (): void => {
    clearMessages();
    setInputValue('');
  };

  return (
    <Card
      title="智能问答"
      extra={
        messages.length > 0 && (
          <Tooltip title="清空对话">
            <Button
              icon={<ClearOutlined />}
              size="small"
              onClick={handleClear}
              disabled={loading}
            >
              清空
            </Button>
          </Tooltip>
        )
      }
      style={{ height: '100%', display: 'flex', flexDirection: 'column' }}
      styles={{
        body: {
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          padding: '16px',
          overflow: 'hidden',
        },
      }}
    >
      {/* Error Alert */}
      {error && (
        <Alert
          message="发送失败"
          description={error}
          type="error"
          closable
          onClose={clearError}
          style={{ marginBottom: '16px' }}
          showIcon
        />
      )}

      {/* Messages Area */}
      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          overflowX: 'hidden',
          padding: '8px 0',
          marginBottom: '16px',
          borderRadius: '8px',
          backgroundColor: '#fafafa',
        }}
      >
        {messages.length === 0 ? (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description={
              <Space direction="vertical" size="small">
                <Text type="secondary">开始对话</Text>
                <Text type="secondary" style={{ fontSize: '12px' }}>
                  输入问题，按 Enter 发送，Shift+Enter 换行
                </Text>
              </Space>
            }
            style={{ marginTop: '40px' }}
          />
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {/* Loading indicator */}
            {loading && (
              <div style={{ textAlign: 'center', padding: '16px' }}>
                <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
                <Text type="secondary" style={{ marginLeft: '8px' }}>
                  AI 正在思考...
                </Text>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div style={{ borderTop: '1px solid #f0f0f0', paddingTop: '16px' }}>
        <Space.Compact style={{ width: '100%' }}>
          <TextArea
            ref={textareaRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入您的问题... (Enter 发送, Shift+Enter 换行)"
            autoSize={{ minRows: 2, maxRows: 6 }}
            disabled={loading}
            style={{ flex: 1 }}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSend}
            loading={loading}
            disabled={!inputValue.trim()}
            style={{ height: 'auto' }}
          >
            发送
          </Button>
        </Space.Compact>
      </div>
    </Card>
  );
};

export default ChatInterface;
