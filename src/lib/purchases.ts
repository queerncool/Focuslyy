/**
 * Subscription seam (Phase 7).
 *
 * Today this delegates to the dev-stub alert. Phase 7 swaps the body for
 * RevenueCat (`react-native-purchases`): purchasePackage, restorePurchases, and
 * logIn for anonymous→account subscription linking. Screens call this interface
 * either way, so activation is a single-file change. See docs/PHASE7.md.
 */
import { runPurchaseStub } from './purchase';
import type { SubscriptionTier } from '@/types';

/** Flips to true once RevenueCat is configured in the dev client. */
export const purchasesAvailable = false;

/** Start a purchase. Stub: the "Subscribe (dev stub)" alert. */
export function purchasePlan(
  tier: Exclude<SubscriptionTier, null>,
  opts: { onSuccess: () => void; subtitle?: string }
) {
  runPurchaseStub(tier, opts);
}

/** Restore prior purchases (Apple requires this button). Stub: nothing to restore. */
export async function restorePurchases(): Promise<'restored' | 'none'> {
  return 'none';
}

/** Link the RevenueCat anonymous user to a signed-in account id. */
export async function linkPurchaseAccount(accountId: string): Promise<void> {
  if (__DEV__) {
    // eslint-disable-next-line no-console
    console.log('[purchases stub] would link RevenueCat account', accountId);
  }
}
