"""Streaming candidate loader for JSONL and JSONL.GZ files."""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def iter_candidates(path: str | Path) -> Iterator[dict[str, Any]]:
    """Yield candidates one at a time without loading the full 487 MB file."""

    candidate_path = Path(path)
    opener = gzip.open if candidate_path.suffix == ".gz" else open
    with opener(candidate_path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"Line {line_number} is not a JSON object")
            yield obj


def find_default_candidates(repo_root: str | Path) -> Path | None:
    """Find the challenge candidates file in common local layouts."""

    root = Path(repo_root)
    candidates = [
        root / "data" / "candidates.jsonl",
        root / "data" / "candidates.jsonl.gz",
        root.parent
        / "[PUB] India_runs_data_and_ai_challenge"
        / "[PUB] India_runs_data_and_ai_challenge"
        / "India_runs_data_and_ai_challenge"
        / "candidates.jsonl",
        root.parent
        / "[PUB] India_runs_data_and_ai_challenge"
        / "[PUB] India_runs_data_and_ai_challenge"
        / "India_runs_data_and_ai_challenge"
        / "candidates.jsonl.gz",
    ]
    return next((path for path in candidates if path.exists()), None)

