# Review session (second Claude Code session): selected turns

I used this session only to review work from the main session. Kept: each first review and each re-check after changes. Replies are condensed. Exported from Claude Code with `/export`.

---

## Section B

**Me:** *(attached the brief)* This session is for reviewing whether my current changes are correct.

**Reviewer:** Read the brief and `B/analysis.py`, and recomputed every sector total by hand: all match (Logistics 44.55M, Healthtech 37.39M, Fintech excl. LedgerLeaf 27.67M, Agritech 25.80M, Climate 13.68M). Cleaning steps are all correct. To change:
1. The comment says LedgerLeaf is ~80x the second-largest seed (US$3M). The second-largest is AgroSense at ~US$4.8M, so ~52x.
2. A comment says the Kirana rows share a "lead", but the CSV has no investor column.
3. The answer depends on LedgerLeaf: if its real amount is above ~US$16.9M (44.55 − 27.67), Fintech is top. Say so in the note; print the threshold.
4. Minor: duplicates are hard-coded, so say they were judged by hand. Logistics leads Healthtech by ~7M, of which 19.25M is an SGD conversion.
Also missing: the slide answer and partner note.

**Me:** And now?

**Reviewer:** Reran the script; numbers unchanged. Both comments fixed (52x, AgroSense, "lead" removed). The script prints "above US$16.9M", matching my calculation. `ANSWER.md` checked: "5 rounds" is right (Kirana, Portline, RouteNine, HaulHub, Dockside); note is 133 words. Still missing: AI log, and a commit.

---

## Section C

**Me:** Review C.

**Reviewer:** Solid. Ran every claim: all 9 problems hold; `probe.py` output matches 1, 2, 3, 5, 6; problem 7 holds (the test's string order happens to match time order). "4 fail on this PR, all pass once 1–3 are fixed" is true: I fixed only 1–3 in a scratch folder and all 10 tests passed. ~173 words. To change:
1. Use one of the brief's three options: "Merge with changes", not "request changes".
2. `test_excludes_closed` using the real clock is harmless; the real problem is `test_no_shared_state`.
3. Say why problems 5 and 6 have no tests.
4. Mention `probe.py`.

**Me:** And now?

**Reviewer:** All four applied, test results unchanged. Two new issues: ~211 words if each inline code span counts as one word (limit 200), with suggested cuts; and "see questions" points to problem 6, which has no question. Suggest adding "Should stage matching ignore case and whitespace?".

**Me:** And now?

**Reviewer:** Fixed: ~195 words by my count, and the questions now cover 5 and 6. Ready to commit.

---

## Section A

**Me:** Review my prompt and test input.

**Reviewer:** Well structured; every requirement has a rule; injection is handled. To change, most important first:
1. "$ with no other currency named" is ambiguous. Snippet 3 contains ₹, so the model may null CropIQ's $3M. Decide per amount instead.
2. "You may map a city": "may" is too weak and will vary between runs.
3. Evidence: allow joining two quotes with "..."; say what to quote when there's no amount.
4. Pre-Series A → Unknown is your own call; note it.
Test input: good coverage of 8 traps. Write the full expected JSON; add a bare-$ trap; consider a full-length article.

**Me:** And now?

**Reviewer:** Ready to run. The bare-$ rule is now per amount; "Map a named HQ city" (HQ also stops Vietnam being taken as GridCool's HQ); evidence rules are clear. Checked the expected JSON field by field. Run each input in a fresh call with default temperature, and keep raw outputs unedited even if malformed.

**Me:** Can I run `run_eval.py` now?

**Reviewer:** Yes. Dry-ran it without calling the API: the prompt and input parse correctly; the expected JSON scores 0 problems. Small issues: a comment says sector is checked but it isn't; lead investors are compared in order; a non-object reply crashes `check()`.

**Me:** Can I commit now?

**Reviewer:** Yes. All three fixed; re-tested: swapped leads pass, `[]` is reported without crashing, a wrong lead is caught. You also handled `companies` not being a list.

**Me:** It's finished running. What happened?

**Reviewer:** Content is correct in 12/12 runs; 9 are "not valid JSON" only because Gemini wrapped them in a ```json fence. Injection ignored; CropIQ's bare $3M read correctly; snippet 3 sector null (not stated in the article). Issues: fences (main problem), sector wording varies ("climate startup" vs "climate"), single-line vs indented layout. Suggest keeping these as v1, then naming fences explicitly in the prompt and constraining sector.

**Me:** How's the v2 prompt?

**Reviewer:** "Must start with { and end with }" is much more specific than "no markdown". Checked the backticks in the system message don't break `run_eval.py`'s parsing. Sector rule is clear.

**Me:** It's run. Can I push?

**Reviewer:** v2: content 12/12; format 10/12 bare JSON (v1: 3/12); the two fenced replies are a remaining failure: a prompt alone can't guarantee format, so production needs JSON mode or fence stripping. Sector now consistent. No API key anywhere in the history or working tree.

---

## Write-up

**Me:** Evaluate the notes.

**Reviewer:** Checked every number against the runs: all correct; ~149 words. Each of the three required parts has its own paragraph. Optional: some v1 replies were single-line and others indented, so "only evidence wording varied" isn't quite accurate; and say what the own test input targeted.

**Me:** Evaluate the AI log.

**Reviewer:** All three under 80 words; facts match; checked the 0.37 SGD figure. Two attribution points: the checker was tested on hand-made outputs by Claude Code, and the 10/10 local fix was written by Claude Code, so say so. Also link the chat exports.

**Me:** Evaluate the README.

**Reviewer:** Clear; summaries match the section files; the three provided files are unchanged since the first commit. Must fix: the `chat_exports/` link is dead. Suggested: handle a missing .env clearly; split `cd C && ...` for PowerShell; word the C summary more plainly.
