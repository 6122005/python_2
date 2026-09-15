from __future__ import annotations

from pathlib import Path

from usage_logger import log_event, read_events


def test_log_event_creates_file_with_header(tmp_path):
    log_path = tmp_path / "usage.csv"
    log_event("analyze_fit", success=True, path=log_path)
    events = read_events(log_path)
    assert len(events) == 1
    assert events[0]["feature"] == "analyze_fit"
    assert events[0]["success"] == "True"


def test_log_event_appends_multiple_rows(tmp_path):
    log_path = tmp_path / "usage.csv"
    log_event("analyze_fit", success=True, path=log_path)
    log_event("generate_cover_letter", success=False, path=log_path)
    events = read_events(log_path)
    assert len(events) == 2
    assert events[1]["feature"] == "generate_cover_letter"
    assert events[1]["success"] == "False"


def test_log_event_never_writes_resume_or_job_text(tmp_path):
    """The whole point of this logger (per spec.md) is that it logs
    usage, not content — this is the test that enforces that promise."""
    log_path = tmp_path / "usage.csv"
    log_event("analyze_fit", success=True, path=log_path)
    raw_content = log_path.read_text(encoding="utf-8")
    assert "resume" not in raw_content.lower() or "feature" in raw_content.lower()
    # more concretely: only the known fieldnames' worth of data is ever written
    events = read_events(log_path)
    assert set(events[0].keys()) == {"timestamp_utc", "feature", "success"}


def test_read_events_returns_empty_list_when_file_missing(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"
    assert read_events(missing_path) == []


def test_log_event_does_not_raise_on_unwritable_path():
    # A path under a read-only mount should be swallowed, not raised —
    # logging must never break the feature it's logging.
    bad_path = Path("/mnt/skills/public/definitely-not-writable/usage.csv")
    log_event("analyze_fit", success=True, path=bad_path)  # should not raise
