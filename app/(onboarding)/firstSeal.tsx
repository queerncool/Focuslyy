import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
  RingTimer,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { useProfileStore, useQuizStore, useSessionStore } from '@/state';
import { colors, spacing } from '@/theme';

export default function FirstSeal() {
  const mode = useQuizStore((s) => s.mode);
  const setOnboarded = useProfileStore((s) => s.setOnboarded);
  const setBlockMin = useSessionStore((s) => s.setBlockMin);
  const setMode = useSessionStore((s) => s.setMode);

  const startFirstSeal = () => {
    // Seed the 5-minute starter session, then drop straight into the seal step.
    setBlockMin(5);
    setMode(mode);
    setOnboarded(true);
    router.replace('/sealApps');
  };

  return (
    <OnboardingScreen
      progress={PROGRESS.firstSeal}
      footer={<Button label="Start my first seal" onPress={startFirstSeal} />}
    >
      <View style={styles.hero}>
        <RingTimer progress={1} size={170} strokeWidth={12} label="5" caption="MINUTES" />
      </View>
      <KickerLabel color={colors.amber}>You're in</KickerLabel>
      <Display style={styles.headline}>Let's run your first seal.</Display>
      <Body style={styles.sub}>
        Just 5 minutes — long enough to feel what locked-in actually feels like.
      </Body>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  hero: {
    alignItems: 'center',
    marginTop: spacing.xl,
    marginBottom: spacing['2xl'],
  },
  headline: {
    marginTop: spacing.sm,
  },
  sub: {
    marginTop: spacing.md,
    fontSize: 17,
    lineHeight: 25,
  },
});
