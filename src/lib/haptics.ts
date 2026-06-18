/**
 * Thin wrapper over expo-haptics so screens fire feedback without worrying
 * about platform support (web is a no-op). Full haptics pass is Phase 6;
 * these cover the defining moments of the session loop.
 */
import * as Haptics from 'expo-haptics';

const safe = (p: Promise<void>) => p.catch(() => {});

export const haptic = {
  /** Toggling an app in the seal list. */
  light: () => safe(Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light)),
  /** Starting a session / committing an action. */
  medium: () => safe(Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)),
  /** A block completing. */
  success: () => safe(Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)),
  /** Breaking the seal early — deliberate, slightly uncomfortable. */
  warning: () => safe(Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning)),
};
