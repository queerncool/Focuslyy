import { Redirect } from 'expo-router';

/**
 * Entry point. Phase 1 lands on the main tabs so the four-tab shell is the
 * first thing rendered. Onboarding gating (anon-default funnel) arrives in
 * Phases 2 & 5.
 */
export default function Index() {
  return <Redirect href="/(app)" />;
}
