import React, { createContext, useContext, useState, useCallback } from 'react';
import type { Role } from '../types/role';

export interface AppState {
  // Session
  sessionId: string | null;
  setSessionId: (id: string | null) => void;
  
  // Role
  selectedRole: Role | null;
  setSelectedRole: (role: Role | null) => void;
  
  // Navigation
  activeView: 'chat' | 'documents' | 'history';
  setActiveView: (view: 'chat' | 'documents' | 'history') => void;
  
  // UI State
  isSidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  
  // Actions
  startNewSession: () => void;
}

const AppContext = createContext<AppState | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [activeView, setActiveView] = useState<'chat' | 'documents' | 'history'>('chat');
  const [isSidebarCollapsed, setSidebarCollapsed] = useState(false);
  
  const startNewSession = useCallback(() => {
    setSessionId(null);
    setActiveView('chat');
  }, []);
  
  const value: AppState = {
    sessionId,
    setSessionId,
    selectedRole,
    setSelectedRole,
    activeView,
    setActiveView,
    isSidebarCollapsed,
    setSidebarCollapsed,
    startNewSession,
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = (): AppState => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
