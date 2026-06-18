import { Stack } from 'expo-router';
import { colors } from '@/theme';

/** Onboarding funnel stack — no tab bar. Screens land in Phase 2. */
export default function OnboardingLayout() {
  return (
    <Stack
      initialRouteName="start"
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.espresso },
      }}
    />
  );
}
