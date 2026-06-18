import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { colors, fontFamily, radius, spacing } from '@/theme';

export default function Discount() {
  return (
    <OnboardingScreen
      progress={PROGRESS.discount}
      footer={
        <>
          <Button
            label="Claim my offer"
            onPress={() => router.push('/firstSeal')}
          />
          <Button
            label="No thanks"
            variant="tertiary"
            onPress={() => router.push('/firstSeal')}
          />
        </>
      }
    >
      <KickerLabel>One-time offer</KickerLabel>
      <Display style={styles.headline}>Wait — start for less.</Display>
      <Body style={styles.sub}>
        Take your first month at a lower price. Cancel anytime — we're not here
        to trap you.
      </Body>

      <View style={styles.offer}>
        <View style={styles.priceRow}>
          <Text style={styles.was}>$10</Text>
          <Text style={styles.now}>$5</Text>
        </View>
        <KickerLabel color={colors.amber}>first month</KickerLabel>
      </View>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  sub: {
    marginTop: spacing.md,
    fontSize: 16,
  },
  offer: {
    marginTop: spacing['2xl'],
    padding: spacing.xl,
    borderRadius: radius.xl,
    borderWidth: 1.5,
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.10)',
    alignItems: 'center',
    gap: spacing.sm,
  },
  priceRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: spacing.base,
  },
  was: {
    fontFamily: fontFamily.mono,
    fontSize: 24,
    color: colors.muted,
    textDecorationLine: 'line-through',
  },
  now: {
    fontFamily: fontFamily.monoBold,
    fontSize: 48,
    color: colors.amberLight,
  },
});
