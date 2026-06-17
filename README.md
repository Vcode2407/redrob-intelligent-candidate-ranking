# Redrob Intelligent Candidate Ranking

Submission package for the Redrob AI **Intelligent Candidate Discovery and Ranking Challenge**.

This repository contains a deterministic, CPU-only Python pipeline for ranking 100,000 candidate profiles. It reads the challenge JSONL file, scores candidates against the Senior AI Engineer job description, keeps the top 100, and writes the final `submission.csv`.

## Challenge Summary

The challenge data includes profiles that can look relevant for the wrong reasons:

- long AI skill lists without matching work history.
- synthetic or inconsistent profile fields.
- high-level summaries that hide weak production experience.
- technically relevant candidates who are hard to reach or hire because of activity, response rate, location, or notice period.

The implementation gives more trust to career-history evidence than to free-text summaries or skill lists.

## Solution Overview

The scoring code gives positive weight to:

- production embeddings, retrieval, vector search, hybrid search, and ranking systems.
- Python and ML systems implementation experience.
- evaluation experience such as NDCG, MRR, A/B testing, and search relevance metrics.
- coherent career progression and product/company ownership.
- behavioral availability signals such as response rate, recent activity, notice period, and relocation feasibility.

It applies penalties for:

- skill lists without role-history evidence.
- consulting-only or side-project-only profiles.
- pure research profiles without production IR/ranking relevance.
- stale, low-response, or long-notice candidates.
- repeated-template, synthetic, or internally inconsistent profiles.

## Architecture

```text
redrob_ranker/
  data/                 # Place local candidates.jsonl here; raw data is not committed
  docs/                 # Analysis, scoring, architecture, PPT/PDF content
  outputs/              # Generated locally; not committed
  src/
    data_loader.py      # Streaming JSONL/GZ loader
    features.py         # Feature extraction and risk detection
    jd_features.py      # Frozen JD requirement profile
    ranking.py          # Bounded top-K ranking engine
    reasoning.py        # Profile-based reasoning generator
    scoring.py          # Scoring facade
    submission.py       # CSV writer and optional debug writer
    validate.py         # Local validator mirror
  tests/
  run.py
  requirements.txt
  submission.csv
```

Core flow:

```text
candidates.jsonl -> data loader -> feature extractor -> scoring engine
-> top-K ranking -> reasoning generator -> submission.csv
```

## Setup

Use Python 3.11+.

```bash
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduce Results

Place the challenge candidate file at `data/candidates.jsonl`, or pass the path explicitly.

```bash
python run.py --candidates data/candidates.jsonl --out submission.csv
```

Full reproduction with debug output and the official validator:

```bash
python run.py \
  --candidates data/candidates.jsonl \
  --out submission.csv \
  --debug-json outputs/ranking_debug_top100.json \
  --official-validator path/to/validate_submission.py
```

Expected local output:

- `submission.csv`
- `outputs/submission.csv`
- optional `outputs/ranking_debug_top100.json` when `--debug-json` is supplied

## Validation

Run unit tests:

```bash
python -m unittest discover -s tests
```

Run the official validator:

```bash
python path/to/validate_submission.py submission.csv
```

The final local validation result was:

```text
Submission is valid.
```

The final `submission.csv` contains:

- 100 candidates.
- unique candidate IDs.
- ranks 1 through 100.
- monotonically decreasing scores.
- candidate-specific reasoning grounded in extracted profile facts.

## Runtime and Constraints

- CPU only.
- No external API calls during ranking.
- Streaming JSONL loading for the 100,000-candidate pool.
- Memory target under 16 GB.
- Runtime target under 5 minutes.
- Final local full run completed in 73.32 seconds on the listed CPU environment.

## Scoring Summary

The implementation combines technical evidence, experience fit, career context, behavior, and risk. The raw score in `src/features.py` is:

```text
(2.85 * Technical + 1.35 * Experience + 1.15 * Career)
* (0.72 + 0.28 * Behavior)
+ 1.45 * Behavior
- 2.60 * Risk
```

Technical evidence is mostly career-history based; skill-list terms act as supporting evidence. Behavioral signals adjust close cases for recruiter reachability and hiring feasibility. Risk penalties cover keyword stuffing, repeated descriptions, long notice periods, location/relocation issues, and inconsistent profiles.

See [docs/scoring_methodology.md](docs/scoring_methodology.md) for the full rubric.

## Documentation

- [docs/analysis_report.md](docs/analysis_report.md): JD and signal analysis.
- [docs/scoring_methodology.md](docs/scoring_methodology.md): scoring rubric and rationale.
- [docs/architecture.md](docs/architecture.md): system architecture.
- [docs/ppt_content.md](docs/ppt_content.md): slide content for the official submission template.
- [FINAL_PDF_SUBMISSION_CONTENT.md](FINAL_PDF_SUBMISSION_CONTENT.md): final evaluator-facing slide content.
- [FINAL_SUBMISSION_GUIDE.md](FINAL_SUBMISSION_GUIDE.md): portal submission steps.

## Repository Hygiene

The raw challenge candidate pool is intentionally not committed. The final root-level submission file is included:

- `submission.csv`

Generated caches, virtual environments, local secrets, large temporary files, notebooks, and output/debug artifacts are excluded by `.gitignore`.
