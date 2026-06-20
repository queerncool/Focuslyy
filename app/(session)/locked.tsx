import { useEffect } from 'react';
import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  runOnJS,
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from 'react-native-reanimated';
import { KickerLabel, Pill, RingTimer } from '@/components';
import { formatClock } from '@/lib/time';
import { useCountdown } from '@/lib/useCountdown';
import { haptic } from '@/lib/haptics';
import { applyShield } from '@/lib/blocking';
import { useSessionStore } from '@/state';
import { colors, fontFamily, gradients, radius, spacing } from '@/theme';

const HOLD_MS = 1500;

export default function Locked() {
  const task = useSessionStore((s) => s.task);
  const blockMin = useSessionStore((s) => s.blockMin);
  const blockedApps = useSessionStore((s) => s.blockedApps);
  const start = useSessionStore((s) => s.start);

  // Stamp the real start time and raise the shield once, on entry. The shield
  // stays up through the break and only lifts when the session is logged.
  useEffect(() => {
    start();
    applyShield(blockedApps);
  }, [start, blockedApps]);

  const totalSec = blockMin * 60;
  const remaining = useCountdown(totalSec, () => {
    haptic.success();
    router.replace('/break');
  });
  const progress = totalSec > 0 ? remaining / totalSec : 0;

  const fill = useSharedValue(0);
  const fillStyle = useAnimatedStyle(() => ({ width: `${fill.value * 100}%` }));

  const breakSeal = () => {
    haptic.warning();
    router.replace({ pathname: '/logWin', params: { broke: '1' } });
  };

  const hold = Gesture.LongPress()
    .minDuration(HOLD_MS)
    .onBegin(() => {
      fill.value = withTiming(1, { duration: HOLD_MS });
    })
    .onStart(() => {
      runOnJS(breakSeal)();
    })
    .onFinalize(() => {
      fill.value = withTiming(0, { duration: 200 });
    });

  const count = blockedApps.length;
  const taskLabel = task.trim();

  return (
    <View style={styles.root}>
      <LinearGradient colors={gradients.locked} style={StyleSheet.absoluteFill} />
      <View style={styles.inner}>
        <Pill label={`Phone sealed · ${count} blocked`} tone="amber" />

        <View style={styles.ring}>
          <RingTimer
            progress={progress}
            size={280}
            strokeWidth={16}
            label={formatClock(remaining)}
            caption="REMAINING"
          />
        </View>

        <View style={styles.taskWrap}>
          <KickerLabel color={colors.muted}>
            {taskLabel ? "You're working on" : 'Deep work in progress'}
          </KickerLabel>
          {taskLabel ? (
            <Text style={styles.task}>{taskLabel}</Text>
          ) : null}
        </View>

        <GestureDetector gesture={hold}>
          <View
            accessibilityRole="button"
            accessibilityLabel="Hold to break the seal"
            accessibilityHint="Press and hold to end this session early"
            style={styles.breakTrack}
          >
            <Animated.View style={[styles.breakFill, fillStyle]} />
            <Text style={styles.breakText}>Hold to break the seal</Text>
          </View>
        </GestureDetector>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    flex: 1,
    backgroundColor: colors.espresso,
  },
  inner: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing['4xl'],
    paddingBottom: spacing['3xl'],
  },
  ring: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  taskWrap: {
    alignItems: 'center',
    gap: spacing.sm,
    paddingHorizontal: spacing.base,
  },
  task: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 22,
    lineHeight: 28,
    color: colors.cream,
    textAlign: 'center',
  },
  breakTrack: {
    width: '100%',
    minHeight: 56,
    borderRadius: radius.pill,
    borderWidth: 1.5,
    borderColor: 'rgba(229,86,75,0.5)',
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
  },
  breakFill: {
    position: 'absolute',
    left: 0,
    top: 0,
    bottom: 0,
    backgroundColor: 'rgba(229,86,75,0.28)',
  },
  breakText: {
    fontFamily: fontFamily.mono,
    fontSize: 14,
    letterSpacing: 1,
    color: colors.crimson,
    textTransform: 'uppercase',
  },
});
