/**
 * App-blocking seam (Phase 7 · the core differentiator).
 *
 * Real blocking is impossible from JavaScript and the native module
 * (`react-native-device-activity` + Apple Family Controls) crashes Metro if it's
 * imported in the managed app — so in Expo Go / web this file is a labeled no-op
 * stub. Screens (Locked, Log Win, Seal Apps) call this interface either way; the
 * native implementation is dropped in for the dev client. See docs/PHASE7.md.
 */

/** Flips to true once the native Family Controls module is wired in. */
export const blockingAvailable = false;

/** Apply the shield over the user's selected apps at session start. */
export async function applyShield(apps: string[]): Promise<void> {
  if (__DEV__) {
    // eslint-disable-next-line no-console
    console.log(`[blocking stub] would seal ${apps.length} app(s):`, apps);
  }
}

/** Lift the shield when the session ends or the seal is broken. */
export async function liftShield(): Promise<void> {
  if (__DEV__) {
    // eslint-disable-next-line no-console
    console.log('[blocking stub] would lift the shield');
  }
}

/**
 * Launch Apple's FamilyActivityPicker and return opaque selection tokens.
 * The stub returns null, so Seal Apps falls back to its named-app toggle list.
 */
export async function pickBlockedApps(): Promise<string[] | null> {
  return null;
}
