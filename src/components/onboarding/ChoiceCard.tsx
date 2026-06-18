import { Pressable, StyleSheet, Text, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';
import { colors, fontFamily, radius, spacing } from '@/theme';

interface ChoiceCardProps {
  label: string;
  selected: boolean;
  onPress: () => void;
  /** 'single' shows a radio dot, 'multi' shows a checkbox. */
  mode?: 'single' | 'multi';
}

/** Selectable option row for the quiz (Q1–Q3). */
export function ChoiceCard({
  label,
  selected,
  onPress,
  mode = 'single',
}: ChoiceCardProps) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole={mode === 'multi' ? 'checkbox' : 'radio'}
      accessibilityState={{ checked: selected, selected }}
      style={[styles.card, selected && styles.cardSelected]}
    >
      <Text style={[styles.label, selected && styles.labelSelected]}>{label}</Text>
      <View style={[styles.marker, selected && styles.markerSelected]}>
        {selected && (
          <Svg width={14} height={14} viewBox="0 0 24 24" fill="none">
            <Path
              d="M5 12.5l4.5 4.5L19 7.5"
              stroke={colors.espresso}
              strokeWidth={3}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </Svg>
        )}
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 60,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.base,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  cardSelected: {
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.10)',
  },
  label: {
    flex: 1,
    fontFamily: fontFamily.display,
    fontSize: 17,
    color: colors.cream,
  },
  labelSelected: {
    color: colors.amberLight,
  },
  marker: {
    width: 24,
    height: 24,
    borderRadius: radius.pill,
    borderWidth: 1.5,
    borderColor: colors.muted,
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: spacing.md,
  },
  markerSelected: {
    backgroundColor: colors.amber,
    borderColor: colors.amber,
  },
});
