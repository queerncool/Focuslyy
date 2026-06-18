import { router } from 'expo-router';
import { StyleSheet, View } from 'react-native';
import { Body, Button, Display, KickerLabel, Screen } from '@/components';
import { useProfileStore } from '@/state';
import { spacing } from '@/theme';

/**
 * Home (Focus) — Phase 3 keeps this minimal: just the entry into the session
 * loop. The full Home (goal ring, streak chip, Day-1 vs Established friends
 * row) is built in Phase 4.
 */
export default function FocusTab() {
  const name = useProfileStore((s) => s.name);
  const greeting = name.trim() ? `Ready, ${name.trim()}?` : 'Ready to lock in?';

  return (
    <Screen style={styles.screen}>
      <View style={styles.body}>
        <KickerLabel>focuslyy</KickerLabel>
        <Display style={styles.headline}>{greeting}</Display>
        <Body style={styles.sub}>
          Seal the apps, do the one thing that matters, and watch the hours add up.
        </Body>
      </View>

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
  body: {
    flex: 1,
    justifyContent: 'center',
  },
  headline: {
    marginTop: spacing.sm,
  },
  sub: {
    marginTop: spacing.base,
    fontSize: 17,
    lineHeight: 25,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
