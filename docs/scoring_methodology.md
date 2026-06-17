# Scoring Methodology

## Objective

Rank the top 100 candidates for a Senior AI Engineer role at Redrob, optimizing for hidden relevance metrics that heavily reward the top 10 and top 50 while filtering honeypots.

## Formula

```text
RawScore =
  (2.85 * Technical + 1.35 * Experience + 1.15 * Career)
  * (0.72 + 0.28 * Behavior)
+ 1.45 * Behavior
- 2.60 * Risk
```

The emitted CSV score is a monotonic normalization of `RawScore` for the final top 100.

## A. Technical Match

Technical is the most important category. Career-history evidence dominates; skills are only corroboration.

History subscore rewards:

- ranking, search relevance, recommendations, learning-to-rank.
- embeddings, vector search, hybrid retrieval, BM25+dense retrieval, FAISS/Pinecone/Qdrant/Milvus/OpenSearch.
- evaluation: NDCG, MRR, A/B testing, human relevance judgments, offline-online correlation.
- production operations: scale, users, queries, latency, monitoring, rollback, index refresh, drift.
- HR-tech context: candidate-JD matching, recruiter-facing search, candidate corpus search.

Skill subscore uses proficiency, duration, endorsements, and assessment score. It is not enough for the candidate to list "RAG" or "Vector Search"; the scorer looks for trusted duration/proficiency and matching career evidence.

## B. Experience Relevance

Experience favors the JD's ideal 5-9 year band but allows exceptional candidates outside the band.

Components:

- years fit: maximum for 5-9 years.
- relevant months in ML/search/ranking/retrieval roles.
- production months in shipped systems.

## C. Career Quality

Career quality captures whether the candidate looks like someone who can thrive in Redrob's founding AI team.

Positive:

- product company or AI-product-company experience.
- current title alignment with ML/search/recommendation.
- senior/lead/staff ownership language.
- history that shows product and PM collaboration.

Negative:

- consulting-only career.
- current services role with no product-company history.
- title/history incoherence.

## D. Behavioral Signals

Behavior is a hireability modifier:

- recent activity.
- open-to-work flag.
- recruiter response rate.
- response time.
- interview completion rate.
- notice period.
- India location or relocation willingness.
- GitHub activity.
- recruiter saves and search appearances.
- profile completeness and verification.

The scorer does not let behavior rescue an irrelevant profile, but it can reorder technically close candidates.

## E. Risk Detection

Risk penalties detect traps and low-quality profiles:

- keyword stuffing: many AI skills with weak production history.
- self-learner AI language as the primary evidence.
- nontechnical current title.
- consulting-only career.
- pure research without production.
- CV/speech primary without IR/NLP/retrieval.
- pre-founding employment at known young companies.
- expert skills with zero months used.
- stale activity, very low response, very long notice, non-India/no-relocation.
- repeated role-description templates.
- experience far above the JD's senior-but-hands-on target band.

Hard honeypot penalties are large enough to push candidates out of the top 100 even if their text contains many JD terms.

## Why These Weights

The official composite is `0.50 * NDCG@10 + 0.30 * NDCG@50 + 0.15 * MAP + 0.05 * P@10`. That means top-rank precision matters far more than broad recall. The weighting therefore:

- makes production technical evidence the largest term.
- uses behavior as a tie-break/modifier, not the main signal.
- penalizes traps aggressively to protect top-100 honeypot rate.
- avoids overfitting to skills because the challenge explicitly contains keyword-stuffers.
