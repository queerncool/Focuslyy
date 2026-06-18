# focuslyy — Claude Code Standing Instructions

You are helping build **focuslyy**, an iOS deep-work app that seals (blocks) distracting apps for focus sessions, then turns those locked-in hours into visible output, streaks, and friendly competition. **Target launch: July 10, 2026.** Target user: Gen Z and millennials, with **ADHD-friendly UX as a first-class concern**, not an afterthought.

Read `docs/BUILD.md` before starting any new phase. Read `docs/prototype.html` (open it visually if you can) when you need to understand a screen's exact look and feel — it's the canonical visual reference.

## Tech stack (locked)

- React Native + Expo (managed workflow, then ejected to a dev client for native modules in Phase 7)
- TypeScript, strict mode
- Expo Router for file-based navigation
- AsyncStorage for v1 local persistence (no backend until Phase 7)
- Supabase for v1.1 social layer (Phase 7+, not before)
- RevenueCat wrapping StoreKit 2 for subscriptions (Phase 7, native)
- `react-native-device-activity` (kingstinct) + Apple's Family Controls entitlement for real app blocking (Phase 7, native)

You will **NOT** try to implement real app blocking in JavaScript. You will **NOT** try to implement IAP receipts in JavaScript. Both are native iOS work explicitly deferred to Phase 7 — see "Native work" in BUILD.md.

## Brand system (locked — do not invent variants)

Palette (use these tokens exactly, no off-brand variants):

| Token        | Hex       | Use                                                |
| ------------ | --------- | -------------------------------------------------- |
| `amber`      | `#F2A03D` | Primary — CTAs, seal, accents                      |
| `amberLight` | `#F6B45E` | Hover / gradient highlights                        |
| `amberDeep`  | `#DE7A2C` | Pressed / gradient end                             |
| `espresso`   | `#18120E` | Dark backgrounds                                   |
| `ink`        | `#221A12` | Dark cards / dark-bg text                          |
| `cream`      | `#F2EBDD` | Light backgrounds                                  |
| `muted`      | `#8C8174` | Secondary text, inactive                           |
| `crimson`    | `#E5564B` | Only "break the seal" / cost-of-waiting accents    |
| `teal`       | `#4FB6A0` | Break / positive states                            |

Centralize tokens in `src/theme/colors.ts`. **Never inline hex values in components.**

Fonts: **Schibsted Grotesk** (display, 700/800) + **Space Mono** (mono — timers, labels, stat numbers) + **Fraunces Black Italic** (marketing/onboarding accent — used in the app icon and a few onboarding hero moments). Load via `expo-font`. Centralize in `src/theme/fonts.ts`.

Logo / app icon: an italic lowercase "y" in amber on espresso. Source files in `assets/icons/`. The y is the only letter in the wordmark with a descender — the part of a letter that drops below the baseline. Below the surface. Where deep work happens. That's the story. Keep it lowercase. The wordmark is always lowercase "focuslyy."

Voice: action-oriented, in the user's voice. CTAs describe what they're DOING, never tell them who they'll BE.

- ✅ "Lock in," "Take my hours back," "Save & share my day," "Start"
- ❌ "Become this person," "Transform your life," "Unlock the new you"

## Six non-negotiable UX principles

These get checked on every screen. Violations are bugs.

1. **Every number traces to a real input or a cited stat.** No fabricated percentiles. No "you're in the top 8%." Results derive from quiz answers vs. the cited 4h 37m daily average. If you don't have the data, don't display the number.
2. **Every screen has a defined Day-1 state.** A brand-new user has zero sessions, zero friends, no streak. Day-1 states show invite prompts and onboarding nudges — NEVER fake friends, NEVER fake leaderboards, NEVER fake activity. Use the `phase` state field (`'day1' | 'established'`) to switch.
3. **Anything shown as user-provided must be capturable.** The "what's the one thing" task is a real text input. The blocklist is real toggles. The log-win note is a real text input. If a screen shows "user content," there must be a place the user actually entered it. This was bug #3 in the prototype iterations; do not repeat it.
4. **Every CTA leads somewhere real.** No dead-end buttons. "Invite friends" opens a real invite screen with a real share intent. "Share to Instagram Story" opens a real share sheet. If you're going to show a button, it has to do the thing.
5. **No fake social proof pre-launch.** Review counts are real (pulled from Supabase waitlist) or placeholders explicitly marked as such. Reviews are real founding-member quotes — not invented. Do not fire the iOS rating prompt during onboarding.
6. **No fabricated user content in any screen.** This is the rule I got bitten on three times: don't pre-fill a "user's" note with example text, don't show fake recent sessions on Day 1, don't put example friends in the leaderboard. If you find yourself dropping in placeholder text that reads as the user's voice, stop and make it an empty state instead.

## File structure (use this layout)

```
focuslyy/
├── CLAUDE.md                 ← you're reading this
├── docs/
│   ├── BUILD.md              ← phased build plan + screen-by-screen spec
│   └── prototype.html        ← visual reference (open in browser)
├── assets/
│   ├── icons/                ← favicon set, app icon source SVGs
│   └── fonts/                ← Fraunces, Schibsted Grotesk, Space Mono ttf files
├── app/                      ← Expo Router routes (file-based)
│   ├── (onboarding)/         ← onboarding stack, no tab bar
│   ├── (app)/                ← main app, tab bar (Focus, Friends, Stats, Profile)
│   └── (session)/            ← modal session flow (setSession → seal → ritual → locked → break → logWin → share)
├── src/
│   ├── theme/                ← colors, fonts, spacing
│   ├── components/           ← reusable UI (Button, Card, Pill, BlockPicker, etc.)
│   ├── state/                ← Zustand stores: quiz, profile, session, sessions[], phase
│   ├── lib/                  ← utilities: time math, persistence wrappers
│   └── types/                ← shared TypeScript types
└── package.json
```

State management: Zustand with `zustand/middleware/persist` to AsyncStorage. One store per concern (quiz, profile, sessions, settings). No Redux. No Context-for-state.

## What to do at the start of every new Claude Code session

1. Read `CLAUDE.md` (this file — auto-loaded but verify you have it)
2. Skim `docs/BUILD.md` for the phase the user is currently on (they'll tell you)
3. Check `git status` and `git log -5` to see what was done last
4. Ask the user which phase prompt they're pasting (1 through 8) if it's not obvious

## What to never do

Never reproduce a bug from the prototype. Specific recurring failures:

- Fake user content masquerading as the user's notes (Log Win screen)
- "Restart the flow" buttons appearing in the live app UI (those were demo-only)
- Stray buttons leaking outside their parent views (caused the floating amber pill bug)
- A vertical bar + dot below it (always reads as an exclamation point — banned shape)

Never invent a stat, percentile, hourly value, or testimonial.

Never attempt real app blocking from JavaScript. Stub it with a labeled placeholder.

Never attempt real subscription payments from JavaScript. Stub with a labeled placeholder.

Never use bright colors outside the locked palette. No purple, no neon, no blue.

Never write a CTA that tells the user who they'll become. CTAs describe action.

Never ship a screen without a defined Day-1 state.

Never use placeholder Lorem Ipsum. Use the real prototype copy from `docs/BUILD.md`.

## What to do when stuck

If a screen's behavior or copy isn't clear from BUILD.md, open `docs/prototype.html` in a browser and look at the exact rendering. That HTML file is the canonical visual reference — every spacing, color, and word in it was approved by the founder over many iterations. Don't reinvent.

If something in BUILD.md and prototype.html conflict, **the prototype wins for visuals, BUILD.md wins for logic.**
