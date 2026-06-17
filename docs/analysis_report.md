# Analysis Report

## Files Reviewed

- `candidate_schema.json`
- `job_description.docx`
- `redrob_signals_doc.docx`
- `submission_spec.docx`
- `sample_candidates.json`
- `sample_submission.csv`
- `Idea Submission Template _ Redrob.pdf`

## Mandatory JD Requirements

The role is Senior AI Engineer on Redrob's AI engineering team. The JD points to a candidate who has built retrieval, matching, ranking, or recommendation systems in production, not someone who only lists AI tools.

Must-have evidence:

- Production embeddings-based retrieval deployed to real users.
- Vector database or hybrid search infrastructure such as FAISS, Pinecone, Weaviate, Qdrant, Milvus, OpenSearch, Elasticsearch, or equivalent.
- Strong Python and production code quality.
- Ranking evaluation literacy: NDCG, MRR, MAP, offline benchmarks, online A/B tests, recruiter feedback loops.
- Product-engineering judgment: can ship a retrieval or ranking feature, measure it, and iterate from recruiter/user feedback.
- Recent hands-on coding, not only architecture or management.
- Roughly 5-9 years, with the ideal band around 6-8 years. The JD allows exceptions when other signals are strong.

Preferred but not mandatory:

- LLM fine-tuning with LoRA/QLoRA/PEFT.
- Learning-to-rank models.
- HR-tech, recruiting-tech, marketplace, search, or recommendation product exposure.
- Distributed systems or large-scale inference optimization.
- External validation via open source, talks, papers, or visible ML work.

## Strong Positive Signals

- Career history explicitly says the candidate owned ranking, retrieval, recommendation, semantic search, or candidate matching systems.
- Work includes production detail: query volume, user volume, latency, index refresh, rollback, monitoring, model drift, or A/B testing.
- Evaluation framework ownership, especially NDCG/MRR/offline-online correlation.
- Recruiter-facing or candidate-JD matching product context.
- Product-company or AI-product-company history rather than services-only delivery.
- Current title aligns with AI/search/recommendation systems work.
- Recent platform activity, high recruiter response rate, high interview completion, shorter notice, and location/relocation feasibility.

## Negative Signals

- Long skill lists with AI buzzwords but no matching career-history evidence.
- Summary language such as "curious about AI", "experimented with ChatGPT", "online courses", or "LangChain side project" as the main AI evidence.
- Nontechnical current titles with AI skill stuffing.
- Consulting-only career at TCS/Infosys/Wipro/Accenture/Cognizant/Capgemini/etc.
- Pure research profiles without production deployment.
- Primary computer vision, speech, or robotics background without NLP/IR relevance.
- Senior architects or leads with no recent coding evidence.
- Stale platform activity, low response rate, very long notice, or no relocation path.

## Behavioral Indicators

From `redrob_signals_doc.docx`, the most important behavior fields for hireability are:

- `last_active_date`
- `open_to_work_flag`
- `recruiter_response_rate`
- `avg_response_time_hours`
- `interview_completion_rate`
- `offer_acceptance_rate`
- `notice_period_days`
- `willing_to_relocate`
- `github_activity_score`
- `saved_by_recruiters_30d`
- `search_appearance_30d`
- `profile_completeness_score`
- verification and LinkedIn connection fields

These are used as a modifier, not a replacement for technical fit. A strong technical candidate with poor response rate can still rank, but is pushed below similarly qualified reachable candidates.

## Disqualifying Candidate Patterns

- Honeypot: employment predating a known company's founding year.
- Honeypot: many expert skills with zero months of use.
- Severe title/history mismatch where a nontechnical current role is paired with unrelated AI-system descriptions.
- Keyword stuffer: many AI skills, low duration/endorsement trust, and no relevant production history.
- Services-only career without product-company evidence.
- Pure research without deployment.
- Stale profile with weak engagement signals.

## Candidate Pool Observations

The pool has 100,000 candidates. A small slice has AI/ML-style current titles, while many profiles are business, HR, sales, content, operations, or non-ML engineering backgrounds. The sample submission ranks several non-engineering profiles highly when they contain AI skill terms. That supports a field-aware approach where work history is more trusted than skill keywords.

The strongest histories are specific: recruiter-facing ranking pipelines, semantic search over large corpora, candidate-corpus embedding search, production recommendation systems, or ranking evaluation pipelines. The implemented ranker gives those signals more weight than broad AI wording in summaries.
