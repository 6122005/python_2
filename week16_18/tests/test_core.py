"""Offline tests — the LLM client is faked, so these run with no API key
and no network access. Run with: pytest tests/ -v
"""
from __future__ import annotations

import json

import pytest

from core import analyze_fit, generate_cover_letter
from errors import EmptyInputError, InputTooLongError, MAX_INPUT_CHARS, validate_inputs


class FakeLLMClient:
    """Stands in for llm_client.LLMClient — returns a canned response
    instead of calling the real API, so core.py's parsing logic can be
    tested in isolation."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.last_call = None

    def complete(self, system: str, user_message: str) -> str:
        self.last_call = {"system": system, "user_message": user_message}
        return self.response


FIT_JSON = json.dumps(
    {
        "score": 72,
        "matched_skills": ["Python", "REST APIs"],
        "missing_skills": ["Kubernetes"],
        "summary": "Strong backend overlap, but no container-orchestration experience shown.",
    }
)


def test_analyze_fit_parses_valid_response():
    llm = FakeLLMClient(FIT_JSON)
    result = analyze_fit(llm, "some resume", "some job description")
    assert result.score == 72
    assert "Python" in result.matched_skills
    assert "Kubernetes" in result.missing_skills
    assert "container" in result.summary


def test_analyze_fit_raises_on_malformed_json():
    llm = FakeLLMClient("this is not json")
    with pytest.raises(json.JSONDecodeError):
        analyze_fit(llm, "resume", "jd")


def test_analyze_fit_sends_both_documents_to_the_model():
    llm = FakeLLMClient(FIT_JSON)
    analyze_fit(llm, "RESUME_MARKER", "JD_MARKER")
    assert "RESUME_MARKER" in llm.last_call["user_message"]
    assert "JD_MARKER" in llm.last_call["user_message"]


def test_generate_cover_letter_returns_stripped_text():
    llm = FakeLLMClient("  Dear Hiring Manager,\n\nI'm excited...\n\n  ")
    letter = generate_cover_letter(llm, "resume", "jd", tone="Friendly")
    assert letter.startswith("Dear Hiring Manager")
    assert letter == letter.strip()


def test_generate_cover_letter_rejects_unknown_tone():
    llm = FakeLLMClient("text")
    with pytest.raises(KeyError):
        generate_cover_letter(llm, "resume", "jd", tone="Sarcastic")  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# Input validation (errors.py)
# --------------------------------------------------------------------------


def test_validate_inputs_accepts_normal_input():
    validate_inputs("a reasonable resume", "a reasonable job description")  # should not raise


def test_validate_inputs_rejects_empty_resume():
    with pytest.raises(EmptyInputError):
        validate_inputs("", "a job description")


def test_validate_inputs_rejects_whitespace_only_resume():
    with pytest.raises(EmptyInputError):
        validate_inputs("   \n  ", "a job description")


def test_validate_inputs_rejects_empty_job_description():
    with pytest.raises(EmptyInputError):
        validate_inputs("a resume", "")


def test_validate_inputs_rejects_oversized_resume():
    with pytest.raises(InputTooLongError):
        validate_inputs("x" * (MAX_INPUT_CHARS + 1), "a job description")


def test_validate_inputs_rejects_oversized_job_description():
    with pytest.raises(InputTooLongError):
        validate_inputs("a resume", "x" * (MAX_INPUT_CHARS + 1))
