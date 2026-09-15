"""Basic auth — Thu D79.

A single shared password, checked against st.secrets, gating access to
the whole app via st.session_state. This is deliberately not a real
multi-user auth system (no accounts, no per-user permissions) — per
docs/spec.md, this is a soft-launch tool for a known handful of people,
and a shared password is the proportionate amount of protection for
that, not an under-engineered login system.
"""
from __future__ import annotations

import hmac

import streamlit as st


def _password_is_correct(entered: str) -> bool:
    expected = st.secrets.get("APP_PASSWORD", "")
    # hmac.compare_digest avoids leaking timing information about how
    # much of the password matched — cheap to do right, so do it right.
    return hmac.compare_digest(entered, expected)


def require_auth() -> None:
    """Call at the top of app.py. Renders a password gate and stops the
    script (st.stop()) until the correct password is entered; does
    nothing once the session is already authenticated."""
    if st.session_state.get("authenticated", False):
        return

    st.title("ResumeFit AI")
    st.caption("This app is currently invite-only.")
    password = st.text_input("Password", type="password")
    submitted = st.button("Enter")

    if submitted:
        if _password_is_correct(password):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("That password isn't right. Double-check and try again.")

    st.stop()
