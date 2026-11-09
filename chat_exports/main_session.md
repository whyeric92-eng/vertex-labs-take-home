# Main session (Claude Code): selected turns

Kept: the turns where I asked Claude Code to do work, or passed on review feedback for it to act on. Claude's replies are condensed to what it did and found. Exported from Claude Code with `/export`.

---

## Section C

**Me:** OK, I've read fix.py. One problem is the timezone issue. What else?

**Claude:** Wrote `C/probe.py` with inputs the original tests don't cover and ran it. Results: `last_contact=None` crashes (naive `datetime.min` minus aware `today`); mixed offsets sort wrong (string sort, not time); a deal 14 days 23 hours stale is not returned (`.days` drops partial days); naive `today` or naive timestamps crash; lowercase "closed - lost" isn't excluded. Also: the docstring claims UTC normalisation that never happens, the mixed-offset test passes by luck, `test_no_shared_state` tests nothing, and there are no tests for None, Closed - Lost or the 14-day boundary. Leaning towards not merging as is.

**Me:** Pushed. Write the tests.

**Claude:** Wrote `C/test_review.py` (6 tests, fixed `today`). On the PR's fix.py: 4 fail, 2 pass (the 2 are regression guards). Wrote a minimal fix in a scratch folder, not the repo, to check the tests themselves: all 10 tests (4 original + 6 new) pass. Assumption recorded: a never-contacted deal counts as most stale.

**Me:** Pushed. Write the review.

**Claude:** Wrote `C/REVIEW.md`: 9 problems ranked, decision, added tests, 3 questions for the teammate (exactly 14 days? where do never-contacted deals go? naive timestamps?). ~161 words.

