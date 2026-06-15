import { StyleSheet, Text } from 'react-native';
import { Screen } from './Screen';
import { KickerLabel } from './KickerLabel';
import { colors, fontFamily, spacing } from '@/theme';

interface PlaceholderScreenProps {
  title: string;
  kicker?: string;
}

/**
 * Phase-1 stub: centered tab name on the brand background, rendered in the
 * locked display font so we can verify fonts loaded. Replaced screen-by-screen
 * in Phases 2-4.
 */
export function PlaceholderScreen({ title, kicker = 'focuslyy' }: PlaceholderScreenProps) {
  return (
    <Screen center>
      <KickerLabel>{kicker}</KickerLabel>
      <Text style={styles.title}>{title}</Text>
    </Screen>
  );
}

const styles = StyleSheet.create({
  title: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 34,
    color: colors.cream,
    marginTop: spacing.sm,
  },
});
