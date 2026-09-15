# Setting Up the Feedback Form (Thu D89)

## Create the Google Form

1. Go to [forms.google.com](https://forms.google.com) → blank form.
2. Title: "ResumeFit AI Feedback."
3. Suggested questions (keep it short — a long form gets zero
   responses, which defeats the point):
   - "What were you trying to do?" (short answer)
   - "Did it work the way you expected?" (Yes / Mostly / No)
   - "What was confusing or annoying?" (paragraph, optional)
   - "Anything else?" (paragraph, optional)
4. Click **Send** → the link icon → copy the short URL.

## Wire it into the app

Paste that URL as `FEEDBACK_FORM_URL` in `.streamlit/secrets.toml`
(locally) and in Streamlit Cloud's secrets panel (in production — see
`docs/deployment_guide.md`). `app.py` already renders a **Give
Feedback** button that opens this link whenever the secret is set; no
code changes needed once the URL is in place.

## Measuring "did they use it"

Google Forms' own **Responses** tab (inside the form editor) shows a
live count and a summary view — no separate analytics needed for this
scale. Check it after each soft-launch conversation (Fri D90) and note
the count in `docs/feedback_log.md`; a big gap between "how many
people I told" and "how many responses" is itself a useful signal
about whether the in-app prompt is visible/compelling enough.
