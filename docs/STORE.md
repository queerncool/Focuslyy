# App Store submission package (Phase 8)

Everything needed to fill out App Store Connect. Copy-paste the text blocks
directly. Items marked **[you, on device]** need a real iPhone or the App Store
Connect website — they can't be generated from the codebase.

---

## 1. Listing copy (paste into App Store Connect)

**App Name** (max 30 chars)
```
Focuslyy
```

**Subtitle** (max 30 chars)
```
Seal the apps. Do deep work.
```

**Promotional text** (max 170 chars — editable anytime without review)
```
Seal your distracting apps for a set block of time, do the work that matters,
and watch your focused hours turn into streaks. Take your hours back.
```

**Keywords** (max 100 chars, comma-separated, NO spaces after commas)
```
focus,deep work,app blocker,adhd,study,productivity,screen time,distraction,focus timer,blocker
```

**Description** (max 4000 chars)
```
You don't have a motivation problem. You have a "one quick check" problem.

The average phone pulls you out of focus every few minutes. Over a year, that's
hundreds of hours — gone to feeds you won't remember. focuslyy gives them back.

HOW IT WORKS
1. Pick the one thing that matters right now.
2. Seal the apps that pull you out — TikTok, Instagram, YouTube, whatever gets
   you. They're locked for the length of your session.
3. A 30-second wind-down ritual gets your head in the game.
4. The timer runs. Your apps stay sealed. You do the work.
5. Log the win and watch your focused hours add up.

WHY IT WORKS
- The seal is real friction. Breaking it early takes a deliberate press-and-hold
  — no accidental escapes, no "just this once."
- Your focused time becomes visible: streaks, weekly hours, and a clean chart of
  your deep work. Progress you can actually see.
- Built ADHD-friendly from the first screen — calm, clear, one decision at a
  time. No clutter, no guilt.

BUILT FOR THE WORK THAT MATTERS
Whether you're shipping a feature, studying for finals, training, writing,
reading, or just reclaiming an afternoon — focuslyy is for self-directed deep
work you choose, on your terms.

Seal the apps. Do deep work. Take your hours back.

—
Subscription unlocks unlimited sessions. Weekly, monthly, and yearly plans
available. Cancel anytime.
```

> Note: no invented stats or fake testimonials (CLAUDE.md rule). The "hundreds
> of hours" line is framed generally, not as a specific percentile. Add real
> founding-member quotes here only once you actually have them.

---

## 2. Screenshots **[you, on device]**

Required sizes: **6.7"** (iPhone 15 Pro Max) and **6.1"** (iPhone 15 Pro).
Capture 5 frames from the real running app, in this order:

| # | Screen | Caption overlay to add |
|---|--------|------------------------|
| 1 | Locked screen, timer running | "Seal the apps. Do the work." |
| 2 | Seal Apps — choosing apps | "Lock what pulls you out." |
| 3 | Stats — the weekly chart | "Watch your hours add up." |
| 4 | Profile — streak + banked hours | "Build a streak you won't break." |
| 5 | Share card | "Make it count. Share your day." |

How to capture: run the app on the device, press the side + volume-up buttons,
then drop the screenshots into App Store Connect (or design framed versions in
Figma/Canva using the brand palette in `src/theme/colors.ts`).

## 3. Preview video (optional but recommended) **[you, on device]**

15–30s, no audio needed. Screen-record one full session: Set Session → Seal →
Locked → Break → Log Win → Share. Human-paced, not rushed.

---

## 4. App Privacy disclosures (App Store Connect → App Privacy)

Declare honestly — App Review checks this against the binary. Based on the
launch build:

| Data type | Collected? | Linked to user? | Purpose |
|-----------|-----------|-----------------|---------|
| Name | Only if user signs in (Apple/Google) | Yes | App functionality (account) |
| Email | Only if user signs in | Yes | App functionality (account) |
| Purchases | Yes (via RevenueCat) | Yes | App functionality (manage subscription) |
| User ID | Yes (anonymous app user id) | Yes | App functionality |
| App activity (sessions, streaks) | Stored **on device** | — | Not collected by us at launch (local-only) |
| Blocked-app selections | Stored **on device only** | — | Never transmitted |

If you have NOT added any analytics SDK, do not declare analytics. If you add
one later, update this. The Family Activity selections never leave the device —
do not declare them.

---

## 5. Family Controls justification (App Review will ask)

```
focuslyy uses the Family Controls and DeviceActivity frameworks to let users
voluntarily restrict their own access to apps they select, only for the duration
of focus sessions they themselves start. The user picks the apps via the system
FamilyActivityPicker; we apply a ManagedSettings shield over only that selection
and lift it automatically when the session ends or the user chooses to break it.
Selections stay on device and are never collected. This directly supports the
app's core use case: self-directed deep work.
```

## 6. App Review notes (paste into the "Notes" field)

```
No login is required to use the app — you can complete onboarding and run focus
sessions anonymously, so no demo account is needed. Sign in with Apple is
optional and only used to save progress. The app uses Family Controls solely for
user-initiated, self-directed app blocking during focus sessions (see usage
justification). Subscriptions are standard auto-renewing StoreKit products;
please test in sandbox.
```

---

## 7. Required URLs (host before submitting)

- **Privacy Policy:** `https://focuslyy.app/privacy` — content drafted in
  `docs/legal/privacy.md`
- **Terms of Use:** `https://focuslyy.app/terms` — content drafted in
  `docs/legal/terms.md`
- **Support URL:** a reachable page or `mailto:` (App Store requires one).

---

## 8. Submission checklist

- [ ] Icon 1024×1024 uploaded (see `assets/icons/`).
- [ ] Screenshots uploaded at 6.7" and 6.1".
- [ ] Name, subtitle, promo text, description, keywords entered.
- [ ] Category: Productivity (primary). Secondary: optional.
- [ ] Age rating completed (likely 4+; the app is not directed at children).
- [ ] Subscriptions created + submitted with the build.
- [ ] App Privacy section completed (table above).
- [ ] Privacy Policy + Terms URLs live.
- [ ] Review notes + Family Controls justification pasted.
- [ ] Build uploaded from Xcode/EAS, attached to the version.
- [ ] Submit. Expect 24–72h; be ready for one revision request.
```
