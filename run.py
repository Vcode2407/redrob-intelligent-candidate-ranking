"""Run the Redrob candidate ranking pipeline."""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from src.config import HEAP_KEEP_SIZE, TOP_K
from src.data_loader import find_default_candidates
from src.jd_features import default_job_profile
from src.ranking import RankingEngine
from src.scoring import ScoringEngine
from src.submission import write_debug, write_submission
from src.validate import validate_submission


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank Redrob candidates for the released JD")
    parser.add_argument("--candidates", type=Path, help="Path to candidates.jsonl or .jsonl.gz")
    parser.add_argument("--out", type=Path, default=Path("submission.csv"), help="Output CSV")
    parser.add_argument("--top-k", type=int, default=TOP_K, help="Number of candidates to submit")
    parser.add_argument(
        "--heap-keep-size",
        type=int,
        default=HEAP_KEEP_SIZE,
        help="Internal heap size. Keep above top-k for stable debug inspection.",
    )
    parser.add_argument("--debug-json", type=Path, help="Optional debug JSON path")
    parser.add_argument(
        "--official-validator",
        type=Path,
        help="Optional path to validate_submission.py from the challenge bundle",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    candidates = args.candidates or find_default_candidates(repo_root)
    if candidates is None:
        print(
            "Could not find candidates.jsonl. Pass --candidates /path/to/candidates.jsonl",
            file=sys.stderr,
        )
        return 2

    started = time.perf_counter()
    scoring_engine = ScoringEngine(default_job_profile())
    ranking_engine = RankingEngine(scoring_engine)
    ranked = ranking_engine.rank_file(candidates, args.top_k, args.heap_keep_size)
    write_submission(ranked, args.out)
    if args.debug_json:
        write_debug(ranked, args.debug_json)

    errors = validate_submission(args.out, expected_rows=args.top_k)
    if errors:
        print("Local validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.official_validator and args.official_validator.exists():
        result = subprocess.run(
            [sys.executable, str(args.official_validator), str(args.out)],
            check=False,
            text=True,
            capture_output=True,
        )
        print(result.stdout.strip())
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return result.returncode

    elapsed = time.perf_counter() - started
    print(f"Wrote {args.out} with {len(ranked)} rows in {elapsed:.2f}s")
    print(f"Top candidate: {ranked[0].candidate_id} score={ranked[0].score:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
