# Redrob Intelligent Candidate Ranking

Submission package for the Redrob AI **Intelligent Candidate Discovery & Ranking Challenge**.

This repository contains a deterministic, CPU-only ranker for 100,000 candidate profiles. It produces a validator-ready `submission.csv` with the top 100 candidates for Redrob's Senior AI Engineer hiring scenario, along with fact-grounded reasoning and debug artifacts.

## Challenge Summary

The challenge asks participants to rank candidates while avoiding common traps:

- keyword-stuffed AI profiles with weak career evidence.
- honeypot candidates and synthetic inconsistencies.
- misleading profile-quality signals.
- candidates who are strong technically but difficult to hire because of availability, location, or notice-period constraints.

The solution is designed to read profiles like a hiring manager: production evidence first, keywords second.

## Solution Overview

The ranker prioritizes:

- production embeddings, retrieval, vector search, hybrid search, and ranking systems.
- Python and ML systems implementation experience.
- evaluation experience such as NDCG, MRR, A/B testing, and search relevance metrics.
- coherent career progression and product/company ownership.
- behavioral availability signals such as response rate, recent activity, notice period, and relocation feasibility.

It explicitly downranks:

- pure keyword matchers without role-history evidence.
- consulting-only or side-project-only profiles.
- pure research profiles without production IR/ranking relevance.
- stale, low-response, hard-to-hire candidates.
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
    reasoning.py        # Fact-grounded reasoning generator
    scoring.py          # Scoring facade
    submission.py       # CSV and debug writers
    validate.py         # Local validator mirror
  tests/
  run.py
  requirements.txt
  submission.csv
```

Core flow:

```text
candidates.jsonl -> data loader -> feature extractor -> scoring engine
-> top-K ranking -> reasoning generator -> submission.csv + debug JSON
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
- `outputs/ranking_debug_top100.json`

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
- Final audited full run completed in 73.32 seconds on the local CPU environment.

## Scoring Summary

Raw score:

```text
3.25 * Technical + 1.50 * Experience + 1.30 * Career
+ 1.10 * Behavior - 1.75 * Risk
```

Technical evidence is mostly career-history based; skill-list terms act as corroboration. Behavioral signals adjust for recruiter reachability and hiring feasibility. Risk penalties are designed to keep honeypots, repeated templates, long-notice profiles, and keyword stuffers out of top ranks.

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
