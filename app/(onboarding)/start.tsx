import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import {
  Accent,
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
  RingTimer,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { spacing } from '@/theme';

export default function Start() {
  return (
    <OnboardingScreen
      progress={PROGRESS.start}
      footer={
        <Button
          label="Find out in 60 seconds"
          onPress={() => router.push('/q1')}
          accessibilityHint="Starts a 60-second quiz"
        />
      }
    >
      <View style={styles.hero}>
        <RingTimer progress={0.72} size={150} strokeWidth={10}>
          <Accent style={styles.y}>y</Accent>
        </RingTimer>
      </View>
      <KickerLabel>focuslyy</KickerLabel>
      <Display style={styles.headline}>
        While you scroll, everyone else is building.
      </Display>
      <Body style={styles.sub}>
        The average person hands their phone 4+ hours every day. That's not a
        habit — it's a head start everyone else is taking.
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
  y: {
    fontSize: 64,
    lineHeight: 72,
  },
  headline: {
    marginTop: spacing.sm,
    fontSize: 38,
    lineHeight: 44,
  },
  sub: {
    marginTop: spacing.base,
    fontSize: 17,
    lineHeight: 25,
  },
});
