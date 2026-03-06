import { useContext } from 'react';
import { AppContext } from '../context/AppContextInternal';
import type { AppState } from '../context/AppState';

export const useAppContext = (): AppState => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};
