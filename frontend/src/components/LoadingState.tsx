import React from 'react';
import { Spin, Skeleton, Card } from 'antd';

interface LoadingStateProps {
  type?: 'spinner' | 'skeleton' | 'card';
  tip?: string;
  rows?: number;
  fullscreen?: boolean;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  type = 'spinner',
  tip = '加载中...',
  rows = 4,
  fullscreen = false,
}) => {
  if (fullscreen) {
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(255, 255, 255, 0.8)',
          zIndex: 9999,
        }}
      >
        <Spin size="large" tip={tip} />
      </div>
    );
  }

  switch (type) {
    case 'skeleton':
      return <Skeleton active paragraph={{ rows }} />;

    case 'card':
      return (
        <Card>
          <Skeleton active paragraph={{ rows }} />
        </Card>
      );

    case 'spinner':
    default:
      return (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <Spin size="large" tip={tip} />
        </div>
      );
  }
};

// Specialized loading states
export const ChatLoading: React.FC = () => (
  <LoadingState type="spinner" tip="AI 正在思考..." />
);

export const DocumentLoading: React.FC = () => (
  <LoadingState type="skeleton" rows={6} />
);

export const TableLoading: React.FC = () => (
  <LoadingState type="card" rows={4} />
);
