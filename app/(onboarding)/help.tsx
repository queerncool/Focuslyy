import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Card,
  Display,
  KickerLabel,
  OnboardingScreen,
  Title,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { colors, fontFamily, spacing } from '@/theme';

const STEPS = [
  { n: '1', title: 'Seal the apps', body: 'Lock what pulls you out — TikTok, IG, games, whatever steals your focus.' },
  { n: '2', title: 'Do deep work', body: 'A timer runs. Your apps stay sealed. One task, no escape hatch.' },
  { n: '3', title: 'See it add up', body: 'focuslyy turns those hours into streaks, stats, and proof you can share.' },
];

export default function Help() {
  return (
    <OnboardingScreen
      progress={PROGRESS.help}
      footer={
        <Button
          label="Your focus starts now"
          onPress={() => router.push('/reviews')}
        />
      }
    >
      <KickerLabel>How focuslyy works</KickerLabel>
      <Display style={styles.headline}>Three steps. That's it.</Display>
      <View style={styles.steps}>
        {STEPS.map((step) => (
          <Card key={step.n} style={styles.card}>
            <View style={styles.badge}>
              <Text style={styles.badgeText}>{step.n}</Text>
            </View>
            <View style={styles.cardBody}>
              <Title style={styles.cardTitle}>{step.title}</Title>
              <Body style={styles.cardCopy}>{step.body}</Body>
            </View>
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
  steps: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
  card: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.base,
  },
  badge: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(242,160,61,0.14)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  badgeText: {
    fontFamily: fontFamily.monoBold,
    fontSize: 16,
    color: colors.amber,
  },
  cardBody: {
    flex: 1,
  },
  cardTitle: {
    fontSize: 18,
  },
  cardCopy: {
    marginTop: spacing.xs,
    fontSize: 15,
    lineHeight: 21,
  },
});
