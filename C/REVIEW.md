# Section C: Review of the AI-written fix

## Problems, most severe first

1. `last_contact=None` crashes: naive `datetime.min` minus aware `today` raises `TypeError`. The spec says real data has these.
2. Sort uses the raw string, not the time. Mixed offsets sort wrong: SG `21:00+08:00` (13:00 UTC) lands after IN `20:00+05:30` (14:30 UTC).
3. `.days > 14` drops partial days: a deal 14 days 23 hours stale is not returned. Use `> timedelta(days=14)`.
4. Docstring says timestamps are normalised to UTC; the code never does this.
5. Naive `today` or naive timestamps also crash.
6. `startswith("Closed")` is case- and whitespace-sensitive.
7. `test_mixed_offsets...` passes by luck: its string order matches its time order.
8. `test_no_shared_state` tests nothing and uses the real clock; `test_excludes_closed` also uses it (harmless).
9. No tests for `None`, `Closed - Lost` or the 14-day boundary.

`probe.py` reproduces problems 1–3, 5 and 6.

## Decision: merge with changes

Problem 1 crashes on real data. Fixes 1–3 are a few lines; merge once `test_review.py` passes.

## Added tests

`test_review.py`: 4 fail on this PR, all pass once 1–3 are fixed. No tests for 5–6: the spec is unclear (see questions).

## Questions for the teammate

- Is exactly 14 days stale?
- Should never-contacted deals be listed first, or separately?
- Naive timestamps: assume UTC, or reject?
- Should stage matching ignore case and whitespace?
