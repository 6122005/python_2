"""Usage logging — Fri D80.

Named `usage_logger.py` rather than the spec's suggested `logging.py`
deliberately: a top-level module literally named `logging.py` shadows
Python's own standard-library `logging` module for every other file in
this project that does `import logging` (Python resolves local files
before stdlib on `sys.path`). That's a subtle, nasty bug to debug later
for zero benefit now — same behavior, safer name.

Logs each event as one CSV row: timestamp + feature name + success flag
only. Per docs/spec.md, resume text and job-description text are never
written here — this file answers "how do people use the app," not "what
did they paste into it."
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_PATH = Path("data/usage_log.csv")
FIELDNAMES = ["timestamp_utc", "feature", "success"]


def log_event(feature: str, success: bool, path: Path | str = DEFAULT_LOG_PATH) -> None:
    """Append one usage event. Never raises — a logging failure should
    never break the user-facing feature it's logging (see the
    try/except below), consistent with Wed D78's "no unhandled
    exception reaches the user" rule."""
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        is_new_file = not path.exists()
        with path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if is_new_file:
                writer.writeheader()
            writer.writerow(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "feature": feature,
                    "success": success,
                }
            )
    except OSError:
        # Disk full, read-only filesystem (common on hosted platforms),
        # permissions issue — none of these should take the app down.
        pass


def read_events(path: Path | str = DEFAULT_LOG_PATH) -> list[dict]:
    """Read logged events back, e.g. for a small internal usage-stats view."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
