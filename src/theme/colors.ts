/**
 * focuslyy locked palette — do not invent variants.
 * Source of truth: CLAUDE.md "Brand system". Never inline hex in components.
 */

export const colors = {
  amber: '#F2A03D', // Primary — CTAs, seal, accents
  amberLight: '#F6B45E', // Hover / gradient highlights
  amberDeep: '#DE7A2C', // Pressed / gradient end
  espresso: '#18120E', // Dark backgrounds
  ink: '#221A12', // Dark cards / dark-bg text
  cream: '#F2EBDD', // Light backgrounds
  muted: '#8C8174', // Secondary text, inactive
  crimson: '#E5564B', // Only "break the seal" / cost-of-waiting accents
  teal: '#4FB6A0', // Break / positive states
} as const;

export type ColorToken = keyof typeof colors;

/**
 * Hairline border tints — derived from locked tokens at low opacity (NOT new
 * palette colors). Used for quiet, sleek 1px dividers and card edges instead of
 * heavy strokes. Centralized so components never inline rgba.
 */
export const border = {
  hairline: 'rgba(242,235,221,0.08)', // cream @ 8% — quiet edges on dark
  subtle: 'rgba(242,235,221,0.14)', // cream @ 14% — a touch more definition
  onLight: 'rgba(34,26,18,0.10)', // ink @ 10% — edges on cream surfaces
} as const;

/**
 * Background gradient tints — NOT new palette colors. Each is `espresso`
 * blended a touch toward an accent for screen mood (kept dark and on-brand).
 * Centralized here so components never inline hex.
 */
export const gradients = {
  symptomWarm: ['#33150F', colors.espresso], // warmed toward crimson — cost-of-waiting
  breakCalm: ['#13201D', colors.espresso], // cooled toward teal — break/positive
  locked: ['#0E0A07', colors.espresso], // deepest focus background
} as const;

/**
 * Semantic aliases. Components should prefer these where a role exists,
 * falling back to raw tokens above. Both resolve to locked hexes only.
 */
export const semantic = {
  bg: colors.espresso,
  surface: colors.ink,
  surfaceLight: colors.cream,
  textOnDark: colors.cream,
  textOnLight: colors.ink,
  textMuted: colors.muted,
  primary: colors.amber,
  primaryPressed: colors.amberDeep,
  danger: colors.crimson,
  positive: colors.teal,
} as const;
