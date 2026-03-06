/**
 * RoleSelector Component
 * AI Assistant role selector with dropdown and description display
 */

import React from 'react';
import { Select, Card, Typography, Space, Tag, Spin, Alert } from 'antd';
import { useRoles } from '../hooks/useRoles';
import type { Role } from '../types/role';
import {
  ToolOutlined,
  TeamOutlined,
  ShoppingOutlined,
  RobotOutlined
} from '@ant-design/icons';

const { Paragraph } = Typography;
const { Option } = Select;

/**
 * Get icon component based on role ID
 * @param roleId - Role identifier
 * @returns React.ReactNode - Icon component
 */
const getRoleIcon = (roleId: string): React.ReactNode => {
  switch (roleId) {
    case 'technical':
      return <ToolOutlined />;
    case 'hr':
      return <TeamOutlined />;
    case 'product':
      return <ShoppingOutlined />;
    default:
      return <RobotOutlined />;
  }
};

/**
 * Get Ant Design Tag color based on role ID
 * @param roleId - Role identifier
 * @returns string - Color name for Tag component
 */
const getRoleColor = (roleId: string): string => {
  switch (roleId) {
    case 'technical':
      return 'blue';
    case 'hr':
      return 'green';
    case 'product':
      return 'purple';
    default:
      return 'default';
  }
};

/**
 * Props for RoleSelector component
 */
interface RoleSelectorProps {
  /** Callback when role changes */
  onRoleChange?: (role: Role) => void;
}

/**
 * RoleSelector component
 * Displays a dropdown to select AI assistant roles with descriptions
 * @param onRoleChange - Optional callback when role selection changes
 */
export const RoleSelector: React.FC<RoleSelectorProps> = ({ onRoleChange }) => {
  const { roles, selectedRole, loading, error, selectRole } = useRoles();

  /**
   * Handle role selection change
   * @param roleId - Selected role ID
   */
  const handleChange = (roleId: string) => {
    const role = roles.find(r => r.id === roleId);
    if (role) {
      selectRole(role);
      onRoleChange?.(role);
    }
  };

  // Loading state
  if (loading) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <Spin tip="正在加载角色..." />
        </div>
      </Card>
    );
  }

  // Error state
  if (error) {
    return (
      <Alert
        message="加载角色失败"
        description={error}
        type="error"
        showIcon
      />
    );
  }

  return (
    <Card title="AI 助手角色" style={{ marginBottom: 16 }}>
      <Space direction="vertical" style={{ width: '100%' }} size="middle">
        <Select
          style={{ width: '100%' }}
          placeholder="选择角色"
          value={selectedRole?.id}
          onChange={handleChange}
          loading={loading}
        >
          {roles.map(role => (
            <Option key={role.id} value={role.id}>
              <Space>
                {getRoleIcon(role.id)}
                {role.name}
              </Space>
            </Option>
          ))}
        </Select>

        {selectedRole && (
          <div style={{ marginTop: 8 }}>
            <Space direction="vertical" style={{ width: '100%' }} size="small">
              <Space>
                <Tag color={getRoleColor(selectedRole.id)} icon={getRoleIcon(selectedRole.id)}>
                  {selectedRole.name}
                </Tag>
              </Space>
              <Paragraph type="secondary" style={{ margin: 0, fontSize: 14 }}>
                {selectedRole.description}
              </Paragraph>
            </Space>
          </div>
        )}
      </Space>
    </Card>
  );
};

export default RoleSelector;
