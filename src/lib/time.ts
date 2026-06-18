/**
 * Time math for the session loop and stats. Pure functions, no side effects.
 */
import type { Session } from '@/types';

/** Seconds → "MM:SS" for countdown displays (mono). */
export function formatClock(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
}

/** Minutes → human duration: "45m", "1h", "1h 30m". */
export function formatDuration(totalMinutes: number): string {
  const m = Math.max(0, Math.round(totalMinutes));
  const h = Math.floor(m / 60);
  const min = m % 60;
  if (h === 0) return `${min}m`;
  if (min === 0) return `${h}h`;
  return `${h}h ${min}m`;
}

/** True if an epoch-ms timestamp falls on the local calendar day of `now`. */
export function isToday(ts: number, now: number = Date.now()): boolean {
  const a = new Date(ts);
  const b = new Date(now);
  return (
    a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate()
  );
}

/** Sum of deep-work minutes logged today (drives Home ring + Share card). */
export function todayMinutes(sessions: Session[], now: number = Date.now()): number {
  return sessions.reduce(
    (sum, s) => (isToday(s.startedAt, now) ? sum + s.durationMin : sum),
    0
  );
}
