import type { Distraction, HoursBand, Mode } from '@/types';

/** Cited daily phone-use average (hours). The ONLY external stat we anchor to. */
export const AVG_HOURS = 4.62;

/** Progress-bar values per onboarding step (§B.1). */
export const PROGRESS = {
  start: 4,
  q1: 12,
  q2: 24,
  q3: 36,
  results: 48,
  symptoms: 56,
  help: 64,
  reviews: 72,
  features: 80,
  plan: 90,
  paywall: 96,
  discount: 98,
  firstSeal: 100,
} as const;

/** Q1 — phone-hours bands. hoursNum is the band midpoint (1, 3, 5, 7). */
export const HOURS_BANDS: { id: HoursBand; label: string; hoursNum: number }[] = [
  { id: 'under2', label: 'Under 2 hrs', hoursNum: 1 },
  { id: '2to4', label: '2–4 hrs', hoursNum: 3 },
  { id: '4to6', label: '4–6 hrs', hoursNum: 5 },
  { id: '6plus', label: '6+ hrs', hoursNum: 7 },
];

/** Q2 — distractions (multi-select). apps[] feeds the seal pre-checks & blocklist line. */
export const DISTRACTION_OPTIONS: {
  id: Distraction;
  label: string;
  apps: string[];
}[] = [
  { id: 'shortform', label: 'Short-form video (TikTok/Reels)', apps: ['TikTok', 'Instagram', 'YouTube'] },
  { id: 'social', label: 'Social media', apps: ['Instagram', 'X', 'Snapchat'] },
  { id: 'games', label: 'Games', apps: ['Games'] },
  { id: 'youtube', label: 'YouTube + streaming', apps: ['YouTube', 'Netflix', 'Twitch'] },
  { id: 'news', label: 'News', apps: ['News', 'Reddit'] },
  { id: 'texting', label: 'Texting + calling', apps: ['Messages', 'WhatsApp'] },
];

/** Q3 — goal → mode + 30-day projection text. */
export const GOAL_OPTIONS: {
  label: string;
  mode: Mode;
  projection: string;
}[] = [
  { label: 'A business or app', mode: 'Build', projection: 'your app, shipped' },
  { label: 'A fitter body', mode: 'Train', projection: 'a stronger body' },
  { label: 'A degree or new skill', mode: 'Study', projection: 'real progress on your degree' },
  { label: 'A creative project', mode: 'Create', projection: 'your project, made' },
  { label: 'Read more books', mode: 'Read', projection: 'a stack of books finished' },
  { label: 'Just my time back', mode: 'Reclaim', projection: 'your time, back in your hands' },
];

/** Derived Results/Paywall numbers from the Q1 band midpoint (§C). */
export function computeHours(hoursNum: number) {
  const yrNum = Math.round((hoursNum * 365) / 100) * 100; // nearest hundred
  const barH = hoursNum / AVG_HOURS; // ratio vs cited average
  return { yrNum, barH };
}

/** Plan projection: hours of deep work over the next ~30 days (4.3 weeks). */
export function planMonthlyHours(dailyGoal: number, commitDays: number) {
  return Math.round(dailyGoal * commitDays * 4.3);
}

/** Top-3 distinct apps across the chosen distractions (Plan blocklist line). */
export function topBlocklist(distractions: Distraction[]): string[] {
  const apps: string[] = [];
  for (const d of distractions) {
    const opt = DISTRACTION_OPTIONS.find((o) => o.id === d);
    if (!opt) continue;
    for (const a of opt.apps) if (!apps.includes(a)) apps.push(a);
  }
  return apps.slice(0, 3);
}
