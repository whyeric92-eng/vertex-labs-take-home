"""Probe the PR's fix.py with inputs the original tests don't cover.
Run from the C folder: python probe.py"""
from datetime import datetime, timezone

from fix import deals_needing_followup

TODAY = datetime(2026, 11, 1, tzinfo=timezone.utc)


def run(label, deals, today=TODAY):
    try:
        print(f"{label}: {deals_needing_followup(deals, today=today)}")
    except Exception as e:
        print(f"{label}: CRASH {type(e).__name__}: {e}")


# 1. last_contact is None (spec says real data has these)
run("1 None last_contact", [
    {"name": "Never", "stage": "Sourcing", "last_contact": None},
])

# 2. Sort uses raw strings, not real time.
#    SG 21:00+08:00 = 13:00 UTC, IN 20:00+05:30 = 14:30 UTC -> SG is more stale.
run("2 sort order (expect ['SG', 'IN'])", [
    {"name": "IN", "stage": "Sourcing", "last_contact": "2026-10-01T20:00:00+05:30"},
    {"name": "SG", "stage": "Sourcing", "last_contact": "2026-10-01T21:00:00+08:00"},
])

# 3. 14 days 23 hours ago: outside the last 14 days, but .days == 14
run("3 14d23h ago (expect ['Edge'])", [
    {"name": "Edge", "stage": "Sourcing", "last_contact": "2026-10-17T01:00:00+00:00"},
])

# 4. Caller passes a naive 'today'
run("4 naive today", [
    {"name": "X", "stage": "Sourcing", "last_contact": "2026-09-01T09:00:00+08:00"},
], today=datetime(2026, 11, 1))

# 5. Timestamp without an offset
run("5 naive last_contact", [
    {"name": "Y", "stage": "Sourcing", "last_contact": "2026-09-01T09:00:00"},
])

# 6. Closed - Lost and a lowercase variant
run("6 closed variants (expect [])", [
    {"name": "Lost", "stage": "Closed - Lost", "last_contact": "2026-09-01T09:00:00+08:00"},
    {"name": "lower", "stage": "closed - lost", "last_contact": "2026-09-01T09:00:00+08:00"},
])
