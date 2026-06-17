"""Small utility functions kept dependency-free for reproduction."""

from __future__ import annotations

from datetime import date
from typing import Iterable


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def count_matches(text: str, terms: Iterable[str]) -> int:
    return sum(1 for term in terms if term in text)


def safe_date(value: object) -> date | None:
    if not isinstance(value, str) or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def candidate_numeric_id(candidate_id: str) -> int:
    try:
        return int(candidate_id.rsplit("_", 1)[1])
    except (IndexError, ValueError):
        return 10**9

