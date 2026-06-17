"""Local submission validation mirroring the released challenge validator."""

from __future__ import annotations

import csv
import re
from pathlib import Path

REQUIRED_HEADER = ["candidate_id", "rank", "score", "reasoning"]
CID_RE = re.compile(r"^CAND_[0-9]{7}$")


def validate_submission(path: str | Path, expected_rows: int = 100) -> list[str]:
    csv_path = Path(path)
    errors: list[str] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return ["CSV is empty"]
        if header != REQUIRED_HEADER:
            errors.append(f"Header mismatch: {header!r}")
        data_rows = [row for row in reader if any(cell.strip() for cell in row)]

    if len(data_rows) != expected_rows:
        errors.append(f"Expected {expected_rows} rows, found {len(data_rows)}")

    seen_ids: set[str] = set()
    seen_ranks: set[int] = set()
    by_rank: list[tuple[int, float, str]] = []
    for row_num, row in enumerate(data_rows, start=2):
        if len(row) != 4:
            errors.append(f"Row {row_num}: expected 4 columns, found {len(row)}")
            continue
        candidate_id, rank_s, score_s, _ = row
        if not CID_RE.match(candidate_id):
            errors.append(f"Row {row_num}: invalid candidate_id {candidate_id!r}")
        if candidate_id in seen_ids:
            errors.append(f"Row {row_num}: duplicate candidate_id {candidate_id}")
        seen_ids.add(candidate_id)
        try:
            rank = int(rank_s)
            score = float(score_s)
        except ValueError:
            errors.append(f"Row {row_num}: rank/score parse error")
            continue
        if rank < 1 or rank > expected_rows:
            errors.append(f"Row {row_num}: rank {rank} out of range")
        if rank in seen_ranks:
            errors.append(f"Row {row_num}: duplicate rank {rank}")
        seen_ranks.add(rank)
        by_rank.append((rank, score, candidate_id))

    missing = set(range(1, expected_rows + 1)) - seen_ranks
    if missing:
        errors.append(f"Missing ranks: {sorted(missing)}")

    by_rank.sort()
    for prev, cur in zip(by_rank, by_rank[1:]):
        prev_rank, prev_score, prev_id = prev
        cur_rank, cur_score, cur_id = cur
        if prev_score < cur_score:
            errors.append(
                f"Score increases from rank {prev_rank} to {cur_rank}: "
                f"{prev_score} < {cur_score}"
            )
        if prev_score == cur_score and prev_id > cur_id:
            errors.append(f"Tie at ranks {prev_rank}/{cur_rank} violates ID order")
    return errors

