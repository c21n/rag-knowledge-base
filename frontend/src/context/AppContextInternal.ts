import { createContext } from 'react';
import type { AppState } from './AppState';

export const AppContext = createContext<AppState | undefined>(undefined);
