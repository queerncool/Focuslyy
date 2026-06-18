import { router } from 'expo-router';
import { StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
  Title,
} from '@/components';
import { AVG_HOURS, PROGRESS } from '@/lib/onboarding';
import { useQuizStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

const AVG_BAR = 88;

export default function Results() {
  const hoursNum = useQuizStore((s) => s.hoursNum) ?? 0;
  const yrNum = useQuizStore((s) => s.yrNum) ?? 0;
  const barH = useQuizStore((s) => s.barH) ?? 0;

  const aboveAvg = hoursNum >= AVG_HOURS;
  const youBar = Math.min(170, Math.max(14, barH * 96));

  return (
    <OnboardingScreen
      progress={PROGRESS.results}
      footer={
        <Button
          label="See what it's costing me"
          onPress={() => router.push('/symptoms')}
        />
      }
    >
      <KickerLabel>Your answer</KickerLabel>
      <Display style={styles.headline}>
        You're handing your phone {hoursNum} hrs every day.
      </Display>
      <Body style={styles.sub}>
        {aboveAvg
          ? `That's above the ${AVG_HOURS}-hour daily average.`
          : `Below the ${AVG_HOURS}-hour daily average — but still hours worth reclaiming.`}
      </Body>

      <View style={styles.chart}>
        <Bar label="AVG" value={`${AVG_HOURS} hrs`} height={AVG_BAR} muted />
        <Bar label="YOU" value={`${hoursNum} hrs`} height={youBar} />
      </View>

      <Title style={styles.cost}>
        That's ~{yrNum.toLocaleString()} hours a year. A master's degree. A
        fluent language. A business. Gone — every year you wait.
      </Title>
    </OnboardingScreen>
  );
}

function Bar({
  label,
  value,
  height,
  muted = false,
}: {
  label: string;
  value: string;
  height: number;
  muted?: boolean;
}) {
  return (
    <View style={styles.barCol}>
      <Text style={[styles.value, { color: muted ? colors.muted : colors.cream }]}>
        {value}
      </Text>
      <View
        style={[styles.bar, { height }, muted ? styles.barMuted : styles.barYou]}
      />
      <KickerLabel
        color={muted ? colors.muted : colors.amber}
        style={styles.barLabel}
      >
        {label}
      </KickerLabel>
    </View>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  sub: {
    marginTop: spacing.md,
  },
  chart: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'flex-end',
    gap: spacing['3xl'],
    marginVertical: spacing.xl,
  },
  barCol: {
    alignItems: 'center',
  },
  value: {
    fontFamily: fontFamily.monoBold,
    fontSize: 14,
    marginBottom: spacing.sm,
  },
  bar: {
    width: 64,
    borderTopLeftRadius: radius.md,
    borderTopRightRadius: radius.md,
  },
  barYou: {
    backgroundColor: colors.amber,
  },
  barMuted: {
    backgroundColor: colors.ink,
  },
  barLabel: {
    marginTop: spacing.md,
  },
  cost: {
    marginTop: spacing.sm,
    fontSize: 21,
    lineHeight: 28,
  },
});