**Me:** *(pasted a second AI's review of Section C)* 1. The decision must use one of the brief's options (Merge / Merge with changes / Reject); "request changes" isn't one. 2. `test_excludes_closed` using the real clock is harmless; the real issue is `test_no_shared_state`. 3. Say why problems 5 and 6 have no tests. 4. Mention probe.py. Which of these should we change?

**Claude:** All four are right. Changed the decision to "Merge with changes" with a merge condition, made item 8 precise, explained the missing tests, referenced probe.py. That went to 205 words, so trimmed to 197.

**Me:** *(pasted the second AI's follow-up)* It's ~211 words if each inline code span counts as one word; and "see questions" doesn't cover problem 6.

**Claude:** Both right. Compressed as suggested and added "Should stage matching ignore case and whitespace?". Counted three ways: 181 / 195 / 200 words.

---

## Section B

**Me:** Pushed. Let's do B.

**Claude:** Wrote `B/analysis.py` (standard library only; prints every row it drops). Cleaning: kept July to September, removed the duplicate Kirana Fleet and PayLoom rows, merged "FinTech" into "Fintech", parsed 18/09/2026, converted SGD and INR. Result: Logistics US$44.55M. But LedgerLeaf's US$250M seed looks like a data error and decides the answer: with it, Fintech leads at US$277.7M.

**Me:** Obviously we explain the situation and give both cases.

**Claude:** The partner asked for one sector and one number, so wrote `B/ANSWER.md` with Logistics US$44.6M as the headline and the LedgerLeaf case in the note (123 words).

**Me:** *(pasted a second AI's review of Section B)* 1. The comment says LedgerLeaf is ~80x the next seed (US$3M); the next is AgroSense at US$4.8M, so ~52x. 2. A comment mentions a "lead" column the CSV doesn't have. 3. State the break-even: above ~US$16.9M, Fintech wins. 4. Say the duplicates were judged by hand; FX also affects the Logistics lead.

**Claude:** Checked each by recomputing. 1-3 and the first half of 4 are right; fixed the comments, made the script print the break-even, added it to the note (133 words). The FX point doesn't hold: SGD would have to fall below ~0.37 for Healthtech to overtake, so left it out.

---

## Section A

**Me:** Pushed. Let's do A.

**Claude:** Drafted `A/prompt.md` (article in `<article>` tags treated as untrusted data; JSON only; no inventing; no own currency conversion; Series D+ → Series C+; only stated leads; verbatim evidence) and `A/my_test_input.md` (8 traps, each with the expected result).

**Me:** *(pasted a second AI's review of the prompt and test input)* 1. "$ with no other currency named" is ambiguous: snippet 3 mentions ₹, so CropIQ's $3M may come back null. 2. "You may map a city" is too weak. 3. Evidence rules need detail. 4. Pre-Series A → Unknown is my own call; note it. Test input: write the full expected JSON; add a bare-$ trap; consider a long article.

**Claude:** Agreed. Rewrote the currency rule per amount ("US$", "USD" and bare "$" count as USD; S$, A$, ₹ don't), "Map a named HQ city", evidence may join two quotes with " ... ". Added CoverLah (bare $5M from a Singapore company) and the full expected JSON. Left the long article as a known gap.

**Me:** I'm using Gemini and have added the key. What next?

**Claude:** Picked gemini-2.5-flash. Wrote `A/run_eval.py`: reads the prompt and test input straight from the .md files, runs each input 3 times with default temperature and no JSON mode (to test the prompt as graders will), saves every raw output, and checks each against the expected values.

**Me:** *(pasted the second AI's review of run_eval.py)* 1. A comment says sector is checked but the code doesn't. 2. Lead investors are compared in order. 3. A non-object JSON reply crashes the checker.

**Claude:** All three fixed, plus one more case (companies not a list). Tested the checker on hand-made outputs without calling the API: reversed leads pass, fenced and array replies are flagged without crashing, an injected answer is caught on every field.

**Me:** *(screenshot of the first run)* Done, have a look.

**Claude:** Content correct in 12/12 runs; injection ignored; CropIQ's bare $3M read as 3,000,000. But 9/12 replies are wrapped in a ```json code fence, so `json.loads` fails on them. GridCool's sector also drifts ("climate startup" vs "climate"). Plan: keep these as v1, tighten the prompt, rerun as v2.

**Me:** Should these go in a v1 folder, since there'll be a v2?

**Claude:** Moved them to `outputs_v1/` with the exact prompt used. Changed the runner: output folder is an argument, it refuses to overwrite, copies the prompt into each folder, and reports format and content separately. Re-scored v1: format 3/12, content 12/12.

**Me:** Change the prompt. *(screenshot about JSON-schema mode / tool calling / validate-and-retry)* Are these standard methods applicable?

**Claude:** They're right for production, but graders will run only the prompt text, not our API settings, so the prompt has to work alone. Worth mentioning in the notes. v2 changes: "Reply with raw JSON only: your reply must start with { and end with }. Do not wrap it in ``` code fences"; sector "one or two lowercase words ... not 'climate startup'".

**Me:** Change "(to fill in)" at the end of prompt.md to gemini-2.5-flash so prompt_used.md is complete.

**Claude:** Done.

**Me:** *(screenshot of the v2 run)*

**Claude:** Checked the outputs are real API replies. v2: content 12/12, format 10/12 (v1: 3/12), sector now consistent ("climate" every run).

---

## Write-up

**Me:** Write the Section A notes.

**Claude:** Counted what varied across the 3 runs (facts identical; only evidence wording varied). Wrote `A/NOTES.md`: where it still fails (format; long articles untested), consistency, and the five open calls. 149 words.

**Me:** *(pasted the second AI's suggestions)* 1. "Only evidence wording varied" isn't quite right: some v1 replies were single-line, others indented. 2. Say what my own test input targeted.

**Claude:** Verified point 1 (v1 snippet 3 runs 2 and 3 are indented). Applied both and trimmed elsewhere to stay at 149 words.

**Me:** Write the AI log.

**Claude:** Estimated times from commit timestamps and wrote `AI_LOG.md`, one entry per section, each under 80 words.

**Me:** Write the README.

**Claude:** Wrote `README.md`: index of answers, one-line summary per section, run instructions. Ran every command in it to confirm the outputs match what it says.

**Me:** *(pasted the second AI's review of the README)* 1. The chat_exports link is dead. 2. Running A without .env gives FileNotFoundError. 3. `&&` doesn't work in PowerShell 5.1. 4. Make the C summary plainer.

**Claude:** 1 is resolved by adding the exports. Made run_eval.py print a clear message when .env is missing (tested by renaming .env), split the `cd C` line, and reworded C as "more than 14 but under 15 days" (exactly 14 days is one of the open questions).
