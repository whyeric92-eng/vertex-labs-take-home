# Vertex Labs intern take-home

Answers to the three sections, with the code and raw outputs behind them. Commits are small and in the order the work was done, so the history shows the process.

| Section | Answer | Supporting files |
|---|---|---|
| A. Prompt and evaluate | [`A/prompt.md`](A/prompt.md), [`A/NOTES.md`](A/NOTES.md) | [`A/my_test_input.md`](A/my_test_input.md), [`A/run_eval.py`](A/run_eval.py), raw outputs in [`A/outputs_v2/`](A/outputs_v2/) (submitted prompt) and [`A/outputs_v1/`](A/outputs_v1/) (first version) |
| B. Messy data | [`B/ANSWER.md`](B/ANSWER.md) | [`B/analysis.py`](B/analysis.py), [`B/rounds.csv`](B/rounds.csv) |
| C. Code review | [`C/REVIEW.md`](C/REVIEW.md) | [`C/test_review.py`](C/test_review.py) (added tests), [`C/probe.py`](C/probe.py) (reproduces the bugs) |

AI log for all three sections: [`AI_LOG.md`](AI_LOG.md). Chat logs (selected turns, translated from Chinese): [`chat_exports/main_session.md`](chat_exports/main_session.md) and [`chat_exports/review_session.md`](chat_exports/review_session.md).

## Summary

- **A.** Content was correct in all 24 runs, including the injection snippet. The main failure is format: the model wrapped JSON in code fences in 9/12 runs; the revised prompt cut this to 2/12.
- **B.** Logistics: US$44.6M in Q3 2026. One row (LedgerLeaf, US$250M seed) looks like a data error and decides the answer; if it is above US$16.9M, Fintech is top instead.
- **C.** Merge with changes. The fix crashes when `last_contact` is `None`, sorts by string rather than time, and misses deals stale for more than 14 but under 15 days.

## How to run

Python 3.13, standard library except pytest.

```
pip install pytest

python B/analysis.py              # B: cleaning log and totals

cd C
python -m pytest -v               # C: 4 of the new tests fail on the PR's fix, as intended
python probe.py                   # C: shows each bug directly
cd ..

python A/run_eval.py outputs_v3   # A: reruns all 12 calls
```

A needs a Gemini API key: create a `.env` file in the repo root with one line, `GEMINI_API_KEY=your-key`.

`fix.py`, `test_fix.py` and `rounds.csv` are the files provided, unchanged. The brief PDF is not included.
