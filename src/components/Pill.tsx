import {
  StyleSheet,
  Text,
  View,
  type StyleProp,
  type ViewStyle,
} from 'react-native';
import { colors, fontFamily, radius, spacing } from '@/theme';

type Tone = 'amber' | 'teal' | 'crimson' | 'muted';

interface PillProps {
  label: string;
  tone?: Tone;
  style?: StyleProp<ViewStyle>;
}

const TONE: Record<Tone, { fg: string; bg: string }> = {
  amber: { fg: colors.amber, bg: 'rgba(242,160,61,0.14)' },
  teal: { fg: colors.teal, bg: 'rgba(79,182,160,0.14)' },
  crimson: { fg: colors.crimson, bg: 'rgba(229,86,75,0.14)' },
  muted: { fg: colors.muted, bg: 'rgba(140,129,116,0.14)' },
};

/** Small status/label pill. Mono uppercase text on a tinted track. */
export function Pill({ label, tone = 'amber', style }: PillProps) {
  const t = TONE[tone];
  return (
    <View style={[styles.base, { backgroundColor: t.bg }, style]}>
      <Text style={[styles.label, { color: t.fg }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    alignSelf: 'flex-start',
    borderRadius: radius.pill,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs + 2,
  },
  label: {
    fontFamily: fontFamily.monoBold,
    fontSize: 12,
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
});
