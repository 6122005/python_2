# ResumeFit AI

See how well your resume fits a job — before you spend an hour
tailoring it by hand.

<!--
  Screenshot goes here once the app has run at least once locally or
  is deployed — take one of the main input screen with a sample
  result showing (fit score + matched/missing skills), save it to
  docs/screenshot.png, and replace this comment with:
  ![ResumeFit AI screenshot](docs/screenshot.png)
-->

**Live app:** _add the Streamlit Cloud URL here after Wed D88 —
see `docs/deployment_guide.md`_

## What it does

Paste your resume and a job description. In a few seconds you get:

- A **fit score** (0–100)
- What in your background **matches** the role
- What's **missing or weak**
- A plain-English summary of the gap

If the fit looks reasonable, generate a **tailored cover letter** in
one of three tones (Professional / Friendly / Direct) — one click,
using the same resume and job description you already pasted in.

## Who it's for

Anyone applying to multiple roles who wants an honest, fast read on
fit before hand-tailoring a resume for a posting that might not even
be a match. Built by a job seeker, for job seekers — see
`docs/spec.md` for the full scope and what's deliberately *not*
included in this version.

## How to use it

1. Open the live app (link above) or run it locally (see below).
2. Enter the shared password (ask the person who sent you the link).
3. Paste your resume text and the job description.
4. Click **Analyze Fit**.
5. Optionally, click **Generate Cover Letter** once you've seen the
   fit results.
6. Something confusing or broken? Use the **Give Feedback** button at
   the bottom of the app — it takes two minutes and directly shapes
   what gets fixed next.

## Running it locally

```bash
git clone <this repo>
cd resumefit-mvp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml with a real ANTHROPIC_API_KEY,
# a password of your choice, and (optionally) a feedback form URL

streamlit run app.py
```

## Project structure

```
resumefit-mvp/
├── app.py              Streamlit UI — wires everything together
├── core.py              Fit analysis + cover letter generation logic
├── llm_client.py         Retry-safe Anthropic API wrapper
├── auth.py               Simple shared-password gate
├── errors.py              Input validation + "never show a raw traceback" handling
├── usage_logger.py         Appends usage events to data/usage_log.csv
├── ui_text.py               All user-facing copy, in one place
├── .streamlit/config.toml     Theme
├── docs/                       Spec, testing notes, deployment + feedback guides
└── tests/                       Offline unit tests (pytest, no API key needed)
```

## Development notes

- **Everything the model produces or receives is handled defensively.**
  `errors.py`'s `safe_run` wrapper means no unhandled exception — API
  timeout, malformed JSON, anything — ever reaches the user as a raw
  traceback; see `docs/bug_list.md` for the testing pass that verified
  this.
- **Usage logging never stores what users paste in** — only a
  timestamp and which feature was used (`usage_logger.py`; see
  `docs/spec.md`'s non-functional requirements).
- Run `pytest tests/ -v` before pushing — 19 offline tests cover the
  parsing, validation, and logging logic without needing a live API
  key.

## Built by

Jenish Bhesaniya — [GitHub](https://github.com/6122005)
