import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import {
  Body,
  Button,
  Card,
  Display,
  KickerLabel,
  OnboardingScreen,
  Pill,
  Title,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { spacing } from '@/theme';

const FEATURES = [
  { title: 'The Seal', body: 'Lock distracting apps for the length of a focus session.' },
  { title: 'Deep-work tracking', body: 'Every sealed hour counts toward your daily goal.' },
  { title: 'Streaks & ranks', body: 'Show up daily, build a streak, climb the ranks.' },
  { title: 'Duels', body: 'Head-to-head focus challenges with friends.', soon: true },
];

export default function Features() {
  return (
    <OnboardingScreen
      progress={PROGRESS.features}
      footer={
        <Button label="Build my plan" onPress={() => router.push('/plan')} />
      }
    >
      <KickerLabel>What you get</KickerLabel>
      <Display style={styles.headline}>Built to make focus stick.</Display>
      <View style={styles.grid}>
        {FEATURES.map((f) => (
          <Card key={f.title} style={styles.card}>
            <View style={styles.cardHead}>
              <Title style={styles.cardTitle}>{f.title}</Title>
              {f.soon && <Pill label="v1.1" tone="teal" />}
            </View>
            <Body style={styles.cardCopy}>{f.body}</Body>
          </Card>
        ))}
      </View>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  grid: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
  card: {
    gap: spacing.sm,
  },
  cardHead: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.sm,
  },
  cardTitle: {
    fontSize: 19,
  },
  cardCopy: {
    fontSize: 15,
    lineHeight: 21,
  },
});
