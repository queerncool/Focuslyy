import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Card,
  Display,
  KickerLabel,
  OnboardingScreen,
  Pill,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { colors, fontFamily, spacing } from '@/theme';

export default function Reviews() {
  return (
    <OnboardingScreen
      progress={PROGRESS.reviews}
      footer={
        <Button label="Continue" onPress={() => router.push('/features')} />
      }
    >
      <KickerLabel>You're not alone</KickerLabel>
      {/*
        Principle #5 — no fake social proof. The waitlist count wires to the
        real Supabase number in Phase 7; until then it's an explicit placeholder,
        never an invented figure.
      */}
      <Display style={styles.headline}>
        <Text style={styles.count}>[X]</Text> people are taking their focus back.
      </Display>
      <View style={styles.note}>
        <Pill label="Placeholder" tone="muted" />
        <Body style={styles.noteText}>
          Live waitlist count lands when the backend is wired (Phase 7).
        </Body>
      </View>

      <View style={styles.reviews}>
        <ReviewCard />
        <ReviewCard />
      </View>
    </OnboardingScreen>
  );
}

/** Explicitly-labeled placeholder — replaced with a REAL founding-member quote before launch. */
function ReviewCard() {
  return (
    <Card style={styles.review}>
      <View style={styles.reviewTop}>
        <Text style={styles.stars}>★★★★★</Text>
        <Pill label="Placeholder" tone="muted" />
      </View>
      <Body color={colors.cream} style={styles.quote}>
        Real founding-member quote goes here before launch.
      </Body>
    </Card>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  count: {
    fontFamily: fontFamily.displayHeavy,
    color: colors.amber,
  },
  note: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    marginTop: spacing.base,
  },
  noteText: {
    flex: 1,
    fontSize: 13,
  },
  reviews: {
    marginTop: spacing['2xl'],
    gap: spacing.md,
  },
  review: {
    gap: spacing.sm,
  },
  reviewTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  stars: {
    color: colors.amber,
    fontSize: 18,
    letterSpacing: 2,
  },
  quote: {
    fontSize: 16,
    lineHeight: 23,
    fontStyle: 'italic',
  },
});
