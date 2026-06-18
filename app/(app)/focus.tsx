import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  Pill,
  RingTimer,
  Screen,
} from '@/components';
import { formatDuration, todayMinutes } from '@/lib/time';
import { currentStreak } from '@/lib/stats';
import { useProfileStore, useSessionsHistoryStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

function greetingFor(name: string): string {
  const h = new Date().getHours();
  const part = h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening';
  return name.trim() ? `${part}, ${name.trim()}` : part;
}

export default function FocusTab() {
  const name = useProfileStore((s) => s.name);
  const dailyGoal = useProfileStore((s) => s.dailyGoal);
  const phase = useProfileStore((s) => s.phase);
  const sessions = useSessionsHistoryStore((s) => s.sessions);

  const todayMin = todayMinutes(sessions);
  const goalMin = Math.max(1, dailyGoal * 60);
  const progress = Math.min(1, todayMin / goalMin);
  const streak = currentStreak(sessions);
  const pct = Math.round(progress * 100);

  return (
    <Screen style={styles.screen}>
      <View style={styles.header}>
        <View style={styles.headerText}>
          <KickerLabel>focuslyy</KickerLabel>
          <Display style={styles.greeting}>{greetingFor(name)}</Display>
        </View>
        {streak > 0 && <Pill label={`🔥 ${streak}`} tone="amber" />}
      </View>

      <View style={styles.ringWrap}>
        <RingTimer
          progress={progress}
          size={240}
          strokeWidth={16}
          label={formatDuration(todayMin)}
          caption={`OF ${dailyGoal}H GOAL`}
        />
        <Body style={styles.ringNote}>
          {todayMin === 0
            ? "You haven't locked in today — let's change that."
            : pct >= 100
              ? "Goal hit. Everything past here is a bonus."
              : `${pct}% of today's goal.`}
        </Body>
      </View>

      <View style={styles.spacer} />

      {phase === 'day1' ? (
        <Pressable
          accessibilityRole="button"
          accessibilityHint="Invite a friend to start a leaderboard"
          onPress={() => router.push('/invite')}
          style={styles.inviteCard}
        >
          <View style={styles.inviteBody}>
            <KickerLabel color={colors.amber}>Better with friends</KickerLabel>
            <Text style={styles.inviteText}>
              Add a friend to start a streak you won't want to break.
            </Text>
          </View>
          <Text style={styles.arrow}>→</Text>
        </Pressable>
      ) : (
        <View style={styles.friendsEmpty}>
          <KickerLabel>Friends</KickerLabel>
          <Body style={styles.friendsEmptyText}>
            No friend activity yet. Invite someone and their sessions show up here.
          </Body>
          <Button
            label="Invite a friend"
            variant="secondary"
            onPress={() => router.push('/invite')}
          />
        </View>
      )}

      <View style={styles.footer}>
        <Button
          label="Begin deep work"
          onPress={() => router.push('/setSession')}
          accessibilityHint="Set up and start a focus session"
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    paddingTop: spacing.lg,
    gap: spacing.sm,
  },
  headerText: {
    flexShrink: 1,
  },
  greeting: {
    marginTop: spacing.sm,
  },
  ringWrap: {
    alignItems: 'center',
    marginTop: spacing['2xl'],
    gap: spacing.base,
  },
  ringNote: {
    fontSize: 15,
    textAlign: 'center',
    paddingHorizontal: spacing.lg,
  },
  spacer: {
    flex: 1,
    minHeight: spacing.lg,
  },
  inviteCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.base,
    padding: spacing.lg,
    borderRadius: radius.xl,
    borderWidth: 1.5,
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
  },
  inviteBody: {
    flex: 1,
    gap: spacing.xs,
  },
  inviteText: {
    fontFamily: fontFamily.display,
    fontSize: 16,
    lineHeight: 22,
    color: colors.cream,
  },
  arrow: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 28,
    color: colors.amber,
  },
  friendsEmpty: {
    padding: spacing.lg,
    borderRadius: radius.xl,
    backgroundColor: colors.ink,
    gap: spacing.md,
  },
  friendsEmptyText: {
    fontSize: 15,
    lineHeight: 21,
  },
  footer: {
    paddingTop: spacing.lg,
    paddingBottom: spacing.sm,
  },
});
