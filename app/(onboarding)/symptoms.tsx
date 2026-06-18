import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { colors, gradients, spacing } from '@/theme';

const LINES = [
  'Every day, the gap between you and the people who finish things gets a little wider.',
  'The version of you that ships, trains, writes — drifting a little further out of reach.',
  'Right now the apps win by default. You don’t decide how your hours go — they do.',
];

export default function Symptoms() {
  return (
    <OnboardingScreen
      progress={PROGRESS.symptoms}
      gradient={gradients.symptomWarm}
      footer={
        <Button label="Show me the fix" onPress={() => router.push('/help')} />
      }
    >
      <KickerLabel color={colors.crimson}>The cost of waiting</KickerLabel>
      <Display style={styles.headline}>It compounds while you wait.</Display>
      <View style={styles.lines}>
        {LINES.map((line, i) => (
          <View key={i} style={styles.lineRow}>
            <View style={styles.tick} />
            <Body color={colors.cream} style={styles.lineText}>
              {line}
            </Body>
          </View>
        ))}
      </View>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  lines: {
    marginTop: spacing['2xl'],
    gap: spacing.xl,
  },
  lineRow: {
    flexDirection: 'row',
    gap: spacing.md,
  },
  tick: {
    width: 4,
    borderRadius: 2,
    backgroundColor: colors.crimson,
  },
  lineText: {
    flex: 1,
    fontSize: 18,
    lineHeight: 26,
  },
});
