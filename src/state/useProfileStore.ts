import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { asyncStorage, storeKey } from '@/lib/persist';
import type { AuthProvider, Phase } from '@/types';

/** §D profileStore — identity, plan customization, and progress. */
interface ProfileState {
  id: string | null; // UUID for anon, real ID after sign-in
  name: string;
  handle: string;
  joinedAt: number | null; // epoch ms
  authProvider: AuthProvider;

  dailyGoal: number; // hours/day target (default 2)
  commitDays: number; // days/week commitment (default 5)
  defaultBlocklist: string[];

  phase: Phase; // 'day1' default for a brand-new user

  streakDays: number;
  bestStreak: number;
  totalXp: number;
  rank: number | null;

  setName: (name: string) => void;
  setPlan: (dailyGoal: number, commitDays: number) => void;
  setPhase: (phase: Phase) => void;
  setIdentity: (id: string, provider: AuthProvider) => void;
  reset: () => void;
}

const initial = {
  id: null,
  name: '',
  handle: '',
  joinedAt: null,
  authProvider: 'anonymous' as AuthProvider,
  dailyGoal: 2,
  commitDays: 5,
  defaultBlocklist: [] as string[],
  phase: 'day1' as Phase,
  streakDays: 0,
  bestStreak: 0,
  totalXp: 0,
  rank: null,
};

export const useProfileStore = create<ProfileState>()(
  persist(
    (set) => ({
      ...initial,
      setName: (name) => set({ name }),
      setPlan: (dailyGoal, commitDays) => set({ dailyGoal, commitDays }),
      setPhase: (phase) => set({ phase }),
      setIdentity: (id, authProvider) => set({ id, authProvider }),
      reset: () => set(initial),
    }),
    { name: storeKey('profile'), storage: asyncStorage }
  )
);
