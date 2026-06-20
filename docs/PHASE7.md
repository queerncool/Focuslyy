# Phase 7 — Native activation runbook (Family Controls + RevenueCat)

This is the step-by-step for turning on the real, native features. **None of
this runs in Expo Go or the browser** — it requires a custom dev client built on
a Mac with Xcode. Everything the app needs in JavaScript is already wired to
*seams* (`src/lib/blocking.ts`, `src/lib/purchases.ts`); activation is mostly
installing native packages, editing `app.json`, and swapping each seam's stub
body for the real implementation below.

> Why seams? The native modules crash the Metro bundler if imported in the
> managed app, so the codebase keeps them out until the dev client exists. The
> screens (Locked, Log Win, Seal Apps, Paywall, Profile, saveAccount) already
> call the seam functions — flipping each `…Available` flag and filling in the
> body is all that's left.

---

## 0. Prerequisites (start these EARLY — Apple is the long pole)

- [ ] **Apple Developer Program** membership (paid).
- [ ] **Family Controls (Distribution) entitlement** — request via Apple's
      form: <https://developer.apple.com/contact/request/family-controls-distribution>.
      Approval can take **days to weeks**. The app cannot ship real blocking
      until this is granted. Do this first.
- [ ] A **Mac with Xcode** installed.
- [ ] An **App Store Connect** app record for `app.focuslyy.ios`.
- [ ] A **RevenueCat** account + project.

## 1. Eject to a dev client

```bash
npx expo install expo-dev-client
npx expo prebuild --clean        # generates the native ios/ project
npx expo run:ios                 # builds + runs the dev client on a simulator/device
```

From here on you launch with `npx expo run:ios` (or a TestFlight build), **not**
Expo Go. Keep the managed-friendly seams so `npx expo start --web` still works
for quick UI checks.

---

## 2. App blocking (the core differentiator)

### 2a. Install + configure

```bash
npx expo install react-native-device-activity
```

Add the config plugin and the entitlement to `app.json` → `expo`:

```jsonc
"ios": {
  "supportsTablet": false,
  "bundleIdentifier": "app.focuslyy.ios",
  "entitlements": {
    "com.apple.developer.family-controls": true   // Distribution variant once approved
  }
},
"plugins": [
  "expo-router",
  "expo-font",
  ["expo-splash-screen", { "backgroundColor": "#18120E", "image": "./assets/images/splash-icon.png", "imageWidth": 120 }],
  ["react-native-device-activity", { /* see the package README for current options */ }]
]
```

Re-run `npx expo prebuild --clean` after editing `app.json`.

> ⚠️ Confirm the exact plugin options and JS API names against the installed
> version's README — the kingstinct package evolves. The structure below is the
> contract our screens expect; map it onto the real calls.

### 2b. Swap in `src/lib/blocking.ts`

Replace the stub body so it requests authorization, shields the selected app
tokens via a `ManagedSettingsStore`, and exposes the system picker:

```ts
import * as DeviceActivity from 'react-native-device-activity';

export const blockingAvailable = true;

export async function applyShield(apps: string[]): Promise<void> {
  await DeviceActivity.requestAuthorization('individual');
  // `apps` are the opaque FamilyActivitySelection tokens saved from the picker.
  DeviceActivity.blockSelection({ selection: apps });   // confirm API name
}

export async function liftShield(): Promise<void> {
  DeviceActivity.unblockSelection();                     // confirm API name
}

export async function pickBlockedApps(): Promise<string[] | null> {
  const selection = await DeviceActivity.presentFamilyActivityPicker(); // confirm
  return selection ?? null;
}
```

### 2c. Wire the Seal Apps screen to the picker

In `app/(session)/sealApps.tsx`, when `blockingAvailable` is true, replace the
named-app toggle list with a single button that calls `pickBlockedApps()`,
stores the returned tokens in `useSessionStore.blockedApps`, and persists them
to `useProfileStore.defaultBlocklist`. **The visual stays the same** — only the
interaction changes. The Locked/Log Win shield calls already work unchanged
(`applyShield` on Locked mount, `liftShield` on Log Win mount).

### 2d. Test

Build to a **real device** (simulators can't enforce Family Controls), select
real apps, start a session, and confirm the OS shield blocks them — and that it
lifts when you log the win or break the seal.

---

## 3. Subscriptions (RevenueCat)

### 3a. Configure products

In **App Store Connect** create the auto-renewing subscriptions, and mirror them
in the **RevenueCat dashboard**:

| Product        | Price | Notes                          |
| -------------- | ----- | ------------------------------ |
| Weekly         | $5    |                                |
| Monthly        | $10   | + a **$5 intro** first month   |
| Yearly         | $80   | "Best value" tile              |

Create a RevenueCat **offering** whose packages map to these, and note the
public **API key**.

### 3b. Install + initialize

```bash
npx expo install react-native-purchases
```

Initialize once at app start (e.g. in `app/_layout.tsx`, dev-client only):

```ts
import Purchases from 'react-native-purchases';
Purchases.configure({ apiKey: '<revenuecat_public_key>', appUserID: profileId });
```

### 3c. Swap in `src/lib/purchases.ts`

```ts
import Purchases from 'react-native-purchases';
import type { SubscriptionTier } from '@/types';

export const purchasesAvailable = true;

export async function purchasePlan(tier, opts) {
  const offerings = await Purchases.getOfferings();
  const pkg = offerings.current?.availablePackages.find((p) => p.identifier === tier);
  if (!pkg) return;
  try {
    await Purchases.purchasePackage(pkg);
    opts.onSuccess();           // record subscription + open saveAccount, as today
  } catch (e) {
    if (!e.userCancelled) throw e;
  }
}

export async function restorePurchases() {
  const info = await Purchases.restorePurchases();
  return info.activeSubscriptions.length > 0 ? 'restored' : 'none';
}

export async function linkPurchaseAccount(accountId: string) {
  await Purchases.logIn(accountId);   // preserves the subscription across anon→account
}
```

The Paywall, Discount, Profile "Restore purchases", and saveAccount screens
already call these — no screen changes needed beyond the init call.

---

## 4. Real sign-in (Apple + Google)

```bash
npx expo install expo-apple-authentication @react-native-google-signin/google-signin
```

In `app/saveAccount.tsx`, replace the simulated `linkWith` body: run the real
provider flow, then call the existing `linkAccount(provider)` and
`linkPurchaseAccount(id)`. Apple Sign-In needs the **"Sign in with Apple"**
capability enabled on the App ID; Google needs an OAuth client + URL scheme.
Remove the "Sign-in is simulated…" caption once live.

---

## 5. Ship checklist

- [ ] Family Controls entitlement granted and in `app.json`.
- [ ] Blocking enforced on a real device (shield up on Locked, down on Log Win).
- [ ] Seal Apps uses the system picker; selection persists as default blocklist.
- [ ] Products live in App Store Connect + RevenueCat; purchase + restore work.
- [ ] Anonymous→account linking verified (`Purchases.logIn`).
- [ ] Apple/Google sign-in working; simulated caption removed.
- [ ] `npx expo start --web` still loads (seams degrade gracefully).

When all boxes are checked, move to **Phase 8** (App Store assets + submission).
```
