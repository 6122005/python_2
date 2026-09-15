"""ResumeFit AI — main Streamlit entry point.

This file only wires UI to core.py; it never builds prompts or parses
model output itself (that's core.py's job) and never swallows an
exception silently (errors.safe_run handles that). See docs/spec.md for
the feature list this implements.
"""
from __future__ import annotations

import streamlit as st

import ui_text as t
from auth import require_auth
from core import analyze_fit, generate_cover_letter
from errors import AppError, MAX_INPUT_CHARS, validate_inputs, safe_run
from llm_client import LLMClient
from usage_logger import log_event

st.set_page_config(page_title=t.PAGE_TITLE, page_icon=t.PAGE_ICON, layout="centered")

require_auth()  # Thu D79 — stops execution here until authenticated


@st.cache_resource
def get_llm_client() -> LLMClient:
    key = st.secrets.get("GROQ_API_KEY", st.secrets.get("ANTHROPIC_API_KEY", ""))
    return LLMClient(api_key=key)


def _char_counter(text: str) -> None:
    st.caption(t.CHAR_COUNTER_TEMPLATE.format(count=len(text), limit=MAX_INPUT_CHARS))


def render_header() -> None:
    st.title(t.HEADER)
    st.caption(t.SUBHEADER)


def render_inputs() -> tuple[str, str]:
    resume_text = st.text_area(
        t.RESUME_LABEL, placeholder=t.RESUME_PLACEHOLDER, height=220, key="resume_text"
    )
    _char_counter(resume_text)

    job_description = st.text_area(
        t.JOB_DESCRIPTION_LABEL,
        placeholder=t.JOB_DESCRIPTION_PLACEHOLDER,
        height=220,
        key="job_description",
    )
    _char_counter(job_description)

    return resume_text, job_description


def render_fit_results() -> None:
    result = st.session_state.get("fit_result")
    if result is None:
        return

    st.divider()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(t.SCORE_LABEL, f"{result.score}/100")
    with col2:
        st.write(f"**{t.SUMMARY_LABEL}**")
        st.write(result.summary)

    m_col, x_col = st.columns(2)
    with m_col:
        st.write(f"**{t.MATCHED_SKILLS_LABEL}**")
        for skill in result.matched_skills:
            st.markdown(f"- ✅ {skill}")
    with x_col:
        st.write(f"**{t.MISSING_SKILLS_LABEL}**")
        for skill in result.missing_skills:
            st.markdown(f"- ⚠️ {skill}")


def render_cover_letter_section(resume_text: str, job_description: str) -> None:
    if st.session_state.get("fit_result") is None:
        return  # secondary feature only unlocks after a successful analysis — per spec

    st.divider()
    st.subheader(t.COVER_LETTER_SECTION_TITLE)
    tone = st.selectbox(t.TONE_LABEL, ["Professional", "Friendly", "Direct"], key="tone")

    if st.button(t.GENERATE_LETTER_BUTTON):
        try:
            with st.spinner(t.GENERATING_LETTER_SPINNER):
                letter = safe_run(
                    lambda: generate_cover_letter(get_llm_client(), resume_text, job_description, tone)
                )
            st.session_state["cover_letter"] = letter
            log_event("generate_cover_letter", success=True)
        except AppError as e:
            log_event("generate_cover_letter", success=False)
            st.error(e.detail)

    letter = st.session_state.get("cover_letter")
    if letter:
        st.text_area(t.COVER_LETTER_LABEL, value=letter, height=260)
        st.caption(t.COPY_HINT)


def render_feedback_footer() -> None:
    st.divider()
    feedback_url = st.secrets.get("FEEDBACK_FORM_URL", "")
    if feedback_url:
        st.link_button(t.FEEDBACK_BUTTON, feedback_url)
        st.caption(t.FEEDBACK_CAPTION)
    st.caption(t.FOOTER)


def main() -> None:
    render_header()
    resume_text, job_description = render_inputs()

    if st.button(t.ANALYZE_BUTTON, type="primary"):
        try:
            safe_run(lambda: validate_inputs(resume_text, job_description))
            with st.spinner(t.ANALYZING_SPINNER):
                result = safe_run(lambda: analyze_fit(get_llm_client(), resume_text, job_description))
            st.session_state["fit_result"] = result
            st.session_state.pop("cover_letter", None)  # stale letter from a prior analysis
            log_event("analyze_fit", success=True)
        except AppError as e:
            log_event("analyze_fit", success=False)
            st.error(e.detail)

    render_fit_results()
    render_cover_letter_section(resume_text, job_description)
    render_feedback_footer()


if __name__ == "__main__":
    main()
