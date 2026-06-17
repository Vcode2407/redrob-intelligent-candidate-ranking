"""Candidate feature extraction.

The extractor is intentionally evidence-weighted:
- career-history proof is worth much more than skill-list keywords;
- behavioral readiness modifies otherwise similar candidates;
- inconsistent or impossible profiles are pushed down hard.
"""

from __future__ import annotations

import math
from typing import Any

from . import config as cfg
from .models import CandidateFacts, FeatureVector
from .utils import clamp, contains_any, count_matches, safe_date


class CandidateFeatureExtractor:
    """Extract weighted features from a single candidate record."""

    def extract(self, candidate: dict[str, Any]) -> FeatureVector:
        profile = candidate["profile"]
        signals = candidate["redrob_signals"]
        history = candidate.get("career_history", [])
        skills = candidate.get("skills", [])

        candidate_id = str(candidate["candidate_id"])
        title = str(profile.get("current_title", ""))
        title_l = title.lower()
        headline_l = str(profile.get("headline", "")).lower()
        summary_l = str(profile.get("summary", "")).lower()
        history_text = " ".join(
            (
                str(item.get("title", ""))
                + " "
                + str(item.get("description", ""))
                + " "
                + str(item.get("company", ""))
                + " "
                + str(item.get("industry", ""))
            ).lower()
            for item in history
        )
        current_description = " ".join(
            str(item.get("description", "")).lower()
            for item in history
            if item.get("is_current")
        )

        skill_by_name = {str(skill.get("name", "")).lower(): skill for skill in skills}
        all_text = " ".join([headline_l, summary_l, history_text, " ".join(skill_by_name)])

        title_score = self._title_score(title_l)
        technical_history_score, history_hits = self._technical_history_score(
            history_text, all_text, skill_by_name
        )
        skill_score, ai_skill_count, trusted_ai_skills = self._skill_score(
            skill_by_name, signals
        )
        experience_score = self._experience_score(profile, history)
        career_score, all_consulting, current_services_no_product = self._career_score(
            profile, history, title_score, history_text, headline_l
        )
        behavior_score = self._behavior_score(profile, signals)

        risk_penalty, flags = self._risk_penalty(
            candidate=candidate,
            title_l=title_l,
            title_score=title_score,
            summary_l=summary_l,
            history_text=history_text,
            current_description=current_description,
            technical_history_score=technical_history_score,
            ai_skill_count=ai_skill_count,
            trusted_ai_skills=trusted_ai_skills,
            all_consulting=all_consulting,
            current_services_no_product=current_services_no_product,
        )

        technical_score = technical_history_score + skill_score
        availability_gate = 0.72 + 0.28 * clamp(behavior_score)
        raw_score = (
            (
                2.85 * technical_score
                + 1.35 * experience_score
                + 1.15 * career_score
            )
            * availability_gate
            + 1.45 * behavior_score
            - 2.60 * risk_penalty
        )

        if technical_score < 1.20 and title_score < 0.70:
            raw_score -= 1.20
        if technical_score < 0.70:
            raw_score -= 1.00

        facts = self._facts(
            candidate_id=candidate_id,
            profile=profile,
            signals=signals,
            skill_by_name=skill_by_name,
            history_text=history_text,
            technical_history_score=technical_history_score,
            flags=flags,
            history_hits=history_hits,
        )

        return FeatureVector(
            candidate_id=candidate_id,
            raw_score=raw_score,
            technical_score=technical_score,
            technical_history_score=technical_history_score,
            skill_score=skill_score,
            experience_score=experience_score,
            career_score=career_score,
            behavior_score=behavior_score,
            risk_penalty=risk_penalty,
            facts=facts,
        )

    @staticmethod
    def _title_score(title_l: str) -> float:
        title_score = cfg.TITLE_WEIGHTS.get(title_l, 0.0)
        if title_score:
            return title_score
        if contains_any(title_l, cfg.TECH_TITLE_HINTS):
            return 0.40
        return 0.0

    @staticmethod
    def _technical_history_score(
        history_text: str, all_text: str, skill_by_name: dict[str, dict[str, Any]]
    ) -> tuple[float, dict[str, int]]:
        rank_hits = count_matches(history_text, cfg.RANKING_TERMS)
        retrieval_hits = count_matches(history_text, cfg.RETRIEVAL_TERMS)
        eval_hits = count_matches(history_text, cfg.EVAL_TERMS)
        production_hits = count_matches(history_text, cfg.PRODUCTION_TERMS)
        hr_hits = count_matches(history_text, cfg.HR_TECH_TERMS)

        score = (
            clamp(rank_hits / 4.0) * 1.30
            + clamp(retrieval_hits / 5.0) * 1.10
            + clamp(eval_hits / 4.0) * 0.90
            + clamp(production_hits / 5.0) * 0.70
            + clamp(hr_hits / 2.0) * 0.55
        )

        if "python" in history_text or "python" in skill_by_name:
            score += 0.12
        if (
            "llm-based re-ranker" in history_text
            or "fine-tuned" in history_text
            or "lora" in history_text
            or "qlora" in history_text
        ):
            score += 0.18
        if hr_hits > 0:
            score += 0.45
        if "50m+ queries" in history_text or "candidate corpus" in history_text:
            score += 0.55
        if "computer vision" in history_text and not contains_any(
            history_text, ("nlp", "retrieval", "search", "ranking", "recommendation")
        ):
            score -= 0.45
        if "speech" in all_text and not contains_any(
            history_text, ("nlp", "retrieval", "search", "ranking", "recommendation")
        ):
            score -= 0.35

        return clamp(score, 0.0, 4.80), {
            "ranking": rank_hits,
            "retrieval": retrieval_hits,
            "evaluation": eval_hits,
            "production": production_hits,
            "hr_tech": hr_hits,
        }

    @staticmethod
    def _skill_score(
        skill_by_name: dict[str, dict[str, Any]], signals: dict[str, Any]
    ) -> tuple[float, int, int]:
        score = 0.0
        ai_skill_count = 0
        trusted_ai_skills = 0
        assessments = {
            str(name).lower(): float(value)
            for name, value in signals.get("skill_assessment_scores", {}).items()
        }

        for group, names in cfg.SKILL_GROUPS.items():
            best = 0.0
            for name in names:
                skill = skill_by_name.get(name)
                if not skill:
                    continue
                if group != "python":
                    ai_skill_count += 1
                proficiency = {
                    "beginner": 0.25,
                    "intermediate": 0.50,
                    "advanced": 0.78,
                    "expert": 1.00,
                }.get(skill.get("proficiency"), 0.30)
                duration = clamp(float(skill.get("duration_months") or 0) / 36.0)
                endorsements = clamp(math.log1p(float(skill.get("endorsements") or 0)) / 4.0)
                assessment = clamp(assessments.get(name, 0.0) / 100.0)
                value = (
                    0.55 * proficiency
                    + 0.25 * duration
                    + 0.10 * endorsements
                    + 0.10 * assessment
                )
                best = max(best, value)
                if duration > 0.40 and proficiency >= 0.50 and group != "python":
                    trusted_ai_skills += 1
            score += cfg.SKILL_GROUP_WEIGHTS[group] * best

        return score, ai_skill_count, trusted_ai_skills

    @staticmethod
    def _experience_score(profile: dict[str, Any], history: list[dict[str, Any]]) -> float:
        years = float(profile.get("years_of_experience") or 0.0)
        if 5.0 <= years <= 9.0:
            years_fit = 1.00
        elif 4.0 <= years < 5.0 or 9.0 < years <= 10.5:
            years_fit = 0.72
        elif 3.0 <= years < 4.0 or 10.5 < years <= 12.0:
            years_fit = 0.42
        else:
            years_fit = 0.12

        relevant_months = 0
        production_months = 0
        relevant_terms = (
            cfg.RANKING_TERMS
            + cfg.RETRIEVAL_TERMS
            + cfg.EVAL_TERMS
            + (
                "machine learning",
                "ml engineer",
                "ml systems",
                "data scientist",
                "recommendation",
                "search",
            )
        )
        for item in history:
            text = (str(item.get("title", "")) + " " + str(item.get("description", ""))).lower()
            months = int(item.get("duration_months") or 0)
            if contains_any(text, relevant_terms):
                relevant_months += months
            if contains_any(text, cfg.PRODUCTION_TERMS):
                production_months += months

        return (
            0.75 * years_fit
            + 0.65 * clamp(relevant_months / 60.0)
            + 0.35 * clamp(production_months / 48.0)
        )

    @staticmethod
    def _career_score(
        profile: dict[str, Any],
        history: list[dict[str, Any]],
        title_score: float,
        history_text: str,
        headline_l: str,
    ) -> tuple[float, bool, bool]:
        companies = [str(item.get("company", "")).lower() for item in history]
        current_company = str(profile.get("current_company", "")).lower()
        product_count = sum(1 for company in companies if company in cfg.PRODUCT_COMPANIES)
        ai_product_count = sum(1 for company in companies if company in cfg.AI_PRODUCT_COMPANIES)
        consulting_count = sum(1 for company in companies if company in cfg.CONSULTING_COMPANIES)
        all_consulting = bool(companies and consulting_count == len(companies))
        current_services_no_product = (
            current_company in cfg.CONSULTING_COMPANIES and product_count == 0
        )

        product_score = (
            clamp(product_count / 2.0) * 0.55 + clamp(ai_product_count / 1.0) * 0.25
        )
        if current_company in cfg.PRODUCT_COMPANIES:
            product_score += 0.18
        if current_company in cfg.AI_PRODUCT_COMPANIES:
            product_score += 0.18
        product_score = clamp(product_score, 0.0, 0.85)

        leadership_text = " ".join(
            [str(profile.get("current_title", "")).lower(), headline_l, history_text]
        )
        leadership = (
            0.28
            if contains_any(
                leadership_text,
                ("senior", "lead", "staff", "owned", "mentored", "led", "architecture"),
            )
            else 0.0
        )
        return title_score + product_score + leadership, all_consulting, current_services_no_product

    @staticmethod
    def _behavior_score(profile: dict[str, Any], signals: dict[str, Any]) -> float:
        last_active = safe_date(signals.get("last_active_date"))
        days_since_active = (
            (cfg.REFERENCE_DATE - last_active).days if last_active is not None else 999
        )
        if days_since_active <= 30:
            recency = 1.00
        elif days_since_active <= 60:
            recency = 0.80
        elif days_since_active <= 120:
            recency = 0.55
        elif days_since_active <= 180:
            recency = 0.25
        else:
            recency = 0.0

        response = clamp(float(signals.get("recruiter_response_rate") or 0.0) / 0.75)
        response_time_hours = float(signals.get("avg_response_time_hours") or 999.0)
        if response_time_hours <= 24:
            response_time = 1.00
        elif response_time_hours <= 72:
            response_time = 0.80
        elif response_time_hours <= 120:
            response_time = 0.55
        elif response_time_hours <= 200:
            response_time = 0.25
        else:
            response_time = 0.05

        interview = clamp(float(signals.get("interview_completion_rate") or 0.0) / 0.90)
        notice = int(signals.get("notice_period_days") or 180)
        if notice <= 30:
            notice_score = 1.00
        elif notice <= 60:
            notice_score = 0.75
        elif notice <= 90:
            notice_score = 0.45
        elif notice <= 120:
            notice_score = 0.20
        else:
            notice_score = 0.05

        country = str(profile.get("country", ""))
        location_text = (str(profile.get("location", "")) + " " + country).lower()
        if country == "India" and contains_any(location_text, cfg.TIER1_LOCATION_HINTS):
            location_score = 1.00
        elif country == "India":
            location_score = 0.78
        else:
            location_score = 0.45
        if signals.get("willing_to_relocate"):
            location_score = max(location_score, 0.86)

        github = float(signals.get("github_activity_score") or -1.0)
        github_score = 0.0 if github < 0.0 else clamp(github / 60.0)
        market_heat = (
            clamp(float(signals.get("saved_by_recruiters_30d") or 0.0) / 15.0) * 0.5
            + clamp(float(signals.get("search_appearance_30d") or 0.0) / 200.0) * 0.5
        )
        score = (
            0.18 * recency
            + 0.18 * response
            + 0.10 * response_time
            + 0.16 * interview
            + 0.10 * notice_score
            + 0.12 * location_score
            + 0.08 * github_score
            + 0.04 * clamp(float(signals.get("profile_completeness_score") or 0.0) / 90.0)
            + 0.04 * market_heat
        )
        if signals.get("open_to_work_flag"):
            score += 0.08
        if signals.get("verified_email"):
            score += 0.02
        if signals.get("verified_phone"):
            score += 0.02
        if signals.get("linkedin_connected"):
            score += 0.02
        return score

    @staticmethod
    def _risk_penalty(
        *,
        candidate: dict[str, Any],
        title_l: str,
        title_score: float,
        summary_l: str,
        history_text: str,
        current_description: str,
        technical_history_score: float,
        ai_skill_count: int,
        trusted_ai_skills: int,
        all_consulting: bool,
        current_services_no_product: bool,
    ) -> tuple[float, list[str]]:
        risk = 0.0
        flags: list[str] = []
        nontechnical_title = title_l in cfg.NON_TECH_TITLES or (
            title_score == 0.0
            and not contains_any(
                title_l,
                ("engineer", "developer", "scientist", "architect", "platform", "search"),
            )
        )

        if all_consulting:
            risk += 1.00
            flags.append("consulting_only")
        elif current_services_no_product:
            risk += 0.55
            flags.append("services_without_product_history")

        self_learner = contains_any(summary_l, cfg.SELF_LEARNER_TERMS)
        if ai_skill_count >= 6 and technical_history_score < 1.00 and (
            nontechnical_title or title_score < 0.40
        ):
            risk += 2.30
            flags.append("keyword_stuffing")
        elif ai_skill_count >= 5 and technical_history_score < 0.70:
            risk += 1.10
            flags.append("skills_not_backed_by_history")

        if self_learner and technical_history_score < 1.20:
            risk += 0.90
            flags.append("self_learner_ai_only")
        if nontechnical_title:
            if technical_history_score < 1.40:
                risk += 1.35
                flags.append("nontechnical_current_title")
            else:
                risk += 1.10
                flags.append("title_history_incoherence")

        if title_l == "ai research engineer" and not contains_any(history_text, cfg.PRODUCTION_TERMS):
            risk += 1.20
            flags.append("research_without_production")
        if title_l == "computer vision engineer" and not contains_any(
            history_text, ("retrieval", "search", "ranking", "recommendation", "nlp")
        ):
            risk += 0.85
            flags.append("cv_primary_not_ir")

        expert_zero = sum(
            1
            for skill in candidate.get("skills", [])
            if skill.get("proficiency") == "expert" and int(skill.get("duration_months") or 0) == 0
        )
        if expert_zero >= 5:
            risk += 6.00
            flags.append("honeypot_zero_duration_expert_stack")
        elif expert_zero:
            risk += 0.55
            flags.append("zero_duration_expert_skill")

        for item in candidate.get("career_history", []):
            company = str(item.get("company", "")).lower()
            founding_year = cfg.COMPANY_FOUNDING_YEARS.get(company)
            start_date = safe_date(item.get("start_date"))
            if founding_year and start_date and start_date.year < founding_year:
                risk += 5.00
                flags.append("honeypot_pre_founding_role")
                break

        salary = candidate.get("redrob_signals", {}).get("expected_salary_range_inr_lpa") or {}
        if float(salary.get("min") or 0.0) > float(salary.get("max") or 0.0):
            risk += 0.05
            flags.append("salary_range_inverted")

        signals = candidate.get("redrob_signals", {})
        profile = candidate.get("profile", {})
        response_rate = float(signals.get("recruiter_response_rate") or 0.0)
        if response_rate < 0.15:
            risk += 1.25
            flags.append("very_low_response_rate")
        last_active = safe_date(signals.get("last_active_date"))
        if last_active is not None and (cfg.REFERENCE_DATE - last_active).days > 120:
            risk += 0.90
            flags.append("stale_activity")
        notice_days = int(signals.get("notice_period_days") or 180)
        if notice_days >= 150:
            risk += 2.00
            flags.append("very_long_notice")
        elif notice_days >= 120:
            risk += 0.55
            flags.append("long_notice")
        if profile.get("country") != "India" and not signals.get("willing_to_relocate"):
            risk += 1.60
            flags.append("outside_india_no_relocation")
        if float(profile.get("years_of_experience") or 0.0) > 12.0:
            risk += 1.40
            flags.append("outside_experience_band_high")

        descriptions = [
            str(item.get("description", "")).strip().lower()[:180]
            for item in candidate.get("career_history", [])
            if str(item.get("description", "")).strip()
        ]
        duplicate_descriptions = len(descriptions) - len(set(descriptions))
        if duplicate_descriptions:
            risk += 0.85 * duplicate_descriptions
            flags.append("repeated_role_description")

        if (
            title_l in cfg.NON_TECH_TITLES
            and contains_any(
                current_description,
                (
                    "java backend",
                    "frontend engineering",
                    "ml feature",
                    "ranking",
                    "semantic search",
                    "recommendation system",
                    "rag-based",
                ),
            )
            and trusted_ai_skills < 2
        ):
            risk += 0.85
            flags.append("current_title_description_mismatch")

        return risk, flags

    @staticmethod
    def _facts(
        *,
        candidate_id: str,
        profile: dict[str, Any],
        signals: dict[str, Any],
        skill_by_name: dict[str, dict[str, Any]],
        history_text: str,
        technical_history_score: float,
        flags: list[str],
        history_hits: dict[str, int],
    ) -> CandidateFacts:
        evidence: list[str] = []
        if contains_any(history_text, ("50m+ queries", "50m queries")):
            evidence.append("ranker serving 50M+ queries/month")
        if "30m+ candidate corpus" in history_text:
            evidence.append("embedding search across a 30M+ candidate corpus")
        if "35m+ items" in history_text:
            evidence.append("semantic search over 35M+ items")
        if "10m+ users" in history_text:
            evidence.append("recommendation system serving 10M+ users")
        if "500k documents" in history_text:
            evidence.append("semantic search over 500K documents")
        if history_hits["hr_tech"] > 0:
            evidence.append("recruiter or candidate matching workflow")
        if history_hits["ranking"] > 0:
            evidence.append("ranking/recommendation systems")
        if history_hits["retrieval"] > 0:
            evidence.append("embedding or vector retrieval")
        if history_hits["evaluation"] > 0:
            evidence.append("ranking evaluation and A/B metrics")
        if history_hits["production"] > 0 or technical_history_score > 2.5:
            evidence.append("production deployment evidence")
        if not evidence and technical_history_score > 1.0:
            evidence.append("applied ML systems experience")

        reasoning_skills = []
        for skill_name, skill in skill_by_name.items():
            if skill_name in cfg.RELEVANT_SKILLS_FOR_REASONING:
                reasoning_skills.append(str(skill.get("name", skill_name)))
        reasoning_skills = sorted(set(reasoning_skills), key=str.lower)[:5]

        concerns: list[str] = []
        notice = int(signals.get("notice_period_days") or 180)
        if notice > 90:
            concerns.append(f"{notice}-day notice period")
        response_rate = float(signals.get("recruiter_response_rate") or 0.0)
        if response_rate < 0.30:
            concerns.append(f"low recruiter response rate ({response_rate:.2f})")
        last_active = safe_date(signals.get("last_active_date"))
        if last_active is not None and (cfg.REFERENCE_DATE - last_active).days > 120:
            concerns.append("stale platform activity")
        if float(profile.get("years_of_experience") or 0.0) > 12.0:
            concerns.append("outside the JD experience band")
        if profile.get("country") != "India" and not signals.get("willing_to_relocate"):
            concerns.append("outside India without relocation signal")
        if any(flag.startswith("services") or flag == "consulting_only" for flag in flags):
            concerns.append("services-heavy career history")
        if any(flag.startswith("honeypot") for flag in flags):
            concerns.append("profile consistency risk")

        return CandidateFacts(
            candidate_id=candidate_id,
            years=float(profile.get("years_of_experience") or 0.0),
            title=str(profile.get("current_title", "")),
            company=str(profile.get("current_company", "")),
            location=str(profile.get("location", "")),
            country=str(profile.get("country", "")),
            response_rate=response_rate,
            notice_days=notice,
            last_active_date=str(signals.get("last_active_date", "")),
            github_activity_score=float(signals.get("github_activity_score") or -1.0),
            open_to_work=bool(signals.get("open_to_work_flag")),
            evidence=evidence[:5],
            skills=reasoning_skills,
            concerns=concerns[:3],
            risk_flags=flags,
        )
