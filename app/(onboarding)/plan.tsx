import { router } from 'expo-router';
import {
  Pressable,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import {
  Body,
  Display,
  KickerLabel,
  OnboardingScreen,
  Pill,
  SegmentedOption,
} from '@/components';
import { planMonthlyHours, PROGRESS, topBlocklist } from '@/lib/onboarding';
import { useProfileStore, useQuizStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';

const GOAL_OPTIONS = [
  { value: 1, label: '1H' },
  { value: 2, label: '2H' },
  { value: 3, label: '3H' },
  { value: 4, label: '4H' },
];
const DAYS_OPTIONS = [
  { value: 3, label: '3' },
  { value: 5, label: '5' },
  { value: 7, label: '7' },
];

export default function Plan() {
  const name = useProfileStore((s) => s.name);
  const dailyGoal = useProfileStore((s) => s.dailyGoal);
  const commitDays = useProfileStore((s) => s.commitDays);
  const setName = useProfileStore((s) => s.setName);
  const setPlan = useProfileStore((s) => s.setPlan);

  const mode = useQuizStore((s) => s.mode);
  const projection = useQuizStore((s) => s.projection);
  const distractions = useQuizStore((s) => s.distractions);

  const hours = planMonthlyHours(dailyGoal, commitDays);
  const blocklist = topBlocklist(distractions);
  const trimmed = name.trim();
  const outcome = projection ?? 'your time, back in your hands';
  const projectionLine = trimmed
    ? `${trimmed}, ${outcome}.`
    : `${outcome.charAt(0).toUpperCase()}${outcome.slice(1)}.`;

  return (
    <OnboardingScreen progress={PROGRESS.plan}>
      <KickerLabel>The plan</KickerLabel>
      <Display style={styles.headline}>Build the plan you'll actually do.</Display>

      {mode != null && (
        <View style={styles.metaRow}>
          <Pill label={`${mode} mode`} tone="amber" />
          {blocklist.length > 0 && (
            <Body style={styles.blocklist}>Blocking {blocklist.join(', ')}</Body>
          )}
        </View>
      )}

      <View style={styles.field}>
        <KickerLabel>What should we call you?</KickerLabel>
        <TextInput
          value={name}
          onChangeText={setName}
          placeholder="Your name"
          placeholderTextColor={colors.muted}
          style={styles.input}
          returnKeyType="done"
          maxLength={24}
        />
      </View>

      <View style={styles.field}>
        <KickerLabel>Daily goal</KickerLabel>
        <SegmentedOption
          options={GOAL_OPTIONS}
          value={dailyGoal}
          onChange={(v) => setPlan(v, commitDays)}
        />
      </View>

      <View style={styles.field}>
        <KickerLabel>Days per week</KickerLabel>
        <SegmentedOption
          options={DAYS_OPTIONS}
          value={commitDays}
          onChange={(v) => setPlan(dailyGoal, v)}
        />
      </View>

      {/* The projection card IS the CTA — no separate button (§B.1). */}
      <Pressable
        accessibilityRole="button"
        accessibilityHint="Continue to your plan"
        onPress={() => router.push('/paywall')}
        style={styles.projection}
      >
        <View style={styles.projectionBody}>
          <KickerLabel color={colors.amber}>Your next 30 days</KickerLabel>
          <Text style={styles.projectionHours}>≈{hours} hours</Text>
          <Body color={colors.cream} style={styles.projectionText}>
            of deep work — {projectionLine}
          </Body>
        </View>
        <Text style={styles.arrow}>→</Text>
      </Pressable>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  metaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginTop: spacing.base,
  },
  blocklist: {
    fontSize: 13,
  },
  field: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
  input: {
    minHeight: 56,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
    paddingHorizontal: spacing.lg,
    fontFamily: fontFamily.display,
    fontSize: 18,
    color: colors.cream,
  },
  projection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.base,
    marginTop: spacing['2xl'],
    padding: spacing.lg,
    borderRadius: radius.xl,
    borderWidth: 1.5,
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.12)',
  },
  projectionBody: {
    flex: 1,
    gap: spacing.xs,
  },
  projectionHours: {
    fontFamily: fontFamily.monoBold,
    fontSize: 34,
    color: colors.amberLight,
    marginTop: spacing.xs,
  },
  projectionText: {
    fontSize: 16,
  },
  arrow: {
    fontFamily: fontFamily.displayHeavy,
    fontSize: 30,
    color: colors.amber,
  },
});
