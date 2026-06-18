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
import { computeHours, HOURS_BANDS, PROGRESS } from '@/lib/onboarding';
import { useQuizStore } from '@/state';
import { spacing } from '@/theme';

export default function Q1() {
  const hoursBand = useQuizStore((s) => s.hoursBand);
  const setHours = useQuizStore((s) => s.setHours);

  return (
    <OnboardingScreen
      progress={PROGRESS.q1}
      footer={
        <Button
          label="Continue"
          disabled={hoursBand == null}
          onPress={() => router.push('/q2')}
        />
      }
    >
      <KickerLabel>Question 1 of 3</KickerLabel>
      <Title style={styles.title}>How many hours a day are you on your phone?</Title>
      <Body style={styles.sub}>Be honest — no one else sees this.</Body>
      <View style={styles.options}>
        {HOURS_BANDS.map((band) => (
          <ChoiceCard
            key={band.id}
            label={band.label}
            selected={hoursBand === band.id}
            onPress={() => {
              const { yrNum, barH } = computeHours(band.hoursNum);
              setHours(band.id, band.hoursNum, yrNum, barH);
            }}
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
