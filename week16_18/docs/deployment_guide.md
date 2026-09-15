# Deploying to Streamlit Cloud (Wed D88)

## Steps

1. Push this repo to GitHub (public or private — Streamlit Cloud's free
   tier supports both if the repo is linked to your account).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select the repo, branch (`main`), and set **Main file path** to
   `app.py`.
4. Before clicking Deploy, open **Advanced settings → Secrets** and
   paste in the contents of your local `.streamlit/secrets.toml`
   (same three keys: `ANTHROPIC_API_KEY`, `APP_PASSWORD`,
   `FEEDBACK_FORM_URL`). Streamlit Cloud secrets are separate from
   your repo — nothing in `.streamlit/secrets.toml.example` gets
   deployed, since the real file is gitignored.
5. Deploy. First build takes a few minutes while it installs
   `requirements.txt`.

## Test every feature on the live URL — don't assume local behavior carries over

Specifically check, in this order:

- [ ] The password gate appears and the correct password gets you in.
- [ ] **Fit analysis works** — this exercises that `ANTHROPIC_API_KEY`
      was pasted correctly into Cloud secrets (a copy-paste error here
      is the single most common first-deploy bug).
- [ ] Cover letter generation works for all three tones.
- [ ] The theme (`.streamlit/config.toml`) actually applied — Cloud
      reads this file automatically, but confirm the colors show up.
- [ ] The "Give Feedback" button opens the real Google Form, not the
      placeholder URL.
- [ ] Submitting an oversized or empty input shows the friendly error
      message, not a crash.
- [ ] `data/usage_log.csv` is being written — check the app's logs in
      Streamlit Cloud's manage panel, or temporarily add a debug view
      (see note below).

## A gotcha specific to this app: `data/usage_log.csv` on Streamlit Cloud

Streamlit Cloud's filesystem is **ephemeral** — it resets on every
redeploy and isn't shared across instances if the app scales. For a
soft launch with a handful of users this is a fine tradeoff (the goal
per `docs/spec.md` is directional usage signal, not a permanent
record), but don't be surprised if `usage_log.csv` empties out after a
redeploy. If usage logging needs to survive redeploys later, swap
`usage_logger.py`'s destination for a hosted store (a Google Sheet via
its API, or a small hosted database) — the `log_event()` /
`read_events()` interface was kept narrow specifically so that swap
doesn't touch `app.py`.

## Live link

Once deployed, put the real URL here and also into `README.md`:

```
Live app: <paste URL here>
```
