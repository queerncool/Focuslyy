import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { asyncStorage, storeKey } from '@/lib/persist';
import type { Mode } from '@/types';

/** §D sessionStore — the current/in-flight session being configured or run. */
interface SessionState {
  task: string;
  blockMin: number; // default 30 (Set Session picker)
  mode: Mode | null;
  blockedApps: string[];
  startedAt: number | null; // epoch ms when Locked begins

  setTask: (task: string) => void;
  setBlockMin: (blockMin: number) => void;
  setMode: (mode: Mode | null) => void;
  setBlockedApps: (apps: string[]) => void;
  start: () => void;
  clear: () => void;
}

const initial = {
  task: '',
  blockMin: 30,
  mode: null as Mode | null,
  blockedApps: [] as string[],
  startedAt: null as number | null,
};

export const useSessionStore = create<SessionState>()(
  persist(
    (set) => ({
      ...initial,
      setTask: (task) => set({ task }),
      setBlockMin: (blockMin) => set({ blockMin }),
      setMode: (mode) => set({ mode }),
      setBlockedApps: (blockedApps) => set({ blockedApps }),
      start: () => set({ startedAt: Date.now() }),
      clear: () => set(initial),
    }),
    { name: storeKey('session'), storage: asyncStorage }
  )
);
