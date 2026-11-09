# AI log

Main tool: Claude Code. A second Claude Code session reviewed each section's work before submission.

## A. Prompt and evaluate (~55 min)

I asked Claude Code to draft the prompt, my test input and a script that scores every run; I chose the traps and the open-question calls. The review caught that "$ with no other currency named" could null CropIQ's $3M, plus checker bugs (lead order, crash on non-objects). Claude Code tested the checker on hand-made outputs first. v1 wrapped JSON in fences 9/12; I tightened the prompt; v2: 2/12.

## B. Messy data (~15 min)

I asked Claude Code to write the cleaning script and partner note; I decided to exclude LedgerLeaf but report both outcomes. It called LedgerLeaf "80x the next seed" (actually 52x: it missed AgroSense's US$4.8M) and cited a "lead" column the CSV lacks. The review caught both and suggested the US$16.9M break-even. I recomputed, applied them, and rejected its FX point (SGD would need to fall below 0.37).

## C. Code review (~25 min)

I read fix.py first and found the timezone crash; Claude Code wrote probe.py, the extra tests and a draft review. The draft said "request changes" (not one of the brief's options), overstated one test's real-clock issue and ran over 200 words; the review caught these. probe.py reproduces each bug; the new tests fail 4 / pass 2 on the PR and pass 10/10 on a minimal fix Claude Code wrote to verify them (not submitted).
