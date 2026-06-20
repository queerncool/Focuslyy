import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { asyncStorage, storeKey } from '@/lib/persist';
import { generateId } from '@/lib/id';
import type {
  AuthProvider,
  Phase,
  SubscriptionStatus,
  SubscriptionTier,
} from '@/types';

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
  hasOnboarded: boolean; // gates entry: funnel vs main app

  // Subscription (stubbed in Phase 5, real RevenueCat in Phase 7).
  subscriptionTier: SubscriptionTier;
  subscriptionStatus: SubscriptionStatus;

  streakDays: number;
  bestStreak: number;
  totalXp: number;
  rank: number | null;

  setName: (name: string) => void;
  setPlan: (dailyGoal: number, commitDays: number) => void;
  setPhase: (phase: Phase) => void;
  setOnboarded: (value: boolean) => void;
  setIdentity: (id: string, provider: AuthProvider) => void;
  /** First-launch anonymous identity: a UUID + join timestamp, kept on sign-in. */
  ensureAnonymousId: () => void;
  /** Link the local profile (and its sessions) to a signed-in account. */
  linkAccount: (provider: Exclude<AuthProvider, 'anonymous'>) => void;
  /** Record a (stubbed) successful purchase. */
  setSubscription: (tier: SubscriptionTier) => void;
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
  hasOnboarded: false,
  subscriptionTier: null as SubscriptionTier,
  subscriptionStatus: 'none' as SubscriptionStatus,
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
      setOnboarded: (hasOnboarded) => set({ hasOnboarded }),
      setIdentity: (id, authProvider) => set({ id, authProvider }),
      ensureAnonymousId: () =>
        set((s) =>
          s.id
            ? {}
            : { id: generateId(), authProvider: 'anonymous', joinedAt: Date.now() }
        ),
      // Keep the same local id so existing sessions stay attached (mirrors
      // RevenueCat's anonymous→logIn aliasing we'll wire in Phase 7).
      linkAccount: (provider) =>
        set((s) => ({
          authProvider: provider,
          joinedAt: s.joinedAt ?? Date.now(),
        })),
      setSubscription: (tier) =>
        set({ subscriptionTier: tier, subscriptionStatus: 'active' }),
      reset: () => set(initial),
    }),
    { name: storeKey('profile'), storage: asyncStorage }
  )
);
