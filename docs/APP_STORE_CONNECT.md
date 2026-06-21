# App Store Connect setup — click-by-click

How to create the app record and the three subscriptions. Do the parts in order.

## Part 0 — One-time prerequisites

**0a. Agree to the Paid Apps agreement + add banking/tax.**
Apple won't let you create paid subscriptions until this is done.
1. Go to <https://appstoreconnect.apple.com> → **Business** (or **Agreements,
   Tax, and Banking**).
2. Find **Paid Apps** → accept the agreement.
3. Fill in **Bank account** and **Tax** info. Status must read **Active**.

**0b. Register the Bundle ID** (if not already there).
1. Go to <https://developer.apple.com/account/resources/identifiers/list>.
2. Click the **➕** next to "Identifiers" → choose **App IDs** → **Continue** →
   **App** → **Continue**.
3. **Description:** `focuslyy`  ·  **Bundle ID:** select **Explicit**, enter
   `app.focuslyy.ios`.
4. Leave capabilities as-is for now (Family Controls gets added after the
   entitlement is granted). Click **Continue → Register**.

## Part A — Create the app record

1. <https://appstoreconnect.apple.com> → **Apps**.
2. Click the blue **➕** → **New App**.
3. Fill in:
   - **Platforms:** iOS
   - **Name:** `Focuslyy`  *(must be unique on the App Store; if it's taken,
     tell me and we'll pick a variant)*
   - **Primary Language:** English (U.S.)
   - **Bundle ID:** pick `app.focuslyy.ios` from the dropdown
   - **SKU:** `focuslyy001` *(just a private ID — anything unique works)*
   - **User Access:** Full Access
4. Click **Create**. The app record now exists (it'll show "Prepare for
   Submission" — that's expected).

## Part B — Create the subscriptions

Open your app → left sidebar → under **Monetization** → **Subscriptions**.

**B1. Create the subscription group** (groups plans that are alternatives to
each other).
1. Click **Create** (Subscription Group).
2. **Reference Name:** `Focuslyy Pro` *(internal only)*.
3. Save. Add a **localized display name** when asked: `Focuslyy Pro`.

**B2. Add the three plans.** Inside the group, click **➕ / Create** for each row
below and enter its values.

| Plan    | Reference Name   | Product ID                  | Duration | Price    |
|---------|------------------|-----------------------------|----------|----------|
| Weekly  | Focuslyy Weekly  | `app.focuslyy.ios.weekly`   | 1 Week   | $4.99    |
| Monthly | Focuslyy Monthly | `app.focuslyy.ios.monthly`  | 1 Month  | $9.99    |
| Yearly  | Focuslyy Yearly  | `app.focuslyy.ios.yearly`   | 1 Year   | $49.99   |

For each plan, after creating it you must also fill:
- **Subscription Duration:** as in the table.
- **Subscription Prices:** click **Add**, pick your country/price ($4.99 /
  $9.99 / $49.99 are the standard tiers closest to $5 / $10 / $50).
- **App Store Localization:** add a **Display Name** (e.g., "Weekly") and a
  short **Description** (e.g., "Unlimited focus sessions, billed weekly.").
- **Review Information:** a screenshot of the paywall (you'll add this once you
  have a build) + optional notes.

**B3. Add the intro offer on the Monthly plan** ("$5 first month").
1. Open the **Monthly** subscription → **Introductory Offers** → **Create
   Introductory Offer**.
2. **Type:** Pay As You Go  ·  **Duration:** 1 Month  ·  **Number of periods:**
   1  ·  **Price:** $4.99.
3. Save. (This makes the first month $4.99, then $9.99/month after.)

> ⚠️ Product IDs must match later. These exact IDs are what we'll map in
> RevenueCat and the code during Phase 7 (see `docs/PHASE7.md`). If you change
> one here, change it there too.

## What "Missing Metadata" means

Until you upload an app build and add screenshots, the subscriptions will show
**"Missing Metadata"** and the app will show **"Prepare for Submission."** That's
normal — they finish during the actual submission (after the Phase 7 native
build). Nothing is broken.
