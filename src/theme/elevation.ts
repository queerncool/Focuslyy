import { Platform, type ViewStyle } from 'react-native';

/**
 * Subtle elevation tokens for a layered, native feel. Shadows are neutral
 * (black-based) — not palette colors — and centralized here so components never
 * inline shadow values. Kept gentle: depth you feel, not flashy drop-shadows.
 */
const SHADOW = '#000';

const make = (
  height: number,
  radius: number,
  opacity: number,
  android: number
): ViewStyle =>
  (Platform.select({
    ios: {
      shadowColor: SHADOW,
      shadowOffset: { width: 0, height },
      shadowOpacity: opacity,
      shadowRadius: radius,
    },
    android: { elevation: android },
    default: {},
  }) as ViewStyle);

export const elevation = {
  none: {} as ViewStyle,
  sm: make(2, 8, 0.18, 2), // cards, pressables
  md: make(6, 16, 0.22, 6), // raised cards, the primary CTA
  lg: make(12, 28, 0.28, 12), // modals, floating surfaces
} as const;

export type ElevationToken = keyof typeof elevation;
