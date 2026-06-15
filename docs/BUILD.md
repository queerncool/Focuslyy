# focuslyy — Build Plan & Spec

This is the master build doc. Two halves:

- **Phase prompts (§A)** — paste these into Claude Code in order, one per session.
- **Spec reference (§B–E)** — the screen-by-screen brief, state model, data bindings, and native work. Claude Code reads this on its own when you ask it to.

Pace: realistically a session per phase, 1–3 sessions across a day or two. Don't try to do two phases in one session; you'll hit a token reset window and lose context mid-build.

---

## §A — Phase prompts (paste these in order)

### Phase 1 — Scaffold, brand, navigation

Read `CLAUDE.md` and `docs/BUILD.md` in full before doing anything. Then:

Scaffold a new Expo + React Native + TypeScript project named `focuslyy` in the current directory, strict mode on. Use Expo Router (file-based). Install: `expo-font`, `@react-native-async-storage/async-storage`, `zustand`, `react-native-svg`, `expo-haptics`, `expo-linear-gradient`.

Set up the file structure exactly as defined in CLAUDE.md ("File structure" section).

Create `src/theme/colors.ts` with the locked palette as named exports. Create `src/theme/fonts.ts` that loads Fraunces Black Italic, Schibsted Grotesk (700, 800), and Space Mono via `expo-font` from `assets/fonts/`. Create `src/theme/spacing.ts` with a 4-based scale.

