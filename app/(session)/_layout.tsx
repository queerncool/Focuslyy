import { Stack } from 'expo-router';
import { colors } from '@/theme';

/** Modal session flow stack (setSession → … → share). Screens land in Phase 3. */
export default function SessionLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.espresso },
        animation: 'slide_from_right',
        // Swipe-back is disabled so the Locked screen can't be escaped by a
        // gesture — breaking the seal is long-press-only (CLAUDE.md).
        gestureEnabled: false,
      }}
    />
  );
}
