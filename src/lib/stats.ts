/**
 * Derived stats over the sessions history (§C: history → Home/Stats/Profile).
 * Pure functions, all computed live from real sessions — never fabricated.
 */
import type { Session } from '@/types';
import { SESSION_XP } from './session';

/** Local midnight for a timestamp. DST-safe (works on calendar dates). */
export function startOfDay(ts: number): number {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

/** Calendar-day offset from a midnight timestamp. */
function addDays(midnightMs: number, n: number): number {
  const d = new Date(midnightMs);
  d.setDate(d.getDate() + n);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function totalMinutes(sessions: Session[]): number {
  return sessions.reduce((sum, s) => sum + s.durationMin, 0);
}

/** Minutes logged in [start, end) by session start time. */
export function minutesBetween(sessions: Session[], start: number, end: number): number {
  return sessions.reduce(
    (sum, s) => (s.startedAt >= start && s.startedAt < end ? sum + s.durationMin : sum),
    0
  );
}

/** XP is a flat award per session for now (§B.2). */
export function totalXp(sessions: Session[]): number {
  return sessions.length * SESSION_XP;
}

/**
 * Consecutive days with ≥1 session, counting back from today (or yesterday,
 * so a streak isn't "lost" until a full day passes with nothing logged).
 */
export function currentStreak(sessions: Session[], now: number = Date.now()): number {
  if (sessions.length === 0) return 0;
  const days = new Set(sessions.map((s) => startOfDay(s.startedAt)));
  let cursor = startOfDay(now);
  if (!days.has(cursor)) {
    cursor = addDays(cursor, -1);
    if (!days.has(cursor)) return 0;
  }
  let count = 0;
  while (days.has(cursor)) {
    count++;
    cursor = addDays(cursor, -1);
  }
  return count;
}

/** Longest run of consecutive active days anywhere in history. */
export function longestStreak(sessions: Session[]): number {
  if (sessions.length === 0) return 0;
  const days = [...new Set(sessions.map((s) => startOfDay(s.startedAt)))].sort(
    (a, b) => a - b
  );
  let best = 1;
  let run = 1;
  for (let i = 1; i < days.length; i++) {
    if (days[i] === addDays(days[i - 1], 1)) {
      run++;
      best = Math.max(best, run);
    } else {
      run = 1;
    }
  }
  return best;
}

export interface DayBar {
  label: string;
  minutes: number;
  isToday: boolean;
}

/** Minutes per day for the trailing 7 days, oldest → today (bar chart). */
export function last7Days(sessions: Session[], now: number = Date.now()): DayBar[] {
  const today = startOfDay(now);
  const bars: DayBar[] = [];
  for (let i = 6; i >= 0; i--) {
    const day = addDays(today, -i);
    const next = addDays(day, 1);
    bars.push({
      label: WEEKDAYS[new Date(day).getDay()],
      minutes: minutesBetween(sessions, day, next),
      isToday: i === 0,
    });
  }
  return bars;
}

export interface PeriodStat {
  minutes: number;
  /** % change vs the preceding window; null when there's no prior data. */
  deltaPct: number | null;
}

/** Rolling window of `days` ending now, with delta vs the preceding window. */
export function rollingPeriod(
  sessions: Session[],
  days: number,
  now: number = Date.now()
): PeriodStat {
  const end = addDays(startOfDay(now), 1); // include all of today
  const start = addDays(end, -days);
  const prevStart = addDays(start, -days);
  const minutes = minutesBetween(sessions, start, end);
  const prev = minutesBetween(sessions, prevStart, start);
  const deltaPct = prev > 0 ? Math.round(((minutes - prev) / prev) * 100) : null;
  return { minutes, deltaPct };
}
