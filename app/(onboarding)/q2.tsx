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
import { DISTRACTION_OPTIONS, PROGRESS } from '@/lib/onboarding';
import { useQuizStore } from '@/state';
import { spacing } from '@/theme';

export default function Q2() {
  const distractions = useQuizStore((s) => s.distractions);
  const toggleDistraction = useQuizStore((s) => s.toggleDistraction);

  return (
    <OnboardingScreen
      progress={PROGRESS.q2}
      footer={
        <Button
          label="Continue"
          disabled={distractions.length === 0}
          onPress={() => router.push('/q3')}
        />
      }
    >
      <KickerLabel>Question 2 of 3</KickerLabel>
      <Title style={styles.title}>What steals your focus most?</Title>
      <Body style={styles.sub}>Pick all that pull you in.</Body>
      <View style={styles.options}>
        {DISTRACTION_OPTIONS.map((opt) => (
          <ChoiceCard
            key={opt.id}
            mode="multi"
            label={opt.label}
            selected={distractions.includes(opt.id)}
            onPress={() => toggleDistraction(opt.id)}
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
