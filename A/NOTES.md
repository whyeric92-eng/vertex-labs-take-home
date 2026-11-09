# Section A: Testing notes

Model: gemini-2.5-flash. Outputs and scores: `outputs_v1/`, `outputs_v2/`.

**Where it still fails.** Format. v1 wrapped the JSON in code fences in 9/12 runs; naming fences explicitly in v2 cut this to 2/12, but prompts can't guarantee it. In production I'd add JSON-schema mode and retries. Full-length articles untested. My own input (Series D, co-leads, bare $, background round) broke only the format.

**Consistency.** Content was correct in all 24 runs: injection ignored, ₹ not converted, "mid-eight figures" → null, participants not counted as leads. Across runs only evidence wording (always verbatim) and JSON layout varied. v1's sector drifted ("climate startup"); fixed in v2.

**Calls the requirements left open.**
- Bare "$" is USD (CoverLah could mean S$).
- "About US$30.8M" counts as a stated USD figure.
- Pre-Series A or unnamed rounds → Unknown.
- Sector null unless stated (AgroSense not inferred as agritech).
- HQ city mapped to country.
