"""Typed domain models for the Redrob ranker."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class JobProfile:
    """Compact representation of the JD requirements used by the ranker."""

    title: str
    min_years: float
    max_years: float
    must_have: tuple[str, ...]
    nice_to_have: tuple[str, ...]
    negative_patterns: tuple[str, ...]
    preferred_locations: tuple[str, ...]


@dataclass(slots=True)
class CandidateFacts:
    """Facts retained for ranking explanations and debug output."""

    candidate_id: str
    years: float
    title: str
    company: str
    location: str
    country: str
    response_rate: float
    notice_days: int
    last_active_date: str
    github_activity_score: float
    open_to_work: bool
    evidence: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FeatureVector:
    """Numerical features and final raw score for one candidate."""

    candidate_id: str
    raw_score: float
    technical_score: float
    technical_history_score: float
    skill_score: float
    experience_score: float
    career_score: float
    behavior_score: float
    risk_penalty: float
    facts: CandidateFacts


@dataclass(slots=True)
class RankedCandidate:
    """Final submission row enriched with raw features."""

    candidate_id: str
    rank: int
    score: float
    reasoning: str
    raw_score: float
    features: FeatureVector

