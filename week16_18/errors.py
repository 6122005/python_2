"""Error handling — Wed D78: no unhandled exception should ever show a raw
Python traceback to a user.

The pattern used throughout app.py: every action that can fail (an LLM
call, a parsing step) is wrapped with `safe_run`, which converts *any*
exception into a friendly `AppError` with a message fit to show in the
UI, while still preserving the real exception for server-side logs.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable, TypeVar

from llm_client import LLMError

T = TypeVar("T")


@dataclass
class AppError(Exception):
    """A friendly, user-facing error. `detail` is safe to show in the UI;
    `original` (if present) is the real exception, for server-side logs
    only — never rendered to the user."""

    detail: str
    original: Exception | None = None


class InputTooLongError(AppError):
    pass


class EmptyInputError(AppError):
    pass


MAX_INPUT_CHARS = 4000


def validate_inputs(resume_text: str, job_description: str) -> None:
    """Raise a friendly AppError for the input problems users actually
    hit: empty fields and inputs that are too long for a reliable,
    affordable analysis. Called before every LLM call."""
    if not resume_text.strip():
        raise EmptyInputError("Please paste your resume text before analyzing.")
    if not job_description.strip():
        raise EmptyInputError("Please paste the job description before analyzing.")
    if len(resume_text) > MAX_INPUT_CHARS:
        raise InputTooLongError(
            f"Your resume is {len(resume_text):,} characters — please trim it to "
            f"under {MAX_INPUT_CHARS:,} so the analysis stays accurate and fast."
        )
    if len(job_description) > MAX_INPUT_CHARS:
        raise InputTooLongError(
            f"That job description is {len(job_description):,} characters — please "
            f"trim it to under {MAX_INPUT_CHARS:,} characters."
        )


def safe_run(fn: Callable[[], T]) -> T:
    """Run fn(), converting any exception into an AppError the UI can
    display safely. AppErrors raised deliberately (validation) pass
    through with their own message; anything else — network errors, a
    malformed JSON response from the model, a bug — is caught and
    reduced to one generic, friendly message so nothing internal leaks
    into the UI."""
    try:
        return fn()
    except AppError:
        raise
    except LLMError as exc:
        raise AppError(
            "The AI service didn't respond in time. Please try again in a moment.",
            original=exc,
        ) from exc
    except json.JSONDecodeError as exc:
        raise AppError(
            "The analysis came back in an unexpected format. Please try again.",
            original=exc,
        ) from exc
    except Exception as exc:  # last line of defense — Wed D78's core rule
        raise AppError(
            "Something went wrong on our end. Please try again, and if it keeps "
            "happening, let us know via the feedback link below.",
            original=exc,
        ) from exc
