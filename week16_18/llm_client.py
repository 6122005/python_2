"""Defensive wrapper around Groq (and fallback to Anthropic) Messages API.

Kept separate from core.py so the business logic (what a "fit analysis"
is) doesn't get tangled up with API plumbing (retries, timeouts).
"""
from __future__ import annotations

import os
import time
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-20b"


class LLMError(Exception):
    """Raised when the LLM call ultimately fails after retries."""


class LLMClient:
    def __init__(
        self,
        api_key: str = "",
        model: str | None = None,
        max_tokens: int = 1024,
        max_retries: int = 3,
        timeout: float = 30.0,
    ) -> None:
        groq_key = os.environ.get("GROQ_API_KEY")
        if not groq_key:
            try:
                import streamlit as st
                groq_key = st.secrets.get("GROQ_API_KEY", "")
            except Exception:
                pass
        if not groq_key and api_key and api_key.startswith("gsk_"):
            groq_key = api_key

        anthropic_key = api_key if (api_key and not api_key.startswith("gsk_")) else os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            try:
                import streamlit as st
                anthropic_key = st.secrets.get("ANTHROPIC_API_KEY", "")
            except Exception:
                pass

        if groq_key:
            from groq import Groq
            self.provider = "groq"
            self._client = Groq(api_key=groq_key, timeout=timeout)
            self.model = model or DEFAULT_MODEL
        elif anthropic_key:
            import anthropic
            self.provider = "anthropic"
            self._client = anthropic.Anthropic(api_key=anthropic_key, timeout=timeout)
            self.model = model or "claude-sonnet-4-5"
        else:
            raise LLMError("No API key configured. Please set GROQ_API_KEY or ANTHROPIC_API_KEY.")

        self.max_tokens = max_tokens
        self.max_retries = max_retries

    def complete(self, system: str, user_message: str) -> str:
        """Send one message, return the model's text."""
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                if self.provider == "groq":
                    resp = self._client.chat.completions.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": user_message},
                        ],
                    )
                    return resp.choices[0].message.content or ""
                else:
                    response = self._client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        system=system,
                        messages=[{"role": "user", "content": user_message}],
                    )
                    return "".join(block.text for block in response.content if block.type == "text")
            except Exception as exc:
                last_error = exc
                err_str = str(exc).lower()
                if "auth" in err_str or "key" in err_str:
                    raise LLMError("The API key is invalid or missing.") from exc
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)

        raise LLMError(f"The AI service is unavailable right now: {last_error}")
