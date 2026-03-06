import React from 'react';
import { Layout, Menu, Button, Space, Typography } from 'antd';
import {
  MessageOutlined,
  FileTextOutlined,
  HistoryOutlined,
  PlusOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import { useAppContext } from '../context/AppContext';
import { RoleSelector } from '../components/RoleSelector';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const {
    activeView,
    setActiveView,
    isSidebarCollapsed,
    setSidebarCollapsed,
    startNewSession,
    selectedRole,
  } = useAppContext();
  
  const menuItems = [
    {
      key: 'chat',
      icon: <MessageOutlined />,
      label: '聊天',
    },
    {
      key: 'documents',
      icon: <FileTextOutlined />,
      label: '文档',
    },
    {
      key: 'history',
      icon: <HistoryOutlined />,
      label: '历史',
    },
    {
      key: 'documents',
      icon: <FileTextOutlined />,
      label: 'Documents',
    },
    {
      key: 'history',
      icon: <HistoryOutlined />,
      label: 'History',
    },
  ];
  
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={isSidebarCollapsed}
        width={280}
        style={{
          background: '#fff',
          borderRight: '1px solid #f0f0f0',
        }}
      >
        <div style={{ padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
          <Title level={4} style={{ margin: 0 }}>
            {isSidebarCollapsed ? '知识库' : '企业知识库'}
          </Title>
        </div>
        
        {!isSidebarCollapsed && (
          <div style={{ padding: '16px', borderBottom: '1px solid #f0f0f0' }}>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              block
              onClick={startNewSession}
            >
              新对话
            </Button>
          </div>
        )}
        
        <Menu
          mode="inline"
          selectedKeys={[activeView]}
          items={menuItems}
          onClick={({ key }) => setActiveView(key as any)}
          style={{ borderRight: 0 }}
        />
        
        {!isSidebarCollapsed && (
          <div style={{ padding: '16px', marginTop: 'auto' }}>
            <RoleSelector
              onRoleChange={(role) => {
                console.log('Role changed:', role);
              }}
            />
          </div>
        )}
      </Sider>
      
      <Layout>
        <Header
          style={{
            background: '#fff',
            padding: '0 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: '1px solid #f0f0f0',
          }}
        >
          <Button
            type="text"
            icon={isSidebarCollapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setSidebarCollapsed(!isSidebarCollapsed)}
          />
          
          <Space>
            {selectedRole && (
              <Typography.Text type="secondary">
                Role: {selectedRole.name}
              </Typography.Text>
            )}
          </Space>
        </Header>
        
        <Content
          style={{
            margin: '24px',
            padding: '24px',
            background: '#fff',
            borderRadius: '8px',
            minHeight: 'calc(100vh - 112px)',
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};
