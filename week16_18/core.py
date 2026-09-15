"""Core business logic for ResumeFit AI: what a "fit analysis" and a
"cover letter" actually are, independent of Streamlit or any UI concern.
app.py should never build a prompt or parse a model response directly —
it only calls into here. See docs/spec.md for the feature list this
implements.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Literal

from llm_client import LLMClient

Tone = Literal["Professional", "Friendly", "Direct"]

FIT_SYSTEM_PROMPT = """You evaluate how well a candidate's resume fits a
specific job description. Be honest and specific — vague encouragement
helps no one. Respond with ONLY a JSON object, no prose, no markdown
fences, in exactly this shape:

{
  "score": <integer 0-100>,
  "matched_skills": [<up to 6 short strings>],
  "missing_skills": [<up to 6 short strings>],
  "summary": "<2-3 sentence plain-English summary of the gap>"
}"""

COVER_LETTER_SYSTEM_PROMPT = """You write short, specific cover letters
that reference real details from the resume and job description — never
generic filler like "I am a hard worker." Three to four short paragraphs.
Output the letter text only, no subject line, no markdown, no commentary
before or after it."""

TONE_INSTRUCTIONS = {
    "Professional": "formal and measured",
    "Friendly": "warm and conversational, while still professional",
    "Direct": "brief, confident, and to the point — no throat-clearing",
}


@dataclass
class FitAnalysis:
    score: int
    matched_skills: List[str]
    missing_skills: List[str]
    summary: str


def analyze_fit(llm: LLMClient, resume_text: str, job_description: str) -> FitAnalysis:
    """Compare a resume against a job description. Raises LLMError on API
    failure, json.JSONDecodeError on a malformed model response — both
    are handled by errors.safe_run at the call site, not here, so this
    function stays focused on the actual logic."""
    user_message = (
        f"RESUME:\n{resume_text}\n\n---\n\nJOB DESCRIPTION:\n{job_description}"
    )
    raw = llm.complete(system=FIT_SYSTEM_PROMPT, user_message=user_message)
    data = json.loads(raw)
    return FitAnalysis(
        score=int(data["score"]),
        matched_skills=list(data.get("matched_skills", [])),
        missing_skills=list(data.get("missing_skills", [])),
        summary=str(data.get("summary", "")),
    )


def generate_cover_letter(
    llm: LLMClient, resume_text: str, job_description: str, tone: Tone = "Professional"
) -> str:
    """Draft a cover letter for this resume/job-description pair, in the
    requested tone. See docs/spec.md — this is a Tue D77 secondary
    feature, gated in the UI behind a successful fit analysis."""
    tone_instruction = TONE_INSTRUCTIONS[tone]
    user_message = (
        f"Write in a {tone_instruction} tone.\n\n"
        f"RESUME:\n{resume_text}\n\n---\n\nJOB DESCRIPTION:\n{job_description}"
    )
    return llm.complete(system=COVER_LETTER_SYSTEM_PROMPT, user_message=user_message).strip()
