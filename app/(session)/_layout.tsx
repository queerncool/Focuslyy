import { Stack } from 'expo-router';
import { colors } from '@/theme';

/** Modal session flow stack (setSession → … → share). Screens land in Phase 3. */
export default function SessionLayout() {
  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.espresso },
      }}
    />
  );
}
