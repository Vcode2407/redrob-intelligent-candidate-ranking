from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from src.features import CandidateFeatureExtractor
from src.models import RankedCandidate
from src.submission import write_submission
from src.validate import validate_submission


def base_candidate() -> dict:
    return {
        "candidate_id": "CAND_0000001",
        "profile": {
            "anonymized_name": "Test Candidate",
            "headline": "Search Engineer",
            "summary": "Production ML engineer.",
            "location": "Pune, Maharashtra",
            "country": "India",
            "years_of_experience": 7.0,
            "current_title": "Search Engineer",
            "current_company": "Razorpay",
            "current_company_size": "1001-5000",
            "current_industry": "Fintech",
        },
        "career_history": [
            {
                "company": "Razorpay",
                "title": "Search Engineer",
                "start_date": "2022-01-01",
                "end_date": None,
                "duration_months": 48,
                "is_current": True,
                "industry": "Fintech",
                "company_size": "1001-5000",
                "description": (
                    "Owned a production semantic search and ranking system using "
                    "BGE embeddings, FAISS, NDCG evaluation, and A/B tests."
                ),
            }
        ],
        "education": [],
        "skills": [
            {
                "name": "Python",
                "proficiency": "advanced",
                "endorsements": 10,
                "duration_months": 60,
            },
            {
                "name": "Vector Search",
                "proficiency": "advanced",
                "endorsements": 8,
                "duration_months": 36,
            },
        ],
        "redrob_signals": {
            "profile_completeness_score": 90,
            "signup_date": "2025-01-01",
            "last_active_date": "2026-05-20",
            "open_to_work_flag": True,
            "profile_views_received_30d": 20,
            "applications_submitted_30d": 2,
            "recruiter_response_rate": 0.80,
            "avg_response_time_hours": 24,
            "skill_assessment_scores": {},
            "connection_count": 100,
            "endorsements_received": 20,
            "notice_period_days": 30,
            "expected_salary_range_inr_lpa": {"min": 30, "max": 45},
            "preferred_work_mode": "hybrid",
            "willing_to_relocate": True,
            "github_activity_score": 50,
            "search_appearance_30d": 100,
            "saved_by_recruiters_30d": 6,
            "interview_completion_rate": 0.9,
            "offer_acceptance_rate": 0.8,
            "verified_email": True,
            "verified_phone": True,
            "linkedin_connected": True,
        },
    }


class CoreTests(unittest.TestCase):
    def test_production_search_candidate_scores_above_keyword_stuffer(self) -> None:
        extractor = CandidateFeatureExtractor()
        good = base_candidate()
        stuffer = base_candidate()
        stuffer["candidate_id"] = "CAND_0000002"
        stuffer["profile"]["current_title"] = "Marketing Manager"
        stuffer["profile"]["summary"] = "Curious about AI, ChatGPT, LangChain, and side projects."
        stuffer["career_history"][0]["title"] = "Marketing Manager"
        stuffer["career_history"][0]["description"] = "Owned content marketing and SEO."
        stuffer["skills"].extend(
            [
                {"name": "RAG", "proficiency": "advanced", "endorsements": 1, "duration_months": 4},
                {
                    "name": "Embeddings",
                    "proficiency": "advanced",
                    "endorsements": 1,
                    "duration_months": 4,
                },
                {
                    "name": "Recommendation Systems",
                    "proficiency": "advanced",
                    "endorsements": 1,
                    "duration_months": 4,
                },
            ]
        )

        self.assertGreater(extractor.extract(good).raw_score, extractor.extract(stuffer).raw_score)

    def test_submission_validator_accepts_valid_rows(self) -> None:
        candidate = base_candidate()
        features = CandidateFeatureExtractor().extract(candidate)
        rows = [
            RankedCandidate(
                candidate_id=f"CAND_{idx:07d}",
                rank=idx,
                score=1.0 - idx * 0.001,
                reasoning="Specific reasoning.",
                raw_score=10.0 - idx,
                features=features,
            )
            for idx in range(1, 101)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "submission.csv"
            write_submission(rows, path)
            self.assertEqual(validate_submission(path), [])


if __name__ == "__main__":
    unittest.main()

