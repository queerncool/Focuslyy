import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  KickerLabel,
  Screen,
  SegmentedOption,
  Title,
} from '@/components';
import { formatDuration } from '@/lib/time';
import { currentStreak, longestStreak, totalMinutes, totalXp } from '@/lib/stats';
import { displayHandle, initialOf } from '@/lib/user';
import { useProfileStore, useSessionsHistoryStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

const GOAL_OPTIONS = [
  { value: 1, label: '1H' },
  { value: 2, label: '2H' },
  { value: 3, label: '3H' },
  { value: 4, label: '4H' },
];

const PHASE_OPTIONS = [
  { value: 'day1' as const, label: 'Day-1' },
  { value: 'established' as const, label: 'Established' },
];

export default function ProfileTab() {
  const name = useProfileStore((s) => s.name);
  const handle = useProfileStore((s) => s.handle);
  const authProvider = useProfileStore((s) => s.authProvider);
  const dailyGoal = useProfileStore((s) => s.dailyGoal);
  const commitDays = useProfileStore((s) => s.commitDays);
  const phase = useProfileStore((s) => s.phase);
  const setPlan = useProfileStore((s) => s.setPlan);
  const setPhase = useProfileStore((s) => s.setPhase);

  const sessions = useSessionsHistoryStore((s) => s.sessions);
  const streak = currentStreak(sessions);
  const best = longestStreak(sessions);
  const banked = totalMinutes(sessions);
  const xp = totalXp(sessions);

  const isAnonymous = authProvider === 'anonymous';

  const promptSignIn = () =>
    Alert.alert(
      'Save your progress',
      'Sign in with Apple arrives in the next update — your streak and sessions are safe on this device until then.'
    );

  return (
    <Screen style={styles.screen}>
      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.identity}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{initialOf(name)}</Text>
          </View>
          <Title>{name.trim() || 'You'}</Title>
          <Text style={styles.handle}>@{displayHandle(name, handle)}</Text>
        </View>

        {isAnonymous && (
          <Pressable
            accessibilityRole="button"
            onPress={promptSignIn}
            style={styles.saveCard}
          >
            <View style={styles.saveBody}>
              <KickerLabel color={colors.amber}>Save your progress</KickerLabel>
              <Text style={styles.saveText}>Sign in with Apple to keep your streak safe.</Text>
            </View>
            <Text style={styles.arrow}>→</Text>
          </Pressable>
        )}

        <View style={styles.statRow}>
          <Stat label="STREAK" value={`🔥 ${streak}`} />
          <Stat label="BEST" value={`${best}`} />
          <Stat label="BANKED" value={formatDuration(banked)} />
          <Stat label="XP" value={`${xp}`} />
        </View>

        <View style={styles.section}>
          <KickerLabel>Daily goal</KickerLabel>
          <SegmentedOption
            options={GOAL_OPTIONS}
            value={dailyGoal}
            onChange={(v) => setPlan(v, commitDays)}
          />
        </View>

        <View style={styles.section}>
          <KickerLabel>View as (dev)</KickerLabel>
          <Body style={styles.devNote}>
            Switch between the brand-new and established experiences across the app.
          </Body>
          <SegmentedOption options={PHASE_OPTIONS} value={phase} onChange={setPhase} />
        </View>

        {isAnonymous && (
          <Button
            label="Save your progress"
            variant="secondary"
            onPress={promptSignIn}
            style={styles.signInBtn}
            accessibilityHint="Sign in to save your streak and sessions"
          />
        )}
      </ScrollView>
    </Screen>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.stat}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  content: {
    paddingTop: spacing.xl,
    paddingBottom: spacing['2xl'],
  },
  identity: {
    alignItems: 'center',
    gap: spacing.sm,
  },
  avatar: {
    width: 76,
    height: 76,
    borderRadius: radius.pill,
    backgroundColor: colors.amber,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.xs,
  },
  avatarText: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 34,
    color: colors.espresso,
  },
  handle: {
    fontFamily: fontFamily.mono,
    fontSize: 14,
    color: colors.muted,
  },
  saveCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.base,
    marginTop: spacing.xl,
    padding: spacing.lg,
    borderRadius: radius.xl,
    borderWidth: 1.5,
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
  },
  saveBody: {
    flex: 1,
    gap: spacing.xs,
  },
  saveText: {
    fontFamily: fontFamily.display,
    fontSize: 15,
    lineHeight: 21,
    color: colors.cream,
  },
  arrow: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 26,
    color: colors.amber,
  },
  statRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.xl,
  },
  stat: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
    gap: spacing.xs,
  },
  statValue: {
    fontFamily: fontFamily.monoBold,
    fontSize: 16,
    color: colors.amberLight,
  },
  statLabel: {
    fontFamily: fontFamily.mono,
    fontSize: 9,
    letterSpacing: 1,
    color: colors.muted,
  },
  section: {
    marginTop: spacing['2xl'],
    gap: spacing.md,
  },
  devNote: {
    fontSize: 13,
    lineHeight: 19,
  },
  signInBtn: {
    marginTop: spacing['2xl'],
  },
});
