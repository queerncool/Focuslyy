import type { ReactNode } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Screen } from '@/components/Screen';
import { ProgressBar } from '@/components/ProgressBar';
import { spacing } from '@/theme';

interface OnboardingScreenProps {
  /** 0–100 funnel progress for the top bar. */
  progress: number;
  children: ReactNode;
  /** Pinned footer (CTAs). Stays at the bottom, outside the scroll area. */
  footer?: ReactNode;
  /** Background tone — Symptoms/Paywall shift away from plain espresso. */
  tone?: 'dark' | 'light';
  /** Optional gradient backdrop (≥2 colors), e.g. the crimson-warm Symptoms bg. */
  gradient?: readonly [string, string, ...string[]];
  /** Disable scroll for screens that should fill exactly one viewport. */
  scroll?: boolean;
}

/**
 * Shared funnel scaffold: progress bar up top, scrollable content, optional
 * pinned footer. Keeps every onboarding screen visually consistent.
 */
export function OnboardingScreen({
  progress,
  children,
  footer,
  tone = 'dark',
  gradient,
  scroll = true,
}: OnboardingScreenProps) {
  return (
    <Screen tone={tone} style={styles.screen}>
      {gradient != null && (
        <LinearGradient colors={gradient} style={StyleSheet.absoluteFill} />
      )}
      <View style={styles.progressWrap}>
        <ProgressBar progress={progress} />
      </View>
      {scroll ? (
        <ScrollView
          style={styles.flex}
          contentContainerStyle={styles.content}
          showsVerticalScrollIndicator={false}
        >
          {children}
        </ScrollView>
      ) : (
        <View style={[styles.flex, styles.content]}>{children}</View>
      )}
      {footer != null && <View style={styles.footer}>{footer}</View>}
    </Screen>
  );
}

const styles = StyleSheet.create({
  screen: {
    paddingHorizontal: spacing.lg,
  },
  flex: {
    flex: 1,
  },
  progressWrap: {
    paddingTop: spacing.sm,
    paddingBottom: spacing.lg,
  },
  content: {
    flexGrow: 1,
    paddingBottom: spacing.lg,
  },
  footer: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
    gap: spacing.sm,
  },
});
