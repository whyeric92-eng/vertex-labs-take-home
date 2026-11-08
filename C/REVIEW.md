# Section C: Review of the AI-written fix

## Problems, most severe first

1. `last_contact=None` crashes: naive `datetime.min` minus aware `today` raises `TypeError`. The spec says real data has these.
2. Sort uses the raw string, not the time. Mixed offsets sort wrong: SG `21:00+08:00` (13:00 UTC) lands after IN `20:00+05:30` (14:30 UTC).
3. `.days > 14` drops partial days: a deal 14 days 23 hours stale is not returned. Use `> timedelta(days=14)`.
4. Docstring says timestamps are normalised to UTC; the code never does this.
5. Naive `today` or naive timestamps also crash.
6. `startswith("Closed")` is case- and whitespace-sensitive.
7. `test_mixed_offsets...` passes by luck: its string order matches its time order.
8. `test_excludes_closed` and `test_no_shared_state` use the real clock; the latter tests nothing (no shared state exists).
9. No tests for `None`, `Closed - Lost` or the 14-day boundary.

## Decision: request changes

Problem 1 crashes on data the spec says exists, so this cannot merge. Fixes 1–3 are small.

## Added tests

`test_review.py`: 4 fail on this PR, all pass once 1–3 are fixed.

## Questions for the teammate

- Is exactly 14 days stale?
- Should never-contacted deals be listed first, or separately?
- Naive timestamps: assume UTC, or reject?
