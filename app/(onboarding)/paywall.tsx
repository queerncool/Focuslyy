import { useState } from 'react';
import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import {
  Body,
  Button,
  Display,
  KickerLabel,
  OnboardingScreen,
  Pill,
} from '@/components';
import { PROGRESS } from '@/lib/onboarding';
import { runPurchaseStub } from '@/lib/purchase';
import { useProfileStore, useQuizStore } from '@/state';
import { colors, fontFamily, radius, spacing } from '@/theme';
import type { SubscriptionTier } from '@/types';

const TILES: {
  tier: Exclude<SubscriptionTier, null>;
  price: string;
  period: string;
  best?: boolean;
}[] = [
  { tier: 'yearly', price: '$80', period: 'per year', best: true },
  { tier: 'monthly', price: '$10', period: 'per month' },
  { tier: 'weekly', price: '$5', period: 'per week' },
];

export default function Paywall() {
  const yrNum = useQuizStore((s) => s.yrNum) ?? 0;
  const projection = useQuizStore((s) => s.projection) ?? 'your time, back in your hands';
  const name = useProfileStore((s) => s.name).trim();
  const setSubscription = useProfileStore((s) => s.setSubscription);

  const [tier, setTier] = useState<Exclude<SubscriptionTier, null>>('yearly');

  const subscribe = () =>
    runPurchaseStub(tier, {
      onSuccess: () => {
        setSubscription(tier);
        router.push({ pathname: '/saveAccount', params: { next: 'firstSeal' } });
      },
    });

  return (
    <OnboardingScreen
      progress={PROGRESS.paywall}
      footer={
        <>
          <Button
            label={name ? `Take my hours back, ${name} →` : 'Take my hours back'}
            onPress={subscribe}
          />
          <Button
            label="Maybe later"
            variant="tertiary"
            onPress={() => router.push('/discount')}
          />
        </>
      }
    >
      <KickerLabel>The math</KickerLabel>
      <Display style={styles.headline}>The expensive option isn't focuslyy.</Display>

      <View style={styles.compare}>
        <View style={[styles.compareCard, styles.losing]}>
          <KickerLabel color={colors.crimson}>You're losing</KickerLabel>
          <Text style={[styles.bigNum, { color: colors.crimson }]}>
            ~{yrNum.toLocaleString()}
          </Text>
          <Body color={colors.cream} style={styles.compareSub}>
            hours every year — {projection}, gone.
          </Body>
        </View>
        <View style={[styles.compareCard, styles.costs]}>
          <KickerLabel color={colors.teal}>focuslyy costs</KickerLabel>
          <Text style={[styles.bigNum, { color: colors.teal }]}>22¢</Text>
          <Body color={colors.cream} style={styles.compareSub}>
            a day on the yearly plan — less than one coffee a week.
          </Body>
        </View>
      </View>

      <Body style={styles.bridge}>Which one is actually expensive?</Body>

      <View style={styles.tiles}>
        {TILES.map((t) => {
          const selected = tier === t.tier;
          return (
            <Pressable
              key={t.tier}
              onPress={() => setTier(t.tier)}
              accessibilityRole="button"
              accessibilityState={{ selected }}
              style={[styles.tile, selected && styles.tileSelected]}
            >
              <View style={styles.tileLeft}>
                <Text style={styles.tilePrice}>{t.price}</Text>
                <Text style={styles.tilePeriod}>{t.period}</Text>
              </View>
              {t.best && <Pill label="Best value" tone="amber" />}
            </Pressable>
          );
        })}
      </View>
    </OnboardingScreen>
  );
}

const styles = StyleSheet.create({
  headline: {
    marginTop: spacing.sm,
  },
  compare: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: spacing.xl,
  },
  compareCard: {
    flex: 1,
    padding: spacing.base,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    gap: spacing.xs,
  },
  losing: {
    borderColor: colors.crimson,
    backgroundColor: 'rgba(229,86,75,0.10)',
  },
  costs: {
    borderColor: colors.teal,
    backgroundColor: 'rgba(79,182,160,0.10)',
  },
  bigNum: {
    fontFamily: fontFamily.monoBold,
    fontSize: 30,
    marginTop: spacing.xs,
  },
  compareSub: {
    fontSize: 13,
    lineHeight: 18,
  },
  bridge: {
    marginTop: spacing.lg,
    fontSize: 16,
    fontStyle: 'italic',
    textAlign: 'center',
  },
  tiles: {
    marginTop: spacing.xl,
    gap: spacing.md,
  },
  tile: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 64,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: 1.5,
    borderColor: colors.ink,
    backgroundColor: colors.ink,
  },
  tileSelected: {
    borderColor: colors.amber,
    backgroundColor: 'rgba(242,160,61,0.10)',
  },
  tileLeft: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: spacing.sm,
  },
  tilePrice: {
    fontFamily: fontFamily.monoBold,
    fontSize: 22,
    color: colors.cream,
  },
  tilePeriod: {
    fontFamily: fontFamily.mono,
    fontSize: 13,
    color: colors.muted,
  },
});
