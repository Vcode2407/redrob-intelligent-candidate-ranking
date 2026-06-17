"""JD feature extraction.

The runtime ranker uses a frozen profile extracted from job_description.docx.
This avoids depending on DOCX parsing packages during the no-network ranking
step while still keeping the JD understanding explicit and reviewable.
"""

from __future__ import annotations

from .config import TIER1_LOCATION_HINTS
from .models import JobProfile


def default_job_profile() -> JobProfile:
    """Return the Redrob Senior AI Engineer profile from the released JD."""

    return JobProfile(
        title="Senior AI Engineer - Founding Team",
        min_years=5.0,
        max_years=9.0,
        must_have=(
            "production embeddings retrieval",
            "vector database or hybrid search",
            "strong python",
            "ranking evaluation metrics",
            "production code in last 18 months",
            "shipper product engineering attitude",
        ),
        nice_to_have=(
            "llm fine tuning",
            "learning to rank",
            "hr tech or marketplace exposure",
            "distributed systems",
            "open source ai ml validation",
        ),
        negative_patterns=(
            "pure research without production",
            "recent langchain/openai side projects only",
            "consulting only career",
            "title chasing job hops",
            "primary cv speech robotics without nlp ir",
            "keyword stuffed profile",
        ),
        preferred_locations=TIER1_LOCATION_HINTS,
    )

