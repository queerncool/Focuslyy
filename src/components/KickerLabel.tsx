import {
  StyleSheet,
  Text,
  type StyleProp,
  type TextStyle,
} from 'react-native';
import { colors, fontFamily } from '@/theme';

interface KickerLabelProps {
  children: string;
  color?: string;
  style?: StyleProp<TextStyle>;
}

/** Mono, uppercase, wide-tracked section label (the "kicker"). */
export function KickerLabel({
  children,
  color = colors.muted,
  style,
}: KickerLabelProps) {
  return <Text style={[styles.label, { color }, style]}>{children}</Text>;
}

const styles = StyleSheet.create({
  label: {
    fontFamily: fontFamily.mono,
    fontSize: 12,
    letterSpacing: 2,
    textTransform: 'uppercase',
  },
});
