import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Body, Button, Display, KickerLabel, Pill } from '@/components';
import { formatClock } from '@/lib/time';
import { useCountdown } from '@/lib/useCountdown';
import { colors, fontFamily, gradients, spacing } from '@/theme';

const BREAK_SEC = 5 * 60;

const RESTORATIVE = ['Stretch', 'Walk', 'Water'];

export default function BreakScreen() {
  const remaining = useCountdown(BREAK_SEC);

  return (
    <View style={styles.root}>
      <LinearGradient colors={gradients.breakCalm} style={StyleSheet.absoluteFill} />
      <View style={styles.inner}>
        <View style={styles.top}>
          <KickerLabel color={colors.teal}>Break</KickerLabel>
          <Display style={styles.headline}>Block done — nice. Take a real break.</Display>
          <Text style={styles.clock}>{formatClock(remaining)}</Text>

          <Pill label="Your apps stay sealed" tone="teal" style={styles.sealedPill} />
          <Body style={styles.warn}>
            Don't scroll — it drains the energy you just built.
          </Body>

          <View style={styles.chips}>
            {RESTORATIVE.map((c) => (
              <Pill key={c} label={c} tone="teal" />
            ))}
          </View>
        </View>

        <View style={styles.footer}>
          <Button
            label="Start next block"
            onPress={() => router.replace('/sealApps')}
            accessibilityHint="Re-seal and run another focus block"
          />
          <Button
            label="End for now"
            variant="secondary"
            onPress={() => router.replace('/logWin')}
            accessibilityHint="Finish and log this session"
          />
        </View>
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
    justifyContent: 'space-between',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing['3xl'],
    paddingBottom: spacing['2xl'],
  },
  top: {
    alignItems: 'center',
  },
  headline: {
    marginTop: spacing.base,
    textAlign: 'center',
  },
  clock: {
    fontFamily: fontFamily.monoBold,
    fontSize: 60,
    color: colors.teal,
    marginTop: spacing.xl,
    letterSpacing: 1,
  },
  sealedPill: {
    marginTop: spacing.xl,
  },
  warn: {
    marginTop: spacing.base,
    fontSize: 15,
    lineHeight: 22,
    textAlign: 'center',
  },
  chips: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing['2xl'],
  },
  footer: {
    gap: spacing.sm,
  },
});
