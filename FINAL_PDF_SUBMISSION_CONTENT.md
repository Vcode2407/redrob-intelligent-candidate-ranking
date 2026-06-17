# Final PDF Submission Content

Use this content to populate the official Redrob idea submission template.

## Slide 1: Cover

Bullets:

- Team: Vkodes
- Problem Statement: Intelligent Candidate Discovery and Ranking Challenge
- Solution: CPU-only ranking pipeline for the Senior AI Engineer JD
- Output: Top 100 candidates with candidate-specific explanations

Presenter notes:

The submission ranks the 100,000-candidate pool for the Senior AI Engineer JD. The scoring uses career-history evidence for retrieval, search, ranking, evaluation, and deployment work, then adjusts close cases using Redrob platform signals.

## Slide 2: Solution Overview

Bullets:

- CPU-only deterministic Python pipeline.
- Streams 100K JSONL candidates without loading the full pool into memory.
- Scores career-history evidence before skill-list terms.
- Uses response rate, activity, notice period, and relocation as hireability modifiers.
- Writes validator-ready `submission.csv`.

Presenter notes:

The ranking command does not call external APIs or hosted models. It uses deterministic feature rules so the same input file produces the same candidate order.

## Slide 3: JD Understanding & Candidate Evaluation

Bullets:

- Must-have: production embeddings/retrieval, vector or hybrid search, Python, and ranking evaluation.
- Strong positives: recruiter-facing search, candidate-JD matching, NDCG/MRR/A-B testing, and product ownership.
- Behavioral positives: recent activity, response rate, interview completion, short notice, relocation feasibility.
- Explicit negatives: pure research, consulting-only profile, LangChain/OpenAI side projects only, CV/speech without IR.
- Risk handling: keyword stuffing, repeated templates, timeline inconsistencies, stale activity, and low response rates.

Presenter notes:

The scorer treats skills as supporting evidence. A profile needs matching work-history text before AI keywords can contribute much to the final rank.

## Slide 4: Ranking Methodology

Bullets:

- Raw score combines technical evidence, experience fit, career context, behavior, and risk.
- An availability gate reduces the score of candidates with weak hiring signals.
- Technical score rewards production ranking, retrieval, vector search, evaluation, and HR-tech relevance.
- Risk penalties demote long notice, non-relocation, over-band experience, repeated descriptions, and suspicious profiles.
- Final top-K uses a bounded heap and monotonic score normalization.

Presenter notes:

The official metric gives high weight to the first 10 and first 50 results. The scoring therefore keeps technical fit as the main signal and uses behavior/risk to order candidates that are otherwise close.

## Slide 5: Explainability & Validation

Bullets:

- Reasoning is assembled from retained profile facts.
- Explanations use years, title, company, evidence labels, skills, and Redrob signals.
- Concerns are surfaced when relevant: notice period, stale activity, location, experience-band mismatch.
- Optional debug JSON can be regenerated locally for component scores and risk flags.
- Official validator passes.

Presenter notes:

The reasoning generator uses only fields retained during scoring. It does not invent employers, skills, or behavioral signals.

## Slide 6: End-to-End Workflow

Bullets:

- Read challenge docs and encode JD requirements.
- Stream candidates from `candidates.jsonl`.
- Extract technical, career, behavioral, and risk features.
- Score each candidate and retain top profiles.
- Generate reasoning and write `submission.csv`.
- Run tests and official validator.

Presenter notes:

The submitted CSV is produced by `run.py`. Notebooks and debug outputs are not required for reproduction.

## Slide 7: System Architecture

Bullets:

- `data_loader.py`: streaming JSONL/GZ reader.
- `features.py`: evidence extraction and risk detection.
- `scoring.py`: scoring facade.
- `ranking.py`: bounded top-K ranking and score normalization.
- `reasoning.py`: profile-based explanations.
- `submission.py` and `validate.py`: output and local checks.

Presenter notes:

The architecture is small enough to inspect quickly. Most of the implementation detail is in feature extraction, risk detection, and CSV validation.

## Slide 8: Results & Performance

Bullets:

- Official validator result: passed.
- Full 100K ranking runtime: 73.32 seconds on CPU.
- Runtime limit: under 5 minutes.
- Output rows: 100.
- Ranks: unique 1-100.
- Scores: monotonic non-increasing.
- Top ranks contain AI/search/recommendation/NLP profiles with production evidence.

Presenter notes:

The final check focused on whether the top ranks still contained stale, very-low-response, long-notice, or non-relocating candidates.

## Slide 9: Technologies Used

Bullets:

- Python standard library.
- JSONL/GZ streaming.
- Deterministic feature scoring from profile fields.
- Bounded heap ranking.
- CSV output and validator mirror.
- Markdown documentation and Mermaid architecture diagram.

Presenter notes:

The stack uses the Python standard library and local files only during ranking, which keeps reproduction simple on CPU.

## Slide 10: Submission Assets

Bullets:

- `submission.csv`: final top-100 ranking.
- Optional local debug artifact: `outputs/ranking_debug_top100.json`, generated when `--debug-json` is used.
- `run.py`: one-command reproduction.
- `src/`: modular ranking implementation.
- `docs/`: architecture, scoring, analysis, and slide content.
- `FINAL_SUBMISSION_GUIDE.md` and `FINAL_SUBMISSION_CHECKLIST.md`.

Presenter notes:

The GitHub repository includes the code, documentation, metadata file, and final CSV. The sandbox URL can be filled separately if the portal requires it.
