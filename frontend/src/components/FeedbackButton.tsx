import React, { useState } from 'react';
import { Button, Space, Tooltip, Modal, Form, Input, message } from 'antd';
import { LikeOutlined, DislikeOutlined, LikeFilled, DislikeFilled } from '@ant-design/icons';
import { useConversations } from '../hooks/useConversations';

const { TextArea } = Input;

interface FeedbackButtonProps {
  messageId: string;
  existingFeedback?: 'thumbs_up' | 'thumbs_down' | null;
}

export const FeedbackButton: React.FC<FeedbackButtonProps> = ({ 
  messageId,
  existingFeedback = null
}) => {
  const { submitFeedback } = useConversations();
  const [feedback, setFeedback] = useState<'thumbs_up' | 'thumbs_down' | null>(existingFeedback);
  const [loading, setLoading] = useState(false);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [pendingRating, setPendingRating] = useState<'thumbs_up' | 'thumbs_down' | null>(null);
  const [form] = Form.useForm();
  
  const handleFeedback = async (rating: 'thumbs_up' | 'thumbs_down', comment?: string) => {
    if (feedback === rating) return; // Already rated
    
    setLoading(true);
    
    try {
      await submitFeedback({
        message_id: messageId,
        rating,
        comment,
      });
      
      setFeedback(rating);
      message.success('感谢您的反馈！');
      setIsModalVisible(false);
      form.resetFields();
    } catch (err) {
      message.error('提交反馈失败');
    } finally {
      setLoading(false);
    }
  };
  
  const handleThumbsUp = () => {
    setPendingRating('thumbs_up');
    handleFeedback('thumbs_up');
  };
  
  const handleThumbsDown = () => {
    setPendingRating('thumbs_down');
    setIsModalVisible(true);
  };
  
  const handleModalSubmit = async (values: { comment: string }) => {
    if (pendingRating) {
      await handleFeedback(pendingRating, values.comment);
    }
  };
  
  return (
    <>
      <Space size="small">
        <Tooltip title="有帮助">
          <Button
            type="text"
            size="small"
            icon={feedback === 'thumbs_up' ? <LikeFilled style={{ color: '#52c41a' }} /> : <LikeOutlined />}
            onClick={handleThumbsUp}
            loading={loading && pendingRating === 'thumbs_up'}
          />
        </Tooltip>
        <Tooltip title="没有帮助">
          <Button
            type="text"
            size="small"
            icon={feedback === 'thumbs_down' ? <DislikeFilled style={{ color: '#ff4d4f' }} /> : <DislikeOutlined />}
            onClick={handleThumbsDown}
            loading={loading && pendingRating === 'thumbs_down'}
          />
        </Tooltip>
      </Space>
      
      <Modal
        title="有什么问题？"
        open={isModalVisible}
        onCancel={() => {
          setIsModalVisible(false);
          setPendingRating(null);
          form.resetFields();
        }}
        footer={null}
      >
        <Form form={form} onFinish={handleModalSubmit} layout="vertical">
          <Form.Item
            name="comment"
            label="可选反馈"
            rules={[{ max: 500, message: '反馈不能超过 500 个字符' }]}
          >
            <TextArea
              rows={3}
              placeholder="告诉我们如何改进..."
              maxLength={500}
              showCount
            />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => {
                setIsModalVisible(false);
                setPendingRating(null);
                form.resetFields();
              }}>
                取消
              </Button>
              <Button type="primary" htmlType="submit" loading={loading}>
                提交
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
