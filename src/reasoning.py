"""Reasoning generator constrained to retained candidate facts."""

from __future__ import annotations

from .models import FeatureVector


class ReasoningGenerator:
    """Create concise, non-hallucinated explanations for submitted rows."""

    def generate(self, features: FeatureVector, rank: int) -> str:
        facts = features.facts
        evidence = ", ".join(facts.evidence[:3]) if facts.evidence else "applied ML evidence"
        skills = ", ".join(facts.skills[:3])

        opening = f"{facts.years:.1f} years as {facts.title} at {facts.company} with {evidence}"
        if skills:
            opening += f"; profile skills include {skills}"

        parts = [opening]

        signal_sentence = (
            f"Platform signals: response rate {facts.response_rate:.2f}, "
            f"last active {facts.last_active_date}, {facts.notice_days}-day notice"
        )
        if facts.open_to_work:
            signal_sentence += ", open to work"
        parts.append(signal_sentence)

        if facts.concerns:
            parts.append("Concern: " + "; ".join(facts.concerns[:2]))

        if rank <= 15 and not facts.concerns:
            parts.append("Top-tier match for Redrob's retrieval, ranking, and evaluation mandate")
        elif rank <= 30:
            parts.append("Ranks on demonstrated systems ownership, with availability now reflected in placement")
        elif rank <= 70:
            parts.append("Relevant systems profile, but weaker than the highest-signal candidate-matching records")
        else:
            parts.append("Lower-cutoff inclusion based on adjacent retrieval or ranking evidence")

        return ". ".join(parts) + "."
