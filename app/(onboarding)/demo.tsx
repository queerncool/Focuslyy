import { useEvent } from 'expo';
import { router } from 'expo-router';
import { useVideoPlayer, VideoView } from 'expo-video';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { Body, Button, KickerLabel, Screen, Title } from '@/components';
import { DEMO_VIDEO, hasDemoVideo } from '@/lib/demo';
import { colors, fontFamily, radius, spacing } from '@/theme';

export default function Demo() {
  const player = useVideoPlayer(DEMO_VIDEO, (p) => {
    // Start muted so it never cuts off the user's music; the native controls
    // can unmute.
    p.muted = true;
    p.play();
  });
  const { status } = useEvent(player, 'statusChange', { status: player.status });

  const failed = !hasDemoVideo || status === 'error';
  const loading = !failed && status !== 'readyToPlay';

  const retry = async () => {
    await player.replaceAsync(DEMO_VIDEO);
    player.play();
  };

  // Swap this modal for Q1 in one action, so back from Q1 lands on Start.
  const startQuiz = () => router.replace('/q1');

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

      <KickerLabel color={colors.amber}>How it works</KickerLabel>
      <Title style={styles.headline}>One session, start to finish.</Title>

      <View style={styles.frame}>
        {failed ? (
          <View style={styles.state}>
            <Body color={colors.cream} style={styles.stateText}>
              The demo didn't load.
            </Body>
            {hasDemoVideo && (
              <Button variant="secondary" label="Try again" onPress={retry} />
            )}
          </View>
        ) : (
          <>
            <VideoView
              player={player}
              style={StyleSheet.absoluteFill}
              contentFit="contain"
              nativeControls
              accessibilityLabel="Demo video of a focus session"
            />
            {loading && (
              <View style={styles.state} pointerEvents="none">
                <ActivityIndicator color={colors.amber} />
              </View>
            )}
          </>
        )}
      </View>

      <View style={styles.footer}>
        <Button
          label="Find out in 60 seconds"
          onPress={startQuiz}
          accessibilityHint="Closes the demo and starts a 60-second quiz"
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
    paddingBottom: spacing.sm,
  },
  close: {
    fontFamily: fontFamily.display,
    fontSize: 22,
    color: colors.muted,
    padding: spacing.xs,
  },
  headline: {
    marginTop: spacing.sm,
  },
  frame: {
    flex: 1,
    marginTop: spacing.lg,
    borderRadius: radius.xl,
    overflow: 'hidden',
    backgroundColor: colors.ink,
  },
  state: {
    ...StyleSheet.absoluteFill,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.base,
    padding: spacing.lg,
  },
  stateText: {
    textAlign: 'center',
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
  },
});
