# Implementation Roadmap

## Completed

- Parsed challenge docs and official slide template.
- Extracted JD requirements, signal meanings, submission constraints, and honeypot warnings.
- Profiled the 100K candidate pool.
- Built a modular streaming ranker.
- Added risk detection for keyword stuffing, honeypots, services-only history, and behavior issues.
- Generated fact-grounded reasoning.
- Produced `submission.csv`.
- Passed official validation.

## Final Pre-Submission Checks

- Fill `submission_metadata.yaml` with team details, GitHub URL, and sandbox/demo link.
- Run:

```bash
python run.py --candidates path/to/candidates.jsonl --out submission.csv --official-validator path/to/validate_submission.py
```

- Review `outputs/ranking_debug_top100.json`.
- Confirm no manual edits were made to the generated CSV.
- Commit code with meaningful history before GitHub submission.

## Optional Improvements If Time Allows

- Add a small Streamlit or CLI upload demo for the required sandbox link.
- Add a top-100 audit notebook that prints compact candidate cards.
- Calibrate risk penalties after another manual review of ranks 1-25 and 90-100.
- Add a Dockerfile for exact Stage 3 reproducibility.

