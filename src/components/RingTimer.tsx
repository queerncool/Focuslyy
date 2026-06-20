import { useEffect, useRef, type ReactNode } from 'react';
import { Animated, Easing, StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Defs, LinearGradient, Stop } from 'react-native-svg';
import { colors, fontFamily } from '@/theme';

const AnimatedCircle = Animated.createAnimatedComponent(Circle);

interface RingTimerProps {
  /** Remaining fraction of the countdown, 0..1 (1 = full ring). */
  progress: number;
  /** Outer diameter in px. */
  size?: number;
  /** Arc thickness in px. */
  strokeWidth?: number;
  /** Big centered label, e.g. a mono "24:00" timer string. */
  label?: string;
  /** Small caption under the label. */
  caption?: string;
  /** Custom centered content (overrides label/caption). */
  children?: ReactNode;
}

/**
 * Amber arc countdown ring (the Locked-screen centerpiece).
 * The arc eases to `progress` on every change, so it sweeps in on mount and
 * glides between countdown ticks instead of jumping.
 */
export function RingTimer({
  progress,
  size = 260,
  strokeWidth = 14,
  label,
  caption,
  children,
}: RingTimerProps) {
  const clamped = Math.max(0, Math.min(1, progress));
  const r = (size - strokeWidth) / 2;
  const cx = size / 2;
  const cy = size / 2;
  const circumference = 2 * Math.PI * r;

  // Animate from empty on mount, then ease toward each new progress value.
  const anim = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    Animated.timing(anim, {
      toValue: clamped,
      duration: 600,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: false,
    }).start();
  }, [clamped, anim]);

  const dashOffset = anim.interpolate({
    inputRange: [0, 1],
    outputRange: [circumference, 0],
  });

  return (
    <View
      style={{ width: size, height: size }}
      accessibilityRole="progressbar"
      accessibilityValue={{ now: Math.round(clamped * 100), min: 0, max: 100 }}
      accessibilityLabel={label ? `${label}${caption ? `, ${caption}` : ''}` : undefined}
    >
      <Svg width={size} height={size}>
        <Defs>
          <LinearGradient id="ringArc" x1="0" y1="0" x2="1" y2="1">
            <Stop offset="0" stopColor={colors.amberLight} />
            <Stop offset="1" stopColor={colors.amberDeep} />
          </LinearGradient>
        </Defs>
        {/* Track */}
        <Circle
          cx={cx}
          cy={cy}
          r={r}
          stroke={colors.ink}
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Progress arc — starts at 12 o'clock, sweeps clockwise */}
        <AnimatedCircle
          cx={cx}
          cy={cy}
          r={r}
          stroke="url(#ringArc)"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          transform={`rotate(-90 ${cx} ${cy})`}
        />
      </Svg>
      <View style={[StyleSheet.absoluteFill, styles.center]}>
        {children ?? (
          <>
            {label != null && <Text style={styles.label}>{label}</Text>}
            {caption != null && <Text style={styles.caption}>{caption}</Text>}
          </>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  label: {
    fontFamily: fontFamily.monoBold,
    fontSize: 52,
    color: colors.cream,
    letterSpacing: 1,
  },
  caption: {
    fontFamily: fontFamily.mono,
    fontSize: 13,
    color: colors.muted,
    marginTop: 4,
    letterSpacing: 1,
  },
});
