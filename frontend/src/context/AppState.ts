import type { Role } from '../types/role';
import type { ViewType } from '../types/view';

export interface AppState {
  // Session
  sessionId: string | null;
  setSessionId: (id: string | null) => void;
  
  // Role
  selectedRole: Role | null;
  setSelectedRole: (role: Role | null) => void;
  
  // Navigation
  activeView: ViewType;
  setActiveView: (view: ViewType) => void;
  
  // UI State
  isSidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  
  // Actions
  startNewSession: () => void;
}
