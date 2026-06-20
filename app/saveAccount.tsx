import { router, useLocalSearchParams } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Body, Button, Display, KickerLabel, Screen } from '@/components';
import { haptic } from '@/lib/haptics';
import { useProfileStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';
import type { AuthProvider } from '@/types';

/**
 * Account-save prompt (§B.5). Reached after a (stubbed) purchase and from the
 * persistent Profile card. Real Apple/Google sign-in needs a native dev build,
 * so here it's simulated — linking the local profile to a provider — and the
 * real SDK wiring lands in Phase 7.
 */
export default function SaveAccount() {
  const { next } = useLocalSearchParams<{ next?: string }>();
  const linkAccount = useProfileStore((s) => s.linkAccount);
  const subscriptionStatus = useProfileStore((s) => s.subscriptionStatus);

  const subscribed = subscriptionStatus === 'active';

  const proceed = () => {
    if (next === 'firstSeal') {
      router.replace('/firstSeal');
    } else if (router.canGoBack()) {
      router.back();
    } else {
      router.replace('/(app)/profile');
    }
  };

  const linkWith = (provider: Exclude<AuthProvider, 'anonymous'>) => {
    haptic.success();
    linkAccount(provider);
    proceed();
  };

  return (
    <Screen style={styles.screen}>
      <View style={styles.topBar}>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel="Close"
          onPress={proceed}
          hitSlop={12}
        >
          <Text style={styles.close}>✕</Text>
        </Pressable>
      </View>

      <View style={styles.body}>
        <KickerLabel color={colors.amber}>Save your progress</KickerLabel>
        <Display style={styles.headline}>
          {subscribed
            ? 'Save your subscription and streak.'
            : "Keep your streak — don't lose it."}
        </Display>
        <Body style={styles.sub}>
          Sign in so your hours, streak, and {subscribed ? 'plan' : 'sessions'} are
          safe if you switch phones. One tap — no password.
        </Body>

        <View style={styles.buttons}>
          <Button label=" Sign in with Apple" onPress={() => linkWith('apple')} />
          <Button
            label="Continue with Google"
            variant="secondary"
            onPress={() => linkWith('google')}
          />
        </View>

        <Text style={styles.devNote}>
          Sign-in is simulated until the native build (Phase 7).
        </Text>
      </View>

      <View style={styles.footer}>
        <Button label="Not now" variant="tertiary" onPress={proceed} />
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
    justifyContent: 'center',
  },
  headline: {
    marginTop: spacing.sm,
  },
  sub: {
    marginTop: spacing.md,
    fontSize: 16,
    lineHeight: 23,
  },
  buttons: {
    marginTop: spacing['2xl'],
    gap: spacing.md,
  },
  devNote: {
    marginTop: spacing.lg,
    fontFamily: fontFamily.mono,
    fontSize: 12,
    color: colors.muted,
    textAlign: 'center',
  },
  footer: {
    paddingBottom: spacing.sm,
  },
});
