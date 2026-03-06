/**
 * Role API Service
 * Handles API calls for role operations
 */

import type { RoleListResponse, RoleDetailsResponse } from '../types/role';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * API service for role operations
 */
export const roleApi = {
  /**
   * List all available roles
   * @returns Promise<RoleListResponse> - List of roles and default role ID
   */
  async listRoles(): Promise<RoleListResponse> {
    const response = await fetch(`${API_BASE_URL}/roles`);

    if (!response.ok) {
      throw new Error('Failed to fetch roles');
    }

    return response.json();
  },

  /**
   * Get details of a specific role
   * @param id - Role ID
   * @returns Promise<RoleDetailsResponse> - Role details
   */
  async getRole(id: string): Promise<RoleDetailsResponse> {
    const response = await fetch(`${API_BASE_URL}/roles/${id}`);

    if (!response.ok) {
      throw new Error('Failed to fetch role details');
    }

    return response.json();
  }
};
