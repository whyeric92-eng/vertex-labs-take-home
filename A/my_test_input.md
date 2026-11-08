# My own test input

Designed to break a typical extraction prompt. Fictional companies.

## Input

```
Singapore-based climate startup GridCool said on Tuesday it has raised S$40 million (about US$30.8 million) in a Series D round co-led by Tembusu Partners and Orchid Capital, with participation from Lumen Ventures. The company previously raised a US$4 million seed round in 2024. GridCool's chief executive said the money will fund expansion into Vietnam. Separately, logistics firm HaulHub, which was acquired by Kargo last month, confirmed it is not raising new funds. Kuala Lumpur edtech BrightPath also closed a pre-Series A round from angel investors, without disclosing the amount. And Singapore insurtech CoverLah raised $5 million in seed funding led by Ember Ventures.
```

## What it tests

| Trap | Expected |
|---|---|
| Non-USD amount with a USD figure given | GridCool `amount_usd` = 30800000 (the stated USD figure, not S$40M) |
| Series D | `round` = "Series C+" |
| Two co-leads plus a participant | leads = Tembusu Partners, Orchid Capital; not Lumen Ventures |
| Past round as background | No separate entry for the 2024 seed |
| Expansion country | GridCool `hq_country` = Singapore, not Vietnam |
| Acquisition, explicitly no raise | No entry for HaulHub or Kargo |
| Round type outside the list | BrightPath `round` = "Unknown", `amount_usd` = null, leads = [] |
| City only | BrightPath `hq_country` = Malaysia |
| Bare "$" from a Singapore company | CoverLah `amount_usd` = 5000000 (my rule: bare $ is USD; could be S$ in reality) |

## Expected output

`evidence` may vary as long as it is an exact quote covering the round and amount.

```json
{
  "companies": [
    {
      "name": "GridCool",
      "hq_country": "Singapore",
      "sector": "climate",
      "round": "Series C+",
      "amount_usd": 30800000,
      "lead_investors": ["Tembusu Partners", "Orchid Capital"],
      "evidence": "raised S$40 million (about US$30.8 million) in a Series D round"
    },
    {
      "name": "BrightPath",
      "hq_country": "Malaysia",
      "sector": "edtech",
      "round": "Unknown",
      "amount_usd": null,
      "lead_investors": [],
      "evidence": "closed a pre-Series A round from angel investors, without disclosing the amount"
    },
    {
      "name": "CoverLah",
      "hq_country": "Singapore",
      "sector": "insurtech",
      "round": "Seed",
      "amount_usd": 5000000,
      "lead_investors": ["Ember Ventures"],
      "evidence": "raised $5 million in seed funding led by Ember Ventures"
    }
  ]
}
```
