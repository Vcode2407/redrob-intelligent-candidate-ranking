"""CSV submission writer."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import RankedCandidate


def write_submission(rows: list[RankedCandidate], out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for row in rows:
            writer.writerow(
                [row.candidate_id, row.rank, f"{row.score:.4f}", row.reasoning]
            )


def write_debug(rows: list[RankedCandidate], out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = []
    for row in rows:
        features = row.features
        payload.append(
            {
                "candidate_id": row.candidate_id,
                "rank": row.rank,
                "score": row.score,
                "raw_score": row.raw_score,
                "technical_score": features.technical_score,
                "technical_history_score": features.technical_history_score,
                "skill_score": features.skill_score,
                "experience_score": features.experience_score,
                "career_score": features.career_score,
                "behavior_score": features.behavior_score,
                "risk_penalty": features.risk_penalty,
                "facts": {
                    "title": features.facts.title,
                    "company": features.facts.company,
                    "years": features.facts.years,
                    "location": features.facts.location,
                    "evidence": features.facts.evidence,
                    "skills": features.facts.skills,
                    "concerns": features.facts.concerns,
                    "risk_flags": features.facts.risk_flags,
                },
            }
        )
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

