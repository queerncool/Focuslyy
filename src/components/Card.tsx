import type { ReactNode } from 'react';
import {
  StyleSheet,
  View,
  type StyleProp,
  type ViewStyle,
} from 'react-native';
import { border, colors, elevation, radius, spacing } from '@/theme';

interface CardProps {
  children: ReactNode;
  /** 'dark' renders on espresso bg (ink card); 'light' on cream bg. */
  tone?: 'dark' | 'light';
  style?: StyleProp<ViewStyle>;
}

/** Rounded surface container. Tone picks the locked surface color. */
export function Card({ children, tone = 'dark', style }: CardProps) {
  return (
    <View
      style={[
        styles.base,
        tone === 'dark' ? styles.dark : styles.light,
        style,
      ]}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: radius.xl,
    padding: spacing.xl,
    borderWidth: StyleSheet.hairlineWidth,
  },
  dark: {
    backgroundColor: colors.ink,
    borderColor: border.hairline,
    ...elevation.sm,
  },
  light: {
    backgroundColor: colors.cream,
    borderColor: border.onLight,
    ...elevation.sm,
  },
});
