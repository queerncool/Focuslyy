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

const TONE: Record<Tone, { fg: string; bg: string; bd: string }> = {
  amber: { fg: colors.amber, bg: 'rgba(242,160,61,0.12)', bd: 'rgba(242,160,61,0.28)' },
  teal: { fg: colors.teal, bg: 'rgba(79,182,160,0.12)', bd: 'rgba(79,182,160,0.28)' },
  crimson: { fg: colors.crimson, bg: 'rgba(229,86,75,0.12)', bd: 'rgba(229,86,75,0.28)' },
  muted: { fg: colors.muted, bg: 'rgba(140,129,116,0.12)', bd: 'rgba(140,129,116,0.28)' },
};

/** Small status/label pill. Mono uppercase text on a tinted track. */
export function Pill({ label, tone = 'amber', style }: PillProps) {
  const t = TONE[tone];
  return (
    <View
      style={[styles.base, { backgroundColor: t.bg, borderColor: t.bd }, style]}
    >
      <Text style={[styles.label, { color: t.fg }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    alignSelf: 'flex-start',
    borderRadius: radius.pill,
    borderWidth: StyleSheet.hairlineWidth,
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
