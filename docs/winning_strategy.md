# Evaluation Notes And Risk Checks

This file records the assumptions used when checking the final ranking. It is not part of the runtime pipeline.

## Likely Review Criteria

- Top-10 and top-50 relevance, based on the official metric weights.
- Evidence of production retrieval, ranking, search, or recommendation work.
- Whether behavior signals make a candidate realistic to contact.
- Whether obvious keyword-stuffed or inconsistent profiles appear in the submitted top 100.
- Whether the reasoning column is specific to the candidate instead of repeating a template.
- Whether the run can be reproduced on CPU without network calls.

## Ranking Review Approach

- Treat profile fields by trust level: career history first, then current title, behavior signals, skills, and summary text.
- Check that top-ranked candidates have at least one work-history proof point for retrieval, search, ranking, matching, or evaluation.
- Use skills as supporting evidence, not as the main ranking reason.
- Review high-risk candidates manually when they have long notice periods, weak response rates, unusual locations, or repeated role descriptions.
- Prefer moving a risky candidate down rather than removing them entirely when the technical evidence is still strong.

## Common Failure Modes

- Ranking by the count of AI skills.
- Embedding full profile text without separating career history from skill lists.
- Ignoring Redrob behavior fields such as response rate, activity, notice period, and relocation.
- Letting a research-heavy profile outrank a production retrieval/search engineer.
- Producing reasoning that mentions facts not present in the candidate record.
- Depending on external APIs or local models that are not available during challenge reproduction.

## Honeypot And Template Checks

- Expert skills with zero months of use.
- Employment dates that conflict with known company timelines.
- Nontechnical current title paired with a long list of unrelated AI-system terms.
- Many AI skills with weak duration, endorsements, or role-history support.
- Consulting-only profiles without product deployment evidence.
- Repeated role descriptions across jobs that look copied rather than specific.

## Top-Rank Quality Checks

- The top 10 should mostly contain candidates with production retrieval, search, ranking, recommendation, or candidate-matching evidence.
- The top 50 should avoid profiles that only have adjacent AI or analytics experience.
- Long-notice or outside-India candidates should not outrank similar candidates who are easier to hire.
- Behavior signals should reorder close technical matches, not replace technical relevance.
