import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import { Body, Button, Display, KickerLabel, Screen } from '@/components';
import { useProfileStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

export default function FriendsTab() {
  const phase = useProfileStore((s) => s.phase);

  return (
    <Screen style={styles.screen}>
      <View style={styles.header}>
        <KickerLabel>Friends</KickerLabel>
        <Display style={styles.headline}>
          {phase === 'day1' ? 'Lock in together.' : 'This week’s leaderboard'}
        </Display>
      </View>

      {phase === 'day1' ? (
        <View style={styles.flex}>
          {/* Obscured preview — decorative placeholder rows, never fake people. */}
          <View style={styles.preview} pointerEvents="none">
            {[0, 1, 2, 3].map((i) => (
              <View key={i} style={styles.previewRow}>
                <Text style={styles.rank}>{i + 1}</Text>
                <View style={[styles.skelName, { width: `${60 - i * 8}%` }]} />
                <View style={styles.skelScore} />
              </View>
            ))}
          </View>

          <View style={styles.lockOverlay}>
            <Text style={styles.lockGlyph}>🔒</Text>
            <Body color={colors.cream} style={styles.lockText}>
              Add 1 friend to unlock the weekly leaderboard.
            </Body>
          </View>

          <View style={styles.footer}>
            <Button
              label="Add a friend"
              onPress={() => router.push('/invite')}
              accessibilityHint="Open the invite screen"
            />
          </View>
        </View>
      ) : (
        <View style={styles.emptyEstablished}>
          <Text style={styles.emptyGlyph}>🏁</Text>
          <Body color={colors.cream} style={styles.emptyTitle}>
            No friends on the board yet.
          </Body>
          <Body style={styles.emptyText}>
            Invite someone and your weekly leaderboard starts here. (Live rankings
            arrive with the social update.)
          </Body>
          <Button
            label="Invite a friend"
            variant="secondary"
            onPress={() => router.push('/invite')}
            style={styles.emptyBtn}
          />
        </View>
      )}
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  header: {
    paddingTop: spacing.lg,
    marginBottom: spacing.xl,
  },
  headline: {
    marginTop: spacing.sm,
  },
  preview: {
    gap: spacing.sm,
    opacity: 0.35,
  },
  previewRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.base,
    padding: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.ink,
  },
  rank: {
    fontFamily: fontFamily.monoBold,
    fontSize: 16,
    color: colors.muted,
    width: 20,
  },
  skelName: {
    height: 14,
    borderRadius: radius.pill,
    backgroundColor: colors.muted,
  },
  skelScore: {
    height: 14,
    width: 44,
    marginLeft: 'auto',
    borderRadius: radius.pill,
    backgroundColor: colors.muted,
  },
  lockOverlay: {
    alignItems: 'center',
    gap: spacing.md,
    marginTop: spacing['2xl'],
    paddingHorizontal: spacing.xl,
  },
  lockGlyph: {
    fontSize: 34,
  },
  lockText: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 19,
    lineHeight: 26,
    textAlign: 'center',
  },
  footer: {
    marginTop: 'auto',
    paddingBottom: spacing.sm,
  },
  emptyEstablished: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.md,
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing['4xl'],
  },
  emptyGlyph: {
    fontSize: 40,
  },
  emptyTitle: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 20,
    textAlign: 'center',
  },
  emptyText: {
    fontSize: 15,
    lineHeight: 22,
    textAlign: 'center',
  },
  emptyBtn: {
    marginTop: spacing.base,
  },
});
