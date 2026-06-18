import { useState } from 'react';
import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { Body, Button, KickerLabel, Screen } from '@/components';
import { formatClock } from '@/lib/time';
import { useCountdown } from '@/lib/useCountdown';
import { haptic } from '@/lib/haptics';
import { colors, fontFamily, radius, spacing } from '@/theme';

const RITUAL_SEC = 30;

const CUES = [
  'Clear your desk',
  'Water within reach',
  'Silence everything',
  'Three deep breaths',
];

export default function Ritual() {
  const [ready, setReady] = useState(false);
  const [checked, setChecked] = useState<string[]>([]);

  const remaining = useCountdown(RITUAL_SEC, () => setReady(true));

  const toggleCue = (cue: string) => {
    haptic.light();
    setChecked((prev) =>
      prev.includes(cue) ? prev.filter((c) => c !== cue) : [...prev, cue]
    );
  };

  const startNow = () => {
    haptic.medium();
    router.replace('/locked');
  };

  return (
    <Screen style={styles.screen}>
      <View style={styles.top}>
        <KickerLabel color={colors.amber}>The ritual</KickerLabel>
        <Text style={styles.clock}>{formatClock(remaining)}</Text>
        <Body style={styles.intro}>
          Don't skip this — it's how your brain learns the seal means focus.
        </Body>
      </View>

      <View style={styles.cues}>
        {CUES.map((cue) => {
          const on = checked.includes(cue);
          return (
            <Pressable
              key={cue}
              accessibilityRole="checkbox"
              accessibilityState={{ checked: on }}
              onPress={() => toggleCue(cue)}
              style={[styles.cue, on && styles.cueOn]}
            >
              <View style={[styles.box, on && styles.boxOn]}>
                {on && <Text style={styles.boxMark}>✓</Text>}
              </View>
              <Text style={[styles.cueText, on && styles.cueTextOn]}>{cue}</Text>
            </Pressable>
          );
        })}
      </View>

      <View style={styles.footer}>
        <Button
          label={ready ? "I'm ready — start now" : `Get ready… ${formatClock(remaining)}`}
          disabled={!ready}
          onPress={startNow}
          accessibilityHint="Start the locked focus block"
        />
        <Button label="Skip the ritual" variant="tertiary" onPress={startNow} />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  top: {
    paddingTop: spacing['2xl'],
    alignItems: 'center',
  },
  clock: {
    fontFamily: fontFamily.monoBold,
    fontSize: 64,
    color: colors.cream,
    marginTop: spacing.base,
    letterSpacing: 1,
  },
  intro: {
    marginTop: spacing.base,
    fontSize: 15,
    lineHeight: 22,
    textAlign: 'center',
  },
  cues: {
    flex: 1,
    justifyContent: 'center',
    gap: spacing.md,
  },
  cue: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.base,
    minHeight: 56,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  cueOn: {
    borderColor: colors.teal,
    backgroundColor: 'rgba(79,182,160,0.12)',
  },
  box: {
    width: 26,
    height: 26,
    borderRadius: radius.sm,
    borderWidth: 1.5,
    borderColor: colors.muted,
    alignItems: 'center',
    justifyContent: 'center',
  },
  boxOn: {
    borderColor: colors.teal,
    backgroundColor: colors.teal,
  },
  boxMark: {
    fontFamily: fontFamily.monoBold,
    fontSize: 15,
    color: colors.espresso,
  },
  cueText: {
    fontFamily: fontFamily.display,
    fontSize: 17,
    color: colors.muted,
  },
  cueTextOn: {
    color: colors.cream,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
    gap: spacing.sm,
  },
});
