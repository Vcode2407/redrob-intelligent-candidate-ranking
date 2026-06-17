# PPT Content For Official Template

## 1. Cover

Title: Redrob Intelligent Candidate Discovery Ranker

Bullets:

- Team: `<your team name>`
- Problem Statement: Rank top 100 candidates for Redrob Senior AI Engineer role
- Objective: Maximize top-rank relevance while avoiding keyword-stuffers and honeypots

Diagram suggestion:

- Clean cover with Redrob challenge title and a simple "JD -> Ranked Candidates" flow.

Speaker notes:

We built a production-style ranker for the Redrob Senior AI Engineer JD. The focus is ranking quality, reproducibility, and trap resistance under the CPU/no-network constraints.

## 2. Solution Overview

Title: Evidence-Weighted Candidate Ranking

Bullets:

- Streams 100K profiles and ranks top 100 in under 5 minutes on CPU.
- Rewards production retrieval, ranking, vector search, evaluation, and product ownership.
- Treats skill keywords as weak evidence unless backed by career history.
- Applies behavioral availability and explicit risk detection.
- Generates fact-grounded reasoning for every submitted candidate.

Diagram suggestion:

- Four blocks: Technical Evidence, Career Quality, Behavioral Readiness, Risk Controls -> Final Rank.

Speaker notes:

Traditional matchers over-index on skill fields. This solution reads the profile like a hiring manager: what did the candidate actually build, where, at what scale, and are they reachable?

## 3. JD Understanding & Candidate Evaluation

Title: What The JD Really Asks For

Bullets:

- Must-have: production embeddings retrieval, vector/hybrid search, Python, ranking evaluation.
- Ideal profile: 6-8 years, applied ML/product-company history, search/recommendation ownership.
- Culture fit: shipper mindset, product collaboration, writes code recently.
- Negative signals: pure research, services-only career, LangChain side projects only, CV/speech without IR.
- Behavioral fit: active, responsive, reachable, feasible notice/location.

Diagram suggestion:

- JD signal pyramid: Must-have systems evidence at base, career quality, behavior, then nice-to-haves.

Speaker notes:

The JD says not to rank by AI keyword count. The hidden target is demonstrated ownership of candidate matching, ranking, retrieval, and evaluation systems.

## 4. Ranking Methodology

Title: Scoring Model

Bullets:

- RawScore = Technical + Experience + Career + Behavior - Risk.
- Technical evidence is mostly career-history based.
- Skills are weighted by proficiency, duration, endorsements, and assessment scores.
- Behavior modifies technically similar candidates.
- Hard risk penalties remove honeypot-like profiles.

Diagram suggestion:

- Weighted equation with the five components and approximate weights.

Speaker notes:

The largest coefficient is technical match, but not simple keyword overlap. A profile must show shipped systems, evaluation, and production ownership.

## 5. Explainability & Validation

Title: Fact-Grounded Reasoning

Bullets:

- Reasoning uses only retained candidate facts.
- Mentions years, title/company, actual evidence labels, skills, and Redrob signals.
- Concerns are included when obvious: long notice, low response, stale activity, location.
- Validator checks format, ranks, uniqueness, score monotonicity.
- Debug JSON supports audit of score components and risk flags.

Diagram suggestion:

- Candidate profile -> extracted facts -> reason sentence -> CSV row.

Speaker notes:

The reasoning column is not generated from a model. It is assembled from scoring facts so it cannot invent employers, skills, or behavior signals.

## 6. End-to-End Workflow

Title: From JD To Submission CSV

Bullets:

- Read JD and signal docs, freeze explicit requirements.
- Stream candidates from JSONL/GZ.
- Extract evidence, behavior, and risk features.
- Score and retain top candidates in a bounded heap.
- Normalize scores, generate reasoning, write CSV.
- Run local and official validators.

Diagram suggestion:

- Horizontal workflow: Docs -> Feature Rules -> Stream Scoring -> Top-K -> Reasoning -> CSV -> Validator.

Speaker notes:

The ranking path is a single command and does not depend on notebooks, APIs, or manual edits.

## 7. System Architecture

Title: Streaming CPU-Only Architecture

Bullets:

- Standard-library Python implementation.
- Bounded top-K heap avoids storing 100K full records.
- Modular source: loader, JD profile, extractor, scorer, ranker, reasoning, validator.
- No network calls or hosted LLM APIs.
- Designed for reproducible Stage 3 sandbox evaluation.

Diagram suggestion:

- Use the architecture diagram from `docs/architecture.md`.

Speaker notes:

The system is deliberately simple operationally. The sophistication is in signal design and risk handling, not infrastructure complexity.

## 8. Results & Performance

Title: Submission Quality Checks

Bullets:

- Official validator: pass.
- Full 100K local run: about 42 seconds after cache warmup.
- Top 100 titles concentrated in search, recommendation, ML, NLP, and senior applied roles.
- Top candidates show production retrieval/ranking evidence and active Redrob signals.
- Honeypot flags absent from final top 100.

Diagram suggestion:

- Small table: runtime, rows processed, validator status, top title distribution, risk-flag summary.

Speaker notes:

The top 10 are dominated by production ranker/search profiles, not broad AI skill lists. Behavior moves weakly reachable candidates below similarly strong reachable candidates.

## 9. Technologies Used

Title: Lean, Reproducible Stack

Bullets:

- Python standard library only.
- JSONL/GZ streaming.
- Deterministic feature scoring.
- Bounded heap ranking.
- CSV writer and local validator.
- Markdown docs and Mermaid architecture diagram.

Diagram suggestion:

- Stack diagram with "Python stdlib" as the foundation and modules above it.

Speaker notes:

Avoiding external packages and APIs reduces reproducibility risk and fits the challenge's real-world latency and cost constraints.

## 10. Submission Assets

Title: Delivered Assets

Bullets:

- `submission.csv`: final top-100 ranking.
- `run.py`: one-command reproduction.
- `src/`: modular production-quality ranker.
- `docs/`: analysis, scoring methodology, architecture, PPT content, winning strategy.
- `outputs/ranking_debug_top100.json`: score and reasoning audit artifact.
- `tests/`: unit tests for core behavior.

Diagram suggestion:

- Repository tree visual.

Speaker notes:

The repo is ready for GitHub submission. The generated CSV is reproducible from the challenge candidates file and passes validation.

