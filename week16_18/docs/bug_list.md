# Bug List — Internal Testing (Wed D83)

> **How to fill this in:** run the app locally for a full hour on real
> resumes and real job postings (not lorem-ipsum test data — the point
> is to hit the edges a real user hits). Log every bug and annoyance
> here as you find it, then rank it P0/P1/P2 *before* Thu D84, so
> tomorrow starts with a sorted list instead of a triage session.
>
> **Priority key:**
> - **P0 — Critical.** Blocks the main use case (paste resume → paste
>   JD → get a fit score). Fix before doing anything else.
> - **P1 — Annoying but not blocking.** The user can still complete the
>   task, but it's rough. Fix if time allows this week.
> - **P2 — Cosmetic.** Doesn't affect functionality. Backlog it.

## Known candidates to specifically try to break

Seed the hour with these — they're the edge cases the code was written
to handle, so confirming they actually work (not just compile) is the
point of a real testing pass:

- [ ] Paste a resume with unusual characters (emoji, non-English text,
      copy-pasted table formatting from a PDF).
- [ ] Submit with one field empty.
- [ ] Paste a job description right at, and one character over, the
      4,000-character limit.
- [ ] Click "Analyze Fit" twice quickly in a row.
- [ ] Generate a cover letter, then re-run the fit analysis with
      different text — confirm the old cover letter doesn't linger.
- [ ] Kill your network mid-analysis and confirm you get a friendly
      error, not a spinner that hangs forever or a traceback.
- [ ] Refresh the page mid-session — does it re-prompt for the password
      correctly, or does it do something confusing?

## Bug log

| # | Priority | What happened | Steps to reproduce | Status |
|---|----------|----------------|----------------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
