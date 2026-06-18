import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import {
  Body,
  Button,
  ChoiceCard,
  KickerLabel,
  OnboardingScreen,
  Title,
} from '@/components';
import { GOAL_OPTIONS, PROGRESS } from '@/lib/onboarding';
import { useQuizStore } from '@/state';
import { spacing } from '@/theme';

export default function Q3() {
  const mode = useQuizStore((s) => s.mode);
  const setGoal = useQuizStore((s) => s.setGoal);

  return (
    <OnboardingScreen
      progress={PROGRESS.q3}
      footer={
        <Button
          label="Continue"
          disabled={mode == null}
          onPress={() => router.push('/results')}
        />
      }
    >
      <KickerLabel>Question 3 of 3</KickerLabel>
      <Title style={styles.title}>
        What would you build if your phone stopped winning?
      </Title>
      <Body style={styles.sub}>This sets your focus mode.</Body>
      <View style={styles.options}>
        {GOAL_OPTIONS.map((opt) => (
          <ChoiceCard
            key={opt.mode}
            label={opt.label}
            selected={mode === opt.mode}
            onPress={() => setGoal(opt.mode, opt.projection)}
          />
        ))}
      </View>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  title: {
    marginTop: spacing.md,
  },
  sub: {
    marginTop: spacing.sm,
  },
  options: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
});
