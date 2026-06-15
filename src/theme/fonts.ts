import { useFonts } from 'expo-font';

/**
 * Brand typefaces (CLAUDE.md "Brand system"):
 *   - Schibsted Grotesk (display, 700/800)
 *   - Space Mono (timers, labels, stat numbers)
 *   - Fraunces Black Italic (marketing/onboarding accent)
 *
 * TTFs live in assets/fonts/ and are loaded via expo-font. Reference these
 * family-name constants everywhere — never the raw string literals.
 */
export const fontFamily = {
  // Display — Schibsted Grotesk
  display: 'SchibstedGrotesk-Bold', // 700
  displayHeavy: 'SchibstedGrotesk-ExtraBold', // 800
  // Mono — Space Mono (timers, labels, stat numbers)
  mono: 'SpaceMono-Regular',
  monoBold: 'SpaceMono-Bold',
  // Accent — Fraunces Black Italic
  accent: 'Fraunces-BlackItalic',
} as const;

export type FontFamilyToken = keyof typeof fontFamily;

/** The map consumed by expo-font's useFonts. */
export const fontAssets = {
  [fontFamily.display]: require('../../assets/fonts/SchibstedGrotesk-Bold.ttf'),
  [fontFamily.displayHeavy]: require('../../assets/fonts/SchibstedGrotesk-ExtraBold.ttf'),
  [fontFamily.mono]: require('../../assets/fonts/SpaceMono-Regular.ttf'),
  [fontFamily.monoBold]: require('../../assets/fonts/SpaceMono-Bold.ttf'),
  [fontFamily.accent]: require('../../assets/fonts/Fraunces-BlackItalic.ttf'),
};

/** Hook wrapper so screens import a single source of truth. */
export function useBrandFonts() {
  return useFonts(fontAssets);
}
