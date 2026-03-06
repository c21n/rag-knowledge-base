/**
 * useRoles Hook
 * Custom React hook for managing AI assistant roles
 */

import { useState, useEffect, useCallback } from 'react';
import type { Role } from '../types/role';
import { roleApi } from '../services/roleApi';

const STORAGE_KEY = 'selected_role_id';

/**
 * Hook return type
 */
interface UseRolesReturn {
  roles: Role[];
  selectedRole: Role | null;
  loading: boolean;
  error: string | null;
  selectRole: (role: Role) => void;
  refreshRoles: () => Promise<void>;
}

/**
 * Custom hook for role management
 * Fetches roles, manages selected state with localStorage persistence
 * @returns UseRolesReturn - Roles state and management functions
 */
export function useRoles(): UseRolesReturn {
  const [roles, setRoles] = useState<Role[]>([]);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch roles from API and set selected role
   */
  const fetchRoles = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await roleApi.listRoles();
      setRoles(response.roles);

      // Check localStorage for previously selected role
      const savedRoleId = localStorage.getItem(STORAGE_KEY);

      if (savedRoleId) {
        const savedRole = response.roles.find(r => r.id === savedRoleId);
        if (savedRole) {
          setSelectedRole(savedRole);
        } else {
          // Fallback to default if saved role not found
          const defaultRole = response.roles.find(r => r.id === response.default_role_id);
          setSelectedRole(defaultRole || response.roles[0] || null);
        }
      } else {
        // Use default role
        const defaultRole = response.roles.find(r => r.id === response.default_role_id);
        setSelectedRole(defaultRole || response.roles[0] || null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load roles');
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Select a role and persist to localStorage
   * @param role - Role to select
   */
  const selectRole = useCallback((role: Role) => {
    setSelectedRole(role);
    localStorage.setItem(STORAGE_KEY, role.id);
  }, []);

  // Fetch roles on mount
  useEffect(() => {
    fetchRoles();
  }, [fetchRoles]);

  return {
    roles,
    selectedRole,
    loading,
    error,
    selectRole,
    refreshRoles: fetchRoles,
  };
}
