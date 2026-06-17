"""Scoring engine facade."""

from __future__ import annotations

from typing import Any

from .features import CandidateFeatureExtractor
from .models import FeatureVector, JobProfile


class ScoringEngine:
    """Score candidates against a frozen JD profile."""

    def __init__(self, job_profile: JobProfile) -> None:
        self.job_profile = job_profile
        self.extractor = CandidateFeatureExtractor()

    def score(self, candidate: dict[str, Any]) -> FeatureVector:
        return self.extractor.extract(candidate)

