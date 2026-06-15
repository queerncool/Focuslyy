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
