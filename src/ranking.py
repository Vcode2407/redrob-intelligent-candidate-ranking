"""Top-K ranking engine."""

from __future__ import annotations

import heapq
from pathlib import Path

from .config import HEAP_KEEP_SIZE, TOP_K
from .data_loader import iter_candidates
from .models import FeatureVector, RankedCandidate
from .reasoning import ReasoningGenerator
from .scoring import ScoringEngine
from .utils import candidate_numeric_id


class RankingEngine:
    """Stream candidates and retain the best scoring profiles."""

    def __init__(
        self,
        scoring_engine: ScoringEngine,
        reasoning_generator: ReasoningGenerator | None = None,
    ) -> None:
        self.scoring_engine = scoring_engine
        self.reasoning_generator = reasoning_generator or ReasoningGenerator()

    def rank_file(
        self,
        candidates_path: str | Path,
        top_k: int = TOP_K,
        heap_keep_size: int = HEAP_KEEP_SIZE,
    ) -> list[RankedCandidate]:
        keep_size = max(top_k, heap_keep_size)
        heap: list[tuple[float, int, FeatureVector]] = []

        for candidate in iter_candidates(candidates_path):
            features = self.scoring_engine.score(candidate)
            heap_key = (features.raw_score, -candidate_numeric_id(features.candidate_id), features)
            if len(heap) < keep_size:
                heapq.heappush(heap, heap_key)
            else:
                if heap_key > heap[0]:
                    heapq.heapreplace(heap, heap_key)

        ordered = sorted(
            (item[2] for item in heap),
            key=lambda fv: (-fv.raw_score, candidate_numeric_id(fv.candidate_id)),
        )[:top_k]
        scores = self._normalize_scores([item.raw_score for item in ordered])

        ranked: list[RankedCandidate] = []
        for rank, (features, score) in enumerate(zip(ordered, scores), start=1):
            ranked.append(
                RankedCandidate(
                    candidate_id=features.candidate_id,
                    rank=rank,
                    score=score,
                    reasoning=self.reasoning_generator.generate(features, rank),
                    raw_score=features.raw_score,
                    features=features,
                )
            )
        return ranked

    @staticmethod
    def _normalize_scores(raw_scores: list[float]) -> list[float]:
        if not raw_scores:
            return []
        high = max(raw_scores)
        low = min(raw_scores)
        if high == low:
            return [round(0.9990 - index * 0.0001, 4) for index, _ in enumerate(raw_scores)]
        normalized = []
        previous: float | None = None
        for raw in raw_scores:
            score = 0.2000 + 0.7990 * ((raw - low) / (high - low))
            score = round(score, 4)
            if previous is not None and score >= previous:
                score = round(previous - 0.0001, 4)
            normalized.append(score)
            previous = score
        return normalized
