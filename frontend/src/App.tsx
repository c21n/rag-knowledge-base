import React from 'react';
import { ConfigProvider } from 'antd';
import { AppProvider, useAppContext } from './context/AppContext';
import { MainLayout } from './layouts/MainLayout';
import { ChatInterface } from './components/ChatInterface';
import DocumentUpload from './components/DocumentUpload';
import DocumentList from './components/DocumentList';
import { ConversationHistory } from './components/ConversationHistory';
import { ErrorBoundary } from './components/ErrorBoundary';

const AppContent: React.FC = () => {
  const { activeView } = useAppContext();

  const renderContent = () => {
    switch (activeView) {
      case 'chat':
        return <ChatInterface />;
      case 'documents':
        return (
          <div>
            <h2>文档管理</h2>
            <DocumentUpload />
            <div style={{ marginTop: 24 }}>
              <DocumentList />
            </div>
          </div>
        );
      case 'history':
        return <ConversationHistory />;
      default:
        return <ChatInterface />;
    }
  };

  return (
    <MainLayout>
      {renderContent()}
    </MainLayout>
  );
};

function App() {
  return (
    <ErrorBoundary>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
          },
        }}
      >
        <AppProvider>
          <AppContent />
        </AppProvider>
      </ConfigProvider>
    </ErrorBoundary>
  );
}

export default App;
