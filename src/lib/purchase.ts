import { Alert } from 'react-native';
import type { SubscriptionTier } from '@/types';

const LABELS: Record<Exclude<SubscriptionTier, null>, string> = {
  weekly: 'Weekly · $5/wk',
  monthly: 'Monthly · $10/mo',
  yearly: 'Yearly · $80/yr',
};

/**
 * Phase 5 paywall stub (§B.5). Real StoreKit/RevenueCat purchasing is Phase 7;
 * here we surface a native alert so the funnel can be exercised end to end.
 */
export function runPurchaseStub(
  tier: Exclude<SubscriptionTier, null>,
  opts: { onSuccess: () => void; subtitle?: string }
) {
  Alert.alert(
    'Subscribe (dev stub)',
    `${opts.subtitle ?? LABELS[tier]}\n\nPayments are wired in Phase 7 — simulate the outcome:`,
    [
      { text: 'Simulate cancel', style: 'cancel' },
      { text: 'Simulate success', onPress: opts.onSuccess },
    ]
  );
}
