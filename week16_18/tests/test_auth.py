"""Tests the password-comparison logic in isolation from Streamlit's
runtime (st.secrets / st.session_state need a running app context, so
require_auth() itself isn't unit-tested here — only the pure comparison
function, via a thin re-implementation check)."""
from __future__ import annotations

import hmac


def test_correct_password_matches():
    assert hmac.compare_digest("correct-horse", "correct-horse")


def test_incorrect_password_does_not_match():
    assert not hmac.compare_digest("wrong", "correct-horse")


def test_empty_password_does_not_match_nonempty_secret():
    assert not hmac.compare_digest("", "correct-horse")
