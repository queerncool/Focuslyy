# Best times to post · @jemsocialapp

Pulled from AdaptlyPost analytics on Mon Oct 26, 2026. The window is Apr 29 to Oct 23, 2026: 164 Instagram posts and 51 Threads posts with metrics. All times are Central (Houston).

Each post's views are compared with the median of the account's other posts within 21 days of it. That way a slot doesn't get credit just because it was used during a strong month. Threads reach dropped a lot in October, when almost every post went out at 7 am, so this check matters there.

## Instagram

| slot (CT) | posts | views vs. same-period median | share of posts beating the median |
| --- | --- | --- | --- |
| **7 pm** | 10 | **1.45x** | **90%** |
| 11 am | 9 | 1.21x | 89% |
| 8 am | 25 | 0.97x | 40% |
| **12 pm (old slot)** | 15 | **0.80x** | **27%** |

- Noon is the weakest hour this account has used, and it's where the three carousels were first scheduled.
- Monday is the best weekday (1.25x). Thursday brings the most comments and shares (26 across 27 posts). The creators, founders and brands days all line up with that.

## Threads

| slot (CT) | posts | views vs. same-period median | share of posts beating the median |
| --- | --- | --- | --- |
| **12–3 pm** | 5 | **1.85x** | **100%** |
| 7 am (current daily slot) | 10 | 0.56x | 40% |
| 7 pm | 3 | 0.25x | 0% |

- Midday also brought the most comments and shares (15).
- Wednesday is the best Threads day (1.66x). Thursday is the weakest: none of 7 posts beat their period median.
- Samples are small (3 to 10 posts per hour), so read these as direction, not law. Re-run after the AfroTech posts come in.

## Applied to the AfroTech carousels

| post | Instagram | Threads |
| --- | --- | --- |
| creators | Mon Oct 26, 7:00 pm | Mon Oct 26, 1:00 pm |
| brands | Thu Oct 29, 7:00 pm | **Wed Oct 28, 12:30 pm** (Wednesday is the best Threads day, Thursday the weakest) |
| founders | Mon Nov 2, 7:00 pm (CST) | Mon Nov 2, 1:00 pm (CST) |

Threads goes at 1 pm, not noon, on Oct 26 and Nov 2 because a UGC opportunity post already sits at 12:00 those days. On Wed Oct 28 noon is free, so brands goes at 12:30, 75 minutes after the 11:15 post.

## Other Threads posts moved

The two remaining 7 am Threads posts (the 0.56x slot) moved into the midday window:

| post | was | now |
| --- | --- | --- |
| "Where top apps found their creators" | Mon Oct 26, 7:00 am | Mon Oct 26, 2:00 pm |
| "Creator mistakes even big apps made" | Tue Oct 27, 7:00 am | Tue Oct 27, 12:30 pm |

The 8 am to 11:15 am slots stay as they are. 8 am tests strong (3.15x, though only 3 posts), and 9 am and 11 am are close to typical (0.91x and 0.85x). That's not enough evidence to move 30+ posts.

## Re-running

1. Export per-post metrics with AdaptlyPost `list_post_analytics` (one platform at a time, `limit: 100`, page through).
2. Filter to the @jemsocialapp connection ids:
   - Instagram `cmuqo31f6005x01o2qvd8q8vd`
   - Threads `cmv6owlu1001m01pnr4h9tvuu`
3. Write `ig.tsv` (publishedAt, views, likes, comments, shares, saves) and `threads.tsv` (publishedAt, views, likes, comments, shares).
4. Run `python3 analyze.py` for the raw medians and `python3 analyze2.py` for the period-adjusted view.
