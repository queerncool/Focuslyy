/**
 * Session-loop content maps (§B.2 / §C). Everything the Set Session, Seal,
 * and Log Win screens key off the user's Q3 mode and Q2 distractions.
 */
import type { Distraction, Mode } from '@/types';
import { DISTRACTION_OPTIONS } from './onboarding';

/** Block-length presets (minutes) + the custom-field cap. */
export const BLOCK_LENGTHS = [15, 30, 60, 90] as const;
export const MAX_CUSTOM_MIN = 240;
export const DEFAULT_BLOCK_MIN = 30;

/** XP awarded per completed block (real formula lands later — §B.2). */
export const SESSION_XP = 120;

/** Set Session suggestion chips, by mode (§B.2). */
export const goalTasks: Record<Mode, string[]> = {
  Build: ['Ship one feature', 'Fix the top bug', 'Write the landing copy'],
  Train: ['Full workout — no phone', 'Meal prep the week', 'Plan + log training'],
  Study: ['One full lecture + notes', 'Past-paper practice set', 'Read & summarize a chapter'],
  Create: ['Draft the next scene', 'Edit one video', 'Sketch three concepts'],
  Read: ['Read 30 pages', 'Finish the chapter', 'Read — no skimming'],
  Reclaim: ['One real task, start to finish', 'Inbox to zero', 'The thing you keep avoiding'],
};

/** Fallback task chips when no mode is set yet (e.g. the onboarding first seal). */
export const DEFAULT_TASKS = [
  'One real task, start to finish',
  'The thing you keep avoiding',
  'Inbox to zero',
];

/** Log Win one-tap completion chips, by mode (§B.2 — Build is spec'd, rest on-voice). */
export const logChips: Record<Mode, string[]> = {
  Build: ['Shipped it ✓', 'Made progress', 'Got unstuck'],
  Train: ['Crushed it ✓', 'Showed up', 'Pushed through'],
  Study: ['Nailed it ✓', 'Made progress', 'Finally clicked'],
  Create: ['Made it ✓', 'Found the flow', 'Rough but real'],
  Read: ['Finished it ✓', 'Made progress', 'Lost in it'],
  Reclaim: ['Done ✓', 'Made progress', 'Faced it'],
};

export const DEFAULT_LOG_CHIPS = ['Got it done ✓', 'Made progress', 'Showed up'];

/** Task suggestions for a mode (or the neutral fallback). */
export function tasksForMode(mode: Mode | null): string[] {
  return mode ? goalTasks[mode] : DEFAULT_TASKS;
}

/** Completion chips for a mode (or the neutral fallback). */
export function chipsForMode(mode: Mode | null): string[] {
  return mode ? logChips[mode] : DEFAULT_LOG_CHIPS;
}

/**
 * Canonical ordered list of named apps for the Phase-3 Seal screen. In Phase 7
 * this list is replaced by Apple's FamilyActivityPicker (opaque tokens).
 */
export const SEAL_APPS: string[] = [
  'TikTok',
  'Instagram',
  'YouTube',
  'X',
  'Snapchat',
  'Games',
  'Netflix',
  'Twitch',
  'News',
  'Reddit',
  'Messages',
  'WhatsApp',
];

/** Apps to pre-check on the Seal screen, derived from Q2 distractions (§C). */
export function recommendedApps(distractions: Distraction[]): string[] {
  const out: string[] = [];
  for (const d of distractions) {
    const opt = DISTRACTION_OPTIONS.find((o) => o.id === d);
    if (!opt) continue;
    for (const app of opt.apps) if (!out.includes(app)) out.push(app);
  }
  return out;
}
