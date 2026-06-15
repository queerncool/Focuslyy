/**
 * Shared domain types. Mirrors §D (State model) and §C (Data bindings) of BUILD.md.
 */

/** Q3 goal → mode. Drives projection text, session chips, mode pill. */
export type Mode = 'Build' | 'Train' | 'Study' | 'Create' | 'Read' | 'Reclaim';

/** Q1 phone-hours band (single-select). */
export type HoursBand = 'under2' | '2to4' | '4to6' | '6plus';

/** Q2 distractions (multi-select). */
export type Distraction =
  | 'shortform'
  | 'social'
  | 'games'
  | 'youtube'
  | 'news'
  | 'texting';

/** Day-1 vs Established gating (§B.4). */
export type Phase = 'day1' | 'established';

export type AuthProvider = 'anonymous' | 'apple' | 'google';

export type SubscriptionTier = 'weekly' | 'monthly' | 'yearly' | null;
export type SubscriptionStatus = 'none' | 'active' | 'expired';

/** A single completed (or in-flight, then persisted) focus session. */
export interface Session {
  id: string;
  startedAt: number; // epoch ms
  endedAt: number | null; // epoch ms, null while in flight
  durationMin: number;
  mode: Mode | null;
  task: string;
  note: string;
  completed: boolean;
  blockedApps: string[];
}

/** Subset of notification toggles (settings store). */
export interface NotificationSettings {
  streakAtRisk: boolean;
  dailyGoalHit: boolean;
  scheduledReminder: boolean;
  logYourWin: boolean;
}
