"""Section B: which sector raised the most in Q3 2026 (Jul-Sep)?
Run from the repo root: python B/analysis.py
Standard library only. Every cleaning step prints what it changed."""
import csv
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

RATES = {"USD": 1.0, "SGD": 0.77, "INR": 0.012}  # given in the brief
Q3_START, Q3_END = date(2026, 7, 1), date(2026, 9, 30)

# Same round reported twice (by different sources), judged by hand. Keep the first row.
# Kirana Fleet: same round and amount, one day apart, one name has "Pte Ltd".
# PayLoom: same day, same round and amount, sector spelled "FinTech".
DUPLICATES = {("Kirana Fleet Pte Ltd", "AsiaDeals"), ("PayLoom", "Press release")}

# Seed round of US$250M is ~52x the next largest seed here (AgroSense, US$4.8M).
# Treated as a likely data error and excluded from the headline; see notes.
SUSPECT = {"LedgerLeaf"}


def parse_date(s):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):  # one row uses 18/09/2026
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date: {s}")


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean(rows):
    kept = []
    for r in rows:
        d = parse_date(r["date"])
        if not (Q3_START <= d <= Q3_END):
            print(f"  out of Q3     : {r['company']} ({r['date']})")
            continue
        if (r["company"], r["source"]) in DUPLICATES:
            print(f"  duplicate     : {r['company']} {r['round']} ({r['source']})")
            continue
        sector = "Fintech" if r["sector"].lower() == "fintech" else r["sector"]
        usd = float(r["amount"]) * RATES[r["currency"]]
        kept.append({**r, "date": d, "sector": sector, "usd": usd})
    return kept


def totals(rows, exclude=()):
    t = defaultdict(float)
    for r in rows:
        if r["company"] not in exclude:
            t[r["sector"]] += r["usd"]
    return sorted(t.items(), key=lambda kv: -kv[1])


def show(title, ranking):
    print(f"\n{title}")
    for sector, usd in ranking:
        print(f"  {sector:<11} US${usd / 1e6:7.2f}M")


if __name__ == "__main__":
    rows = load(Path(__file__).with_name("rounds.csv"))
    print(f"{len(rows)} rows loaded. Cleaning:")
    q3 = clean(rows)
    print(f"{len(q3)} Q3 rounds after cleaning.")

    headline = totals(q3, exclude=SUSPECT)
    show("Headline (LedgerLeaf excluded):", headline)
    show("If LedgerLeaf's US$250M is correct:", totals(q3))

    # How big LedgerLeaf's real amount must be for Fintech to take the top spot
    top_usd = headline[0][1]
    fintech_usd = dict(headline)["Fintech"]
    print(f"\nFintech overtakes {headline[0][0]} if LedgerLeaf's real amount "
          f"is above US${(top_usd - fintech_usd) / 1e6:.1f}M")
