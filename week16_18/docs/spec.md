# ResumeFit AI — Product Spec

Written before Day 1 of the build (Mon D76) so that Tue D77's rule —
*"add all secondary features from the spec, add nothing else"* — has
something concrete to point at. Treat this file as the single source of
truth for scope; if a feature isn't listed here, it doesn't go in the app
without updating this file first.

## What it is

A tool that compares a resume against a specific job description and
tells the candidate, in seconds, how well they match and what's missing
— then drafts a tailored cover letter if they want one.

## Who it's for

Job seekers (starting with the builder himself) applying to multiple
roles who want a fast, honest read on fit before spending 20 minutes
hand-tailoring a resume for a posting that might not even be a match.

## Core user flow (the "happy path" — Mon D76)

1. User pastes their resume text.
2. User pastes a job description.
3. User clicks **Analyze Fit**.
4. App shows: a fit score (0–100), a short list of matched skills, a
   short list of missing/weak skills, and a 2–3 sentence plain-English
   summary of the gap.

## Secondary features (Tue D77 — and *only* these)

- **Generate cover letter** — a button, shown only after a successful
  fit analysis, that drafts a short cover letter using the same resume
  + job description, in one of three tones (Professional / Friendly /
  Direct).
- **Copy-to-clipboard** for both the fit summary and the cover letter.
- **Input length guard** — resume and job description each capped at a
  sane length (4,000 characters) with a live character counter, so
  users get a clear warning instead of a silent truncation or an API
  error.

## Explicitly out of scope for this MVP

Anything not listed above — resume file upload/parsing (PDF/DOCX),
multi-resume comparison, saved history, account profiles beyond the
single shared password, email sending, ATS keyword density scoring,
LinkedIn import. These are good "v2" ideas; they are not this app.
Listing them here is deliberate, so "add nothing not in spec" has
teeth on Tue D77.

## Non-functional requirements (Wed–Fri, D78–D80)

- No unhandled exception should ever reach the user as a raw traceback.
- The app sits behind a single shared password (this is an internal/
  soft-launch tool, not a multi-tenant product — see `auth.py`).
- Every analysis and cover-letter generation is logged (timestamp +
  feature name + success/failure only — never resume or job-description
  content) to `data/usage_log.csv`.

## Success signal for the soft launch (Week 18)

At least 3 of the 5 soft-launch users complete a full analysis
unassisted and can correctly explain what the fit score means, without
being told.
