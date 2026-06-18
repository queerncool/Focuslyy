import { router } from 'expo-router';
import { Pressable, Share, StyleSheet, Text, View } from 'react-native';
import { Body, Button, Display, KickerLabel, ProgressBar, Screen } from '@/components';
import { haptic } from '@/lib/haptics';
import { displayHandle } from '@/lib/user';
import { useProfileStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

const GOAL_JOINS = 3;

export default function Invite() {
  const name = useProfileStore((s) => s.name);
  const handle = useProfileStore((s) => s.handle);

  const username = displayHandle(name, handle);
  const link = `focuslyy.app/r/${username}`;
  const message = `I'm sealing my distracting apps and doing real deep work with focuslyy. Come lock in with me → https://${link}`;

  // No friends backend yet (Phase 7), so joins are honestly zero.
  const joined = 0;

  const shareInvite = async () => {
    haptic.medium();
    try {
      await Share.share({ message });
    } catch {
      /* dismissed — no-op */
    }
  };

  return (
    <Screen style={styles.screen}>
      <View style={styles.topBar}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Close"
          onPress={() => router.back()}
          hitSlop={12}
        >
          <Text style={styles.close}>✕</Text>
        </Pressable>
      </View>

      <View style={styles.body}>
        <KickerLabel color={colors.amber}>Invite</KickerLabel>
        <Display style={styles.headline}>Bring a friend. Keep each other honest.</Display>

        <View style={styles.linkCard}>
          <KickerLabel>Your invite link</KickerLabel>
          <Text style={styles.link} selectable>
            {link}
          </Text>
        </View>

        <View style={styles.msgCard}>
          <KickerLabel>They'll see</KickerLabel>
          <Body color={colors.cream} style={styles.msgText}>
            {message}
          </Body>
        </View>

        <View style={styles.progressWrap}>
          <View style={styles.progressLabels}>
            <Text style={styles.progressText}>{joined} of {GOAL_JOINS} joined</Text>
            <Text style={styles.progressHint}>Unlock the leaderboard at 1</Text>
          </View>
          <ProgressBar progress={(joined / GOAL_JOINS) * 100} />
        </View>
      </View>

      <View style={styles.footer}>
        <Button
          label="Share my invite link"
          onPress={shareInvite}
          accessibilityHint="Open the share sheet with your invite link"
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    paddingTop: spacing.sm,
  },
  close: {
    fontFamily: fontFamily.display,
    fontSize: 22,
    color: colors.muted,
    padding: spacing.xs,
  },
  body: {
    flex: 1,
    paddingTop: spacing.base,
  },
  headline: {
    marginTop: spacing.sm,
  },
  linkCard: {
    marginTop: spacing['2xl'],
    padding: spacing.lg,
    borderRadius: radius.xl,
    borderWidth: 1.5,
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
    gap: spacing.sm,
  },
  link: {
    fontFamily: fontFamily.monoBold,
    fontSize: 18,
    color: colors.amberLight,
  },
  msgCard: {
    marginTop: spacing.base,
    padding: spacing.lg,
    borderRadius: radius.xl,
    backgroundColor: colors.ink,
    gap: spacing.sm,
  },
  msgText: {
    fontSize: 15,
    lineHeight: 22,
  },
  progressWrap: {
    marginTop: spacing['2xl'],
    gap: spacing.sm,
  },
  progressLabels: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'baseline',
  },
  progressText: {
    fontFamily: fontFamily.monoBold,
    fontSize: 14,
    color: colors.cream,
  },
  progressHint: {
    fontFamily: fontFamily.mono,
    fontSize: 12,
    color: colors.muted,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
