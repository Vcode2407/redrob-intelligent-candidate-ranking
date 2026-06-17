# Winning Strategy

## Likely Hidden Evaluation Criteria

- Top-10 exactness: NDCG@10 has 50% weight, so the first page matters most.
- Production retrieval/ranking relevance, not broad AI vocabulary.
- Behavioral availability for candidates who are otherwise close.
- Honeypot rate in top 100.
- Reasoning quality during manual review.
- Reproducible CPU-only runtime.
- Code clarity and ability to defend design choices.

## How Top Teams Will Approach It

- Parse the JD as a hiring rubric, not a bag of words.
- Separate profile fields by trust level: career history > title > behavior > skills > summary buzzwords.
- Use explicit negative controls for keyword stuffing and synthetic inconsistencies.
- Inspect top-ranked candidates manually through debug artifacts.
- Optimize top-10 precision before broad recall.

## Common Mistakes

- Counting AI skills and ranking by total.
- Using embeddings over full text without field weighting, causing skill stuffers to dominate.
- Ignoring Redrob behavioral signals.
- Not checking honeypots.
- Producing generic or hallucinated reasoning.
- Depending on API calls or heavy local models that fail Stage 3 reproduction.
- Submitting a valid CSV but no defensible methodology.

## Honeypot Avoidance

- Detect expert skills with zero months of use.
- Detect employment before known company founding year.
- Penalize nontechnical title plus unrelated AI-system descriptions.
- Penalize inflated AI skill lists without career evidence.
- Penalize inverted or inconsistent profile fields lightly unless paired with stronger risk.
- Keep risk flags in debug output and inspect top 100 before submission.

## Improving NDCG@10 And NDCG@50

- Put exact production ranking/search/retrieval owners at the top.
- Prefer candidates with evidence of evaluation frameworks and online/offline correlation.
- Use behavior only after technical evidence is established.
- Move low-response or stale candidates below similarly technical active candidates.
- Keep long-notice/outside-India candidates if technically exceptional, but not ahead of equivalent reachable candidates.
- Avoid filler profiles in the top 50; every top-50 candidate should have at least one career-history proof point.

