# Section B: Top sector by Q3 2026 funding

## Answer (for the slide)

**Logistics: US$44.6M raised in Q3 2026 (5 rounds)**

## Note to the partner

What I changed:
- Kept July to September only (dropped one June and one October row).
- Removed two double-counted rounds (checked by hand): Kirana Fleet's Series A and PayLoom's Series B were each reported by two sources.
- Merged "FinTech" into "Fintech" and read 18/09/2026 as 18 September.
- Converted SGD and INR at the rates you gave.

Before you use it: LedgerLeaf is listed as a US$250M seed round, about 52 times the next largest seed here, so I think it's a data error and left it out. The answer depends on this one row: if LedgerLeaf's real amount is above about US$16.9M (e.g. US$25M with an extra zero), Fintech is top instead. Please confirm it before the meeting.

These figures come from news reports only, so undisclosed rounds are missing.

## How to reproduce

`python B/analysis.py` (standard library only). It prints each row it drops and the totals with and without LedgerLeaf.
