import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { asyncStorage, storeKey } from '@/lib/persist';
import type { Session } from '@/types';

/** §D sessionsHistoryStore — the append-only log of completed sessions. */
interface SessionsHistoryState {
  sessions: Session[];
  addSession: (session: Session) => void;
  clear: () => void;
}

export const useSessionsHistoryStore = create<SessionsHistoryState>()(
  persist(
    (set) => ({
      sessions: [],
      addSession: (session) =>
        set((s) => ({ sessions: [session, ...s.sessions] })),
      clear: () => set({ sessions: [] }),
    }),
    { name: storeKey('sessionsHistory'), storage: asyncStorage }
  )
);