Build reusable components in `src/components/`: `Button` (primary amber filled, secondary ghost, tertiary text), `Card`, `Pill`, `KickerLabel` (mono uppercase), `RingTimer` (the amber arc countdown — see prototype's locked screen). All consume tokens from `src/theme/`, never inline hex.

Set up tab navigation under `app/(app)/` with four tabs: Focus (default), Friends, Stats, Profile. Stub each tab with a placeholder screen showing the tab name centered. Set up `app/(onboarding)/` as a separate stack with no tab bar. Set up `app/(session)/` as a modal stack.

Centralize state in `src/state/`. Create empty Zustand stores: `useQuizStore`, `useProfileStore`, `useSessionStore`, `useSessionsHistoryStore`. Wire `persist` middleware to AsyncStorage for all of them. Define the TypeScript types in `src/types/`.

Run on iOS simulator. **Exit criteria:** the app boots, the tab bar shows four tabs, the placeholder screens render with brand fonts loaded, and you can switch tabs cleanly.

### Phase 2 — Onboarding funnel (the conversion engine)

Read §B.1 (Onboarding) and §C (Data Bindings) in BUILD.md before starting. Open `docs/prototype.html` in a browser and click through the onboarding flow once (Start → Q1 → Q2 → Q3 → Results → Symptoms → Help → Reviews → Features → Plan → Paywall → Discount → FirstSeal) — that's your visual reference for every screen.

Build the onboarding stack in `app/(onboarding)/`. Each screen is one file. Use a shared progress bar component at the top (4% → 100% across the funnel; values in §B.1). Persist quiz answers to `useQuizStore` as the user advances.

The data bindings are **NON-NEGOTIABLE** — every value in §C must flow from user inputs, not from hardcoded text. Specifically: Q1 hours band drives the Results headline, annualized "hours per year," and bar height. Q2 distractions drive the Seal screen's pre-selected apps and the Plan screen's blocklist line. Q3 goal drives the Plan screen's MODE label, 30-day projection, and (later) the Session screen's mode pill. The Plan screen has live customization (name input, daily goal buttons, days-per-week buttons) that update a live projection card.

**Exit criteria:** I can complete the full funnel on the simulator, my answers actually change the Results and Plan screens, the projection updates live as I tap goal/days, and on completion the quiz state is persisted (kill the app, reopen, the state survives).

Do NOT build the paywall payment integration in this phase. The paywall screen is fully designed (cost-comparison band + three plan tiles), but the CTA just advances to FirstSeal (or to Discount on "maybe later") — RevenueCat wiring is Phase 7.

### Phase 3 — Core session loop (the heart of the product)

Read §B.2 (Core App) and skim §B.1 for context. Open the prototype, skip into the core app via the button, and click through Set Session → Seal Apps → Ritual → Locked → Break → Log Win → Share. That's your visual reference.

Build the session flow as a modal stack in `app/(session)/`. The screens in order:

1. **Set Session** — task input (real text input, real suggestion chips that change by mode from Q3), block-length picker (15/30/60/90 + custom field max 240), mode pill from Plan.
2. **Seal Apps** — the list of toggleable apps with pre-checks based on Q2. Live count badge. NOTE: in Phase 7 this becomes Apple's FamilyActivityPicker, but for Phases 3-6 use the named-app toggle list from the prototype.
3. **Ritual** — 30-second countdown, four prep cues, a button that's enabled only after the countdown ends (or skippable).
4. **Locked** — the big amber ring countdown using the `RingTimer` component, the task text echoed, the blocked-app count echoed, a long-press "hold to break the seal" early-exit (use react-native-gesture-handler).
5. **Break** — 5-minute countdown, teal-tinted background, "your apps stay sealed" message, restorative chips, two CTAs (start next block / end for now).
6. **Log Win** — TIME / XP / STREAK stat row (TIME computed from block length), task echo ("did you finish: '{task}'?"), real text input with goal-aware completion chips. Saves to `useSessionsHistoryStore` on advance.
7. **Share** — branded share-card preview, real `Share` intent on tap (use `expo-sharing`).

The task text, block length, and seal count MUST flow through every subsequent screen. If I type "Ship the onboarding flow" on Set Session, it appears on Locked, on Log Win, and on the share card.

**Exit criteria:** I can complete a full session from Home → Set Session → … → Share, the countdowns actually run, the task carries through, and the completed session appears in the sessions history store. Killing the app preserves history.

### Phase 4 — Tabs (Stats, Profile, Friends), Day-1 vs Established states, Invite

Read §B.3 (Tabs) and §B.4 (Day-1 states). Open the prototype, use the Day-1 / Established toggle in the top right to compare states on Home, Friends, and Stats.

Build the four tabs:

1. **Home (Focus)** — greeting with name, streak chip, goal ring (today's deep-work / 2h goal), CTA "Begin deep work." Day-1: streak shows 🔥1, invite-bootstrap card in place of friends row. Established: friends activity line + FOMO copy. Read `phase` from `useProfileStore`.
2. **Stats** — today / this week / this month totals, delta vs previous period ("+18% vs last week"), 7-day bar chart, recent sessions list (real entries from `useSessionsHistoryStore` — never fake), current streak + best streak + total banked hours. Day-1 shows an encouraging first-session state. Use Victory Native or react-native-svg for the bar chart.
3. **Profile** — avatar, name, handle, joined date, streak/XP/rank stats, settings (daily goal, default blocklist, reminders, subscription stub, sign out). Anonymous users see a "Save your progress — Sign in with Apple" card at the top. Use Profile to switch the `phase` flag manually for dev testing.
4. **Friends** — Day-1: blurred leaderboard preview + "Add 1 friend to unlock" CTA → Invite. Established: weekly leaderboard with real ranking. v1 ships in Day-1-only mode (Friends backend is Phase 7+).
5. **Invite** (separate screen, not a tab) — referral link `focuslyy.app/r/{username}` with Copy button (use `Clipboard` from `expo-clipboard`, show "Copied ✓" feedback), pre-written invite message, real Share intent, "0 of 3 joined" progress bar.

**Exit criteria:** every tab renders, the Day-1 / Established toggle in Profile flips states correctly across all tabs, Stats reflects my real session history, Invite copies the link and opens a share sheet.

### Phase 5 — Auth + paywall stubs

Read §B.5 (Auth + Paywall).

Implement the auth flow following the anonymous-default pattern we locked in:

- User can complete the entire funnel (including the paywall) without creating a focuslyy account
- On successful purchase (which is stubbed in this phase), prompt with "Save your subscription and streak — Sign in with Apple" — one-tap if they accept, dismissible if they decline
- Persistent "Save your progress" card in Profile if still anonymous
- When they later sign in, link the local profile/sessions to the new account ID

Use Apple Sign-In (`expo-apple-authentication`) and Google Sign-In (`@react-native-google-signin/google-signin`). For the anonymous path, generate a UUID on first launch and store in `useProfileStore`.

Stub the paywall: tapping a plan tile shows a native alert "Subscribe (dev stub)" with options "Simulate success" / "Simulate cancel." Success path triggers the post-purchase account-save prompt. This stub gets replaced with real RevenueCat in Phase 7.

**Exit criteria:** I can complete the funnel anonymously, get to "successful purchase" via the stub, see the account-save prompt, accept or decline, and either flow lands me in the core app with my state intact.

### Phase 6 — Polish, transitions, device test

Read §D (State Model) for the persistence audit. Then do a polish pass on everything built so far:

- Add screen transitions (push + fade for stack navigation, slide-up for modals)
- Add haptic feedback on key actions (use `expo-haptics`): seal apps (light), start session (medium), block complete (success), break the seal early (warning)
- Add micro-interactions: tap-press scale-down on Buttons, the goal ring on Home animating to current % on mount, the Locked screen ring updating smoothly each tick
- Audit every screen for empty states, loading states, error states
- Audit every CTA for the "leads somewhere real" rule
- Run on a real iPhone via Expo Go or a TestFlight dev build — simulator hides real-device issues (Safe Area Insets, Dynamic Island spacing, keyboard avoidance)
- Fix any layout issues that appear only on device
- Add proper accessibility labels (`accessibilityLabel`, `accessibilityHint`) to all interactive elements

**Exit criteria:** the app runs on my actual iPhone smoothly. Every screen feels considered. No jank on countdowns or transitions. Haptics fire on the moments that matter. Closes Phase 6 with a TestFlight build I can hand to ~5 beta testers.

### Phase 7 — Native work: Family Controls + RevenueCat

**PRE-REQUISITE:** Apple's Family Controls (Distribution) entitlement must be approved before this phase ships. Start that request the day you start Phase 1 — it's the long pole and is on Apple's timeline, not ours. If the entitlement isn't approved yet, do Phase 8 (App Store assets) first to fill the wait.

This phase requires ejecting from Expo's managed workflow into a custom dev client. Run `npx expo install expo-dev-client` and follow the migration. From here on, simulator builds happen via `npx expo run:ios`, not Expo Go.

**App blocking (the core differentiator):**

1. Install `react-native-device-activity` (kingstinct package)
2. Set up the Expo config plugin per the package README
3. Add the `com.apple.developer.family-controls` entitlement (Distribution variant) to the iOS config
4. Rewrite the Seal Apps screen: replace the named-app toggle UI with a button that launches Apple's `FamilyActivityPicker` system sheet. Store the returned selection (opaque tokens) in `useProfileStore` as the default blocklist
5. On session start: apply a `ManagedSettingsStore` shield over the selected app tokens. On break start: keep the shield. On session end OR long-press break-the-seal: lift the shield
6. Test with real apps. The blocking should be enforced by the OS, not just hidden behind our UI

**Subscriptions:**

1. Install RevenueCat SDK (`react-native-purchases`)
2. Configure products in App Store Connect AND RevenueCat dashboard: weekly $5, monthly $10, annual $80, plus a $5 intro offer for monthly (the discount path)
3. Replace the Phase 5 paywall stub with real `Purchases.purchasePackage()` calls
4. On successful purchase: trigger the existing account-save prompt from Phase 5
5. Anonymous-to-account linking: when an anonymous user signs in after purchase, call `Purchases.logIn(appUserId)` to associate the subscription with the new account ID. This is how RevenueCat preserves subscriptions across the anonymous-to-signed-in transition
6. Build a "Restore purchases" button in Profile (Apple requires this for App Store approval)

**Exit criteria:** I can pick apps via Apple's picker, start a focus session, ACTUALLY get blocked from opening TikTok (etc.) on a real device for the session duration, and the shield lifts on session end. I can purchase via real StoreKit in sandbox mode, sign in after, and my subscription survives a full app reinstall.

### Phase 8 — App Store assets + submission

Build the App Store submission package:

1. **Icon:** finalize the 1024×1024 from `assets/icons/icon-1024.png`, re-rendered with real Fraunces Black Italic loaded (see `assets/icons/README.md`)
2. **Screenshots:** required at 6.7" (iPhone 15 Pro Max) and 6.1" (iPhone 15 Pro) sizes. Capture 5-7 frames from the real running app:
   - Hero — locked screen with timer running
   - The seal moment — choosing apps to block
   - Stats — week-over-week climb
   - Streaks/rank — Profile screen
   - Share card example
3. **Preview video:** 15-30 seconds, no audio required. Screen-record a full session from setSession → locked → break → log win → share. Keep it human-paced
4. **App Store listing copy:**
   - Name: "Focuslyy" (capitalized in store, lowercase in app)
   - Subtitle: "Seal the apps. Do deep work."
   - Description: lead with the cost-of-waiting frame, then the seal mechanic, then social-proof (real reviews if you have them by now)
   - Keywords: focus, deep work, app blocker, ADHD, study, productivity, screen time, distraction
   - Privacy policy URL: must be hosted at focuslyy.app/privacy before submission
   - Terms URL: focuslyy.app/terms
5. **App Privacy disclosures** in App Store Connect — declare exactly what data is collected (Anonymous: usage analytics if any; Signed-in: name, email, app activity). Be honest, App Review checks this.
6. **Family Controls usage justification** — App Review will ask why you need this entitlement in production. Have a one-paragraph explanation ready: "focuslyy uses Family Controls and DeviceActivity to allow users to voluntarily restrict their own access to selected apps during user-initiated focus sessions, supporting the core use case of self-directed deep work."

Submit. Expect 24-72h review. Be ready for one revision request.

---

## §B — Screen-by-screen specification

(Reference Claude Code can read while building each phase.)

### §B.1 Onboarding funnel

Architecture: stack navigator under `app/(onboarding)/`. Progress bar component at top of every screen. Progress values: start 4 · q1 12 · q2 24 · q3 36 · results 48 · symptoms 56 · help 64 · reviews 72 · features 80 · plan 90 · paywall 96 · discount 98 · firstSeal 100.

**Start** — Hook screen. Big ring icon (countdown-style) at top. Headline: "While you scroll, everyone else is building." Subhead about the average person losing 4+ hours a day — note: this screen makes claims about the average person only, never about "you," because we haven't asked anything yet. CTA: "Find out in 60 seconds."

**Q1 — Phone hours (multi-choice, single-select)** — "How many hours a day are you on your phone?" Options: Under 2 hrs / 2–4 hrs / 4–6 hrs / 6+ hrs. Save selection to `quizStore.hoursBand`. Compute and save:

- `hoursNum`: midpoint of band (1, 3, 5, 7)
- `yrNum`: hoursNum × 365 (rounded to nearest hundred)
- `barH`: visual bar height ratio vs. 4.62 (the cited average)

**Q2 — Distractions (multi-choice, multi-select)** — "What steals your focus most?" Options: Short-form video (TikTok/Reels) / Social media / Games / YouTube + streaming / News / Texting + calling. Save as array. Used to pre-check the Seal screen's recommended apps.

**Q3 — Goal (multi-choice, single-select)** — "What would you build if your phone stopped winning?" Options map to mode + projection:

| Option                 | Mode    | 30-day projection                  |
| ---------------------- | ------- | ---------------------------------- |
| A business or app      | Build   | your app, shipped                  |
| A fitter body          | Train   | a stronger body                    |
| A degree or new skill  | Study   | real progress on your degree       |
| A creative project     | Create  | your project, made                 |
| Read more books        | Read    | a stack of books finished          |
| Just my time back      | Reclaim | your time, back in your hands      |

**Results** — "You're handing your phone {hoursNum} hrs every day." Subhead compares to the real 4.62 hours/day average (cited). If `hoursNum < 4.62`, reframe honestly ("Still hours worth reclaiming"), don't shame. Bar chart: AVG bar (height 88) vs YOU bar (height = barH * 96). Line: "That's ~{yrNum} hours a year. A master's degree. A fluent language. A business. Gone — every year you wait." CTA: "See what it's costing me."

**Symptoms** — "The cost of waiting." Background shifts crimson-warm. Three agitation lines about the gap growing, the finisher-you drifting away, apps winning by default. CTA: "Show me the fix."

**Help** — "How focuslyy works." Three-step diagram: seal apps → do deep work → focuslyy turns hours into visible output. CTA: "Your focus starts now."

**Reviews** — "You're not alone." Display the real waitlist count (from Supabase when wired, or a placeholder labeled `[X]` for now — never an invented number). Two ★★★★★ founding-member quotes (placeholders until you have real ones, labeled). CTA: Continue.

**Features** — "What you get." Four feature cards: The Seal · Deep-work tracking · Streaks & ranks · Duels (note: Duels are v1.1 — keep the card but it's directional). CTA: "Build my plan."

**Plan (THE CONVERSION MOMENT)** — "Build the plan you'll actually do." Subhead: short. Then customization:

- Name input ("What should we call you?")
- Daily goal: 4 buttons (1H / **2H selected** / 3H / 4H)
- Days per week: 3 buttons (3 / **5 selected** / 7)
- Live projection card (**TAPPABLE — this card IS the CTA**): "YOUR NEXT 30 DAYS / ≈{goal × days × 4.3} hours of deep work — {name}, {projection}." Right side: amber arrow.

No separate big CTA button at the bottom — the projection card itself advances to the paywall. This was a hard-earned design decision: a separate amber button competed with the customization controls.

**Paywall** — "The expensive option isn't focuslyy." Two side-by-side cards:

- YOU'RE LOSING (crimson border, soft crimson bg): "~{yrNum.toLocaleString()}" hours every year, = "{projection} — gone."
- FOCUSLYY COSTS (teal border, soft teal bg): "22¢" per day · yearly · "Less than one coffee a week."

Bridge line italic: "Which one is actually expensive?"

Three plan tiles below (yearly highlighted as BEST VALUE, pre-selected): Yearly $80 · Monthly $10 · Weekly $5. CTA: "Take my hours back" (personalized with name if entered → "Take my hours back, {name} →"). Secondary: "Maybe later" → discount.

**Discount** — "Wait — start for less." First month $5 (was $10). CTA: "Claim my offer." Secondary: "No thanks" → firstSeal anyway. Don't trap them.

**FirstSeal** — "You're in. Let's run your first seal — just 5 minutes." Drops them into a real 5-minute session so they feel the product. CTA: "Start my first seal" → into the session stack at the Seal Apps step with a 5-minute preset.

### §B.2 Core app — session flow

**Set Session** — "What's the one thing that matters most right now?" Real text input + suggestion chips (taken from `goalTasks[mode]`, where mode comes from quizStore):

- Build: ['Ship one feature', 'Fix the top bug', 'Write the landing copy']
- Train: ['Full workout — no phone', 'Meal prep the week', 'Plan + log training']
- Study: ['One full lecture + notes', 'Past-paper practice set', 'Read & summarize a chapter']
- Create: ['Draft the next scene', 'Edit one video', 'Sketch three concepts']
- Read: ['Read 30 pages', 'Finish the chapter', 'Read — no skimming']
- Reclaim: ['One real task, start to finish', 'Inbox to zero', "The thing you keep avoiding"]

Block-length picker: 15 / **30 (default)** / 60 / 90 buttons + a custom-minutes input (cap 240). Mode pill displays mode. CTA: "Choose what to block →" → Seal Apps.

**Seal Apps (Phase 3 — UI only; Phase 7 — real)** — "Block what pulls you out." Phase-3 list of toggleable named apps with pre-checks from Q2 (TikTok/IG/YT on by default if Short-form was picked; add Messages if Texting was picked). Live count badge. CTA: "Seal & start ritual →" → Ritual. Phase 7 replaces the list with a button that launches Apple's FamilyActivityPicker. Visual stays the same — only the interaction changes.

**Ritual** — 0:30 countdown. Four prep cues with check icons: clear desk, water within reach, silence everything, three deep breaths. Copy: "Don't skip this — it's how your brain learns the seal means focus." CTA: "I'm ready — start now" → Locked.

**Locked (the centerpiece)** — Darkest background. Pill: "PHONE SEALED · {count} BLOCKED." Big amber ring countdown using `RingTimer` component, set to `state.blockMin` minutes. Below: "YOU'RE WORKING ON {task}." Demo control: "Block complete" (real build: this fires automatically when timer ends). "Hold to break the seal" — long-press only, never tap-to-exit. This is deliberate friction.

**Break** — "Block done — nice. Take a real break." Background shifts toward teal. 5-minute countdown. Critical message: "Your apps stay sealed." + "Don't scroll — it drains the energy you just built." Restorative chips: Stretch · Walk · Water. CTAs: "Start next block" → Seal Apps · "End for now" → Log Win.

**Log Win** — "Session complete." Stat row: TIME (computed from blockMin) · XP (+120 for now, real formula later) · STREAK (🔥{days}). Real text input prefilled with placeholder "Add a note about '{task}'…" The label above reads "DID YOU FINISH: '{task}'?" if a task was entered. One-tap completion chips by mode (`logChips[mode]`): Build → ['Shipped it ✓', 'Made progress', 'Got unstuck'] etc. CTA: "Save & share my day" → Share. Saves the session to `useSessionsHistoryStore`.

**Share** — Branded share-card preview: "TODAY I LOCKED IN FOR {total today} of deep work · 🔥{streak}-day streak / Seal the apps. Do deep work. / @focuslyy · focuslyy.app." CTA: "Share to Instagram Story" (opens `Share` intent with the rendered image — use `react-native-view-shot` + `expo-sharing`). Secondary: "More options."

### §B.3 Tabs

(Full content covered in Phase 4 prompt above; details in prototype.)

### §B.4 Day-1 vs Established states

`useProfileStore.phase: 'day1' | 'established'`. Day-1 is the default for a brand-new user. Transition to 'established' when the user adds their first friend (manual flag in v1, automatic in v1.1 when Friends backend ships).

Day-1 implications (DO NOT SKIP):

- **Home:** streak shows 🔥1, friends-row replaced by invite-bootstrap card
- **Friends tab:** shows blurred locked leaderboard with "Add 1 friend to unlock" CTA, NEVER fake friends
- **Stats:** shows first-session encouragement, empty bar chart, "1h banked so far" hero stat (or 0 if no sessions yet)
- **Profile:** shows persistent "Save your progress — Sign in with Apple" card if anonymous

### §B.5 Auth + paywall

Anonymous-default, account-on-purchase prompt. Covered in Phase 5 prompt and CLAUDE.md.

---

## §C — Data binding map (every value in the app traces back to here)

```
Q1 hours band ─┬─► Results: headline number (hoursNum = band midpoint)
               ├─► Results: annualized "hours a year" (yrNum)
               ├─► Results: YOU bar height (barH vs avg 4.62)
               └─► Paywall: YOU'RE LOSING headline number

Q2 distractions ─┬─► Seal screen: pre-checked apps ("FOR YOU")
                 └─► Plan screen: blocklist line (top 3)

Q3 goal ─┬─► Plan: MODE label + projection text
         ├─► Set Session: mode pill
         ├─► Set Session: TRY chips (from goalTasks[mode])
         ├─► Log Win: completion chips (from logChips[mode])
         └─► Paywall: YOU'RE LOSING outcome line

Plan customization ─┬─► Profile: dailyGoal, commitDays, name persist
                    └─► Home goal ring: dailyGoal × 60 min target

Task input (Set Session) ──► Locked: "you're working on {task}"
                              Log Win: "did you finish: '{task}'?"
                              Share card: caption hook

Block length (Set Session) ─► Locked: countdown duration
                              Log Win: TIME stat

Seal selection (Seal screen) ► Locked: "{n} blocked" count
                               Profile: default blocklist if saved

Sessions history ─┬─► Home: today's goal ring, streak chip
                  ├─► Stats: all metrics, bar chart, recent sessions
                  ├─► Profile: streak, XP, rank
                  └─► Share card: today's total

phase (day1/established) ─┬─► Home: invite-bootstrap vs friends row
                          ├─► Friends tab: blurred preview vs real board
                          ├─► Stats: empty-state messaging vs full
                          └─► Profile: "save your progress" card visible
```

Rule: if a screen displays a value, you should be able to point to a line above explaining where it came from. If you can't, the value is fabricated and the screen is broken.

---

## §D — State model

Zustand stores in `src/state/`, all with `persist` middleware to AsyncStorage.

```ts
// quizStore
{ hoursBand, hoursNum, yrNum, barH, distractions[], mode, projection }

// profileStore
{ id (UUID for anon, real ID after sign-in), name, handle, joinedAt,
  authProvider: 'anonymous' | 'apple' | 'google',
  dailyGoal, commitDays, defaultBlocklist[],
  phase: 'day1' | 'established',
  streakDays, bestStreak, totalXp, rank }

// sessionStore (current/in-flight session)
{ task, blockMin, mode, blockedApps[], startedAt }

// sessionsHistoryStore
{ sessions: Array<{
    id, startedAt, endedAt, durationMin, mode, task, note,
    completed: boolean, blockedApps[]
}> }

// settingsStore
{ notifications: { streakAtRisk, dailyGoalHit, scheduledReminder, logYourWin },
  reminderTime, quietHoursStart, quietHoursEnd,
  subscription: { status, tier, renewsAt } }
```

---

## §E — Native work (Phase 7 — handed off to the dev)

Already covered in Phase 7 prompt above and in CLAUDE.md's "Tech stack" + "What to never do" sections. The TL;DR:

1. Family Controls (Distribution) entitlement — request from Apple Day 1. Long pole.
2. `react-native-device-activity` — the React Native bridge to Apple's APIs. Requires custom dev client (not Expo Go).
3. The Seal screen mechanism changes in Phase 7: from named-app toggles to Apple's `FamilyActivityPicker`. Tokens are opaque.
4. RevenueCat + StoreKit 2 — handles weekly/monthly/yearly + intro price + cross-device subscription state. Anonymous-to-account linking via `Purchases.logIn()`.
5. Restore Purchases button — Apple requires this for IAP apps.

### Useful commands

```bash
# Dev
npx expo start                  # Start Metro
npx expo start --ios            # iOS simulator
npx expo start --clear          # Clear Metro cache

# Real device (after Phase 7 — Expo Go won't work for native modules)
npx expo run:ios                # Build dev client to plugged-in iPhone

# Type check
npx tsc --noEmit

# Lint
npx expo lint

# Submit (Phase 8)
eas build --platform ios --profile production
eas submit --platform ios
```
