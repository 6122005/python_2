"""User-facing copy — Tue D82.

Every string a user sees lives here, not scattered through app.py, for
two reasons: it's the one place to review tone/clarity in one pass (the
actual D82 task), and it means a future "make this friendlier" or
translation pass touches one file instead of hunting through UI code.
"""

PAGE_TITLE = "ResumeFit AI"
PAGE_ICON = "🎯"

HEADER = "ResumeFit AI"
SUBHEADER = "See how well your resume fits a job — before you spend an hour tailoring it."

RESUME_LABEL = "Your resume"
RESUME_PLACEHOLDER = "Paste your resume text here (no need to format it — plain text is fine)."

JOB_DESCRIPTION_LABEL = "Job description"
JOB_DESCRIPTION_PLACEHOLDER = "Paste the full job posting here."

ANALYZE_BUTTON = "Analyze Fit"
ANALYZING_SPINNER = "Comparing your resume against the job description…"

SCORE_LABEL = "Fit score"
MATCHED_SKILLS_LABEL = "What matches"
MISSING_SKILLS_LABEL = "What's missing or weak"
SUMMARY_LABEL = "In plain English"

COVER_LETTER_SECTION_TITLE = "Want a cover letter?"
TONE_LABEL = "Tone"
GENERATE_LETTER_BUTTON = "Generate Cover Letter"
GENERATING_LETTER_SPINNER = "Drafting your cover letter…"
COVER_LETTER_LABEL = "Your draft cover letter"

COPY_HINT = "Click inside the box, then Ctrl/Cmd+A, Ctrl/Cmd+C to copy."

CHAR_COUNTER_TEMPLATE = "{count:,} / {limit:,} characters"

FEEDBACK_BUTTON = "💬 Give Feedback"
FEEDBACK_CAPTION = "Found a bug or have a suggestion? Two minutes, really helps."

FOOTER = "Built by Jenish Bhesaniya"
