import React, { useState, useCallback } from 'react';
import type { Role } from '../types/role';
import type { ViewType } from '../types/view';
import type { AppState } from './AppState';
import { AppContext } from './AppContextInternal';

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [activeView, setActiveView] = useState<ViewType>('chat');
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
