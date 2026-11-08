"""Tests added in review. Each one fails on the PR's fix.py and should
pass once the issues are fixed. All tests pass a fixed `today`."""
from datetime import datetime, timezone

from fix import deals_needing_followup

TODAY = datetime(2026, 11, 1, tzinfo=timezone.utc)


def deal(name, last_contact, stage="Sourcing"):
    return {"name": name, "stage": stage, "last_contact": last_contact}


def test_none_last_contact_is_returned_first():
    # Assumption: a deal never contacted counts as the most stale.
    deals = [
        deal("Old", "2026-09-01T09:00:00+08:00"),
        deal("Never", None),
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["Never", "Old"]


def test_sort_uses_real_time_not_string_order():
    # SG 21:00+08:00 = 13:00 UTC, IN 20:00+05:30 = 14:30 UTC.
    # SG is more stale, but "20:00" < "21:00" as strings.
    deals = [
        deal("IN", "2026-10-01T20:00:00+05:30"),
        deal("SG", "2026-10-01T21:00:00+08:00"),
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["SG", "IN"]


def test_just_over_14_days_is_returned():
    # 14 days 23 hours ago: no contact in the last 14 days.
    deals = [deal("Edge", "2026-10-17T01:00:00+00:00")]
    assert deals_needing_followup(deals, today=TODAY) == ["Edge"]


def test_just_under_14_days_is_not_returned():
    # 13 days 23 hours ago: still inside the window.
    deals = [deal("Recent", "2026-10-19T01:00:00+00:00")]
    assert deals_needing_followup(deals, today=TODAY) == []


def test_both_closed_stages_excluded_open_kept():
    deals = [
        deal("Won", "2026-09-01T09:00:00+08:00", stage="Closed - Won"),
        deal("Lost", None, stage="Closed - Lost"),
        deal("Open", "2026-09-01T09:00:00+08:00", stage="Diligence"),
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["Open"]


def test_realistic_mix():
    # Every kind of row the spec says real data contains, in one list.
    deals = [
        deal("Fresh", "2026-10-30T10:00:00+05:30"),
        deal("Never", None, stage="Diligence"),
        deal("IN", "2026-10-01T20:00:00+05:30"),
        deal("SG", "2026-10-01T21:00:00+08:00"),
        deal("Lost", None, stage="Closed - Lost"),
    ]
    assert deals_needing_followup(deals, today=TODAY) == ["Never", "SG", "IN"]
