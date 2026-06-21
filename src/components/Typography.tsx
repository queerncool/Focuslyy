import {
  StyleSheet,
  Text,
  type StyleProp,
  type TextStyle,
} from 'react-native';
import { colors, fontFamily } from '@/theme';

interface TextProps {
  children: React.ReactNode;
  style?: StyleProp<TextStyle>;
  color?: string;
}

/** Big hero headline — Schibsted ExtraBold. */
export function Display({ children, style, color = colors.cream }: TextProps) {
  return <Text style={[styles.display, { color }, style]}>{children}</Text>;
}

/** Section/screen title — Schibsted ExtraBold, smaller. */
export function Title({ children, style, color = colors.cream }: TextProps) {
  return <Text style={[styles.title, { color }, style]}>{children}</Text>;
}

/** Body / subhead copy — Schibsted Bold, muted by default. */
export function Body({ children, style, color = colors.muted }: TextProps) {
  return <Text style={[styles.body, { color }, style]}>{children}</Text>;
}

/** Fraunces Black Italic accent — onboarding hero moments only. */
export function Accent({ children, style, color = colors.amber }: TextProps) {
  return <Text style={[styles.accent, { color }, style]}>{children}</Text>;
}

const styles = StyleSheet.create({
  display: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 34,
    lineHeight: 41,
    letterSpacing: -0.8,
  },
  title: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 24,
    lineHeight: 30,
    letterSpacing: -0.5,
  },
  body: {
    fontFamily: fontFamily.display,
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0.1,
  },
  accent: {
    fontFamily: fontFamily.accent,
    fontSize: 30,
  },
});
