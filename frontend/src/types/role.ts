/**
 * Role TypeScript types
 * Defines interfaces for AI assistant roles
 */

/**
 * Role interface representing an AI assistant persona
 */
export interface Role {
  id: string;
  name: string;
  description: string;
  system_prompt: string;
  icon?: string;
  color?: string;
}

/**
 * Response interface for listing all roles
 */
export interface RoleListResponse {
  roles: Role[];
  default_role_id: string;
}

/**
 * Response interface for getting role details
 */
export interface RoleDetailsResponse {
  role: Role;
}
