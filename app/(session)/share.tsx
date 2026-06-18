import { router } from 'expo-router';
import { Share, StyleSheet, Text, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Button, KickerLabel, Screen } from '@/components';
import { formatDuration, todayMinutes } from '@/lib/time';
import { haptic } from '@/lib/haptics';
import {
  useProfileStore,
  useSessionStore,
  useSessionsHistoryStore,
} from '@/state';
import { colors, fontFamily, gradients, radius, spacing } from '@/theme';

export default function ShareScreen() {
  const sessions = useSessionsHistoryStore((s) => s.sessions);
  const streakDays = useProfileStore((s) => s.streakDays);
  const clearSession = useSessionStore((s) => s.clear);

  const totalToday = formatDuration(todayMinutes(sessions));
  const streak = Math.max(streakDays, 1);

  const finish = () => {
    clearSession();
    router.replace('/focus');
  };

  const shareDay = async () => {
    haptic.medium();
    const streakLine = streak > 1 ? ` · ${streak}-day streak` : '';
    try {
      // Built-in system share sheet (real intent, no extra deps). Rendering the
      // card to an image for an Instagram-Story-specific share is Phase 6/7.
      await Share.share({
        message: `Today I locked in for ${totalToday} of deep work${streakLine}.\nSeal the apps. Do deep work.\nfocuslyy.app`,
      });
    } catch {
      /* user dismissed the sheet — no-op */
    }
  };

  return (
    <Screen style={styles.screen}>
      <View style={styles.body}>
        <KickerLabel color={colors.amber}>Share your day</KickerLabel>

        {/* Branded share-card preview */}
        <View style={styles.card}>
          <LinearGradient
            colors={gradients.locked}
            style={StyleSheet.absoluteFill}
          />
          <KickerLabel color={colors.muted}>Today I locked in for</KickerLabel>
          <Text style={styles.total}>{totalToday}</Text>
          <Text style={styles.sub}>of deep work · 🔥{streak}-day streak</Text>

          <View style={styles.cardFooter}>
            <Text style={styles.tagline}>Seal the apps. Do deep work.</Text>
            <Text style={styles.handle}>@focuslyy · focuslyy.app</Text>
          </View>
        </View>
      </View>

      <View style={styles.footer}>
        <Button
          label="Share my day"
          onPress={shareDay}
          accessibilityHint="Open the share sheet with your day's card"
        />
        <Button label="Done" variant="tertiary" onPress={finish} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  body: {
    flex: 1,
    justifyContent: 'center',
    gap: spacing.lg,
  },
  card: {
    borderRadius: radius['2xl'],
    overflow: 'hidden',
    padding: spacing.xl,
    borderWidth: 1.5,
    borderColor: 'rgba(242,160,61,0.4)',
    gap: spacing.xs,
  },
  total: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 56,
    lineHeight: 60,
    color: colors.amber,
    marginTop: spacing.sm,
  },
  sub: {
    fontFamily: fontFamily.mono,
    fontSize: 14,
    color: colors.cream,
    letterSpacing: 0.5,
  },
  cardFooter: {
    marginTop: spacing['2xl'],
    gap: spacing.xs,
  },
  tagline: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 18,
    color: colors.cream,
  },
  handle: {
    fontFamily: fontFamily.mono,
    fontSize: 12,
    color: colors.muted,
    letterSpacing: 1,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
    gap: spacing.sm,
  },
});
