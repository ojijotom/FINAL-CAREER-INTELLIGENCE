
"""Calculate explainable career compatibility scores.

Missing information is treated as not assessed, not as a score of zero.
Skill scores are calculated from assessed requirements only, and coverage
is reported separately so that incomplete profiles remain visible.
"""

import math
import re
from typing import Any


DEFAULT_WEIGHTS = {
    "skills": 0.65,
    "education": 0.15,
    "interests": 0.15,
    "evidence": 0.05,
}


EDUCATION_LEVELS = {
    "secondary": 1,
    "high school": 1,
    "high school certificate": 1,
    "kcse": 1,
    "certificate": 2,
    "professional certificate": 2,
    "diploma": 3,
    "higher diploma": 4,
    "bachelor": 5,
    "bachelor's": 5,
    "bachelors": 5,
    "degree": 5,
    "undergraduate degree": 5,
    "postgraduate diploma": 6,
    "honours degree": 6,
    "masters": 7,
    "master's": 7,
    "master degree": 7,
    "doctorate": 8,
    "phd": 8,
    "doctoral degree": 8,
}


def _normalise_name(value: Any) -> str:
    """Normalise names for consistent matching."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().casefold()


def _display_name(value: Any) -> str:
    """Return a clean display version of a name."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _parse_number(value: Any) -> float | None:
    """Safely parse a finite number, rejecting booleans and invalid values."""
    if isinstance(value, bool) or value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None

    if not math.isfinite(number):
        return None

    return number


def _normalise(value: Any) -> float:
    """Convert a valid numeric value to a percentage between 0 and 100."""
    number = _parse_number(value)

    if number is None:
        return 0.0

    return max(0.0, min(number, 100.0))


def _safe_weight(value: Any, default: float = 1.0) -> float:
    """Return a valid non-negative weighting value."""
    number = _parse_number(value)

    if number is None:
        return default

    return max(0.0, number)


def _prepare_student_skills(student_skills: list[dict]) -> dict:
    """Deduplicate student skills without transferring verification status.

    When duplicate records exist, the highest valid level is retained.
    If levels tie, a verified record takes priority.
    """
    lookup = {}

    for skill in student_skills or []:
        if not isinstance(skill, dict):
            continue

        name = _display_name(skill.get("name"))
        key = _normalise_name(name)

        if not key:
            continue

        level = _parse_number(skill.get("level"))

        # A record without a valid level is not an assessed skill.
        if level is None:
            continue

        level = max(0.0, min(level, 100.0))
        verified = skill.get("verified") is True

        candidate = {
            "name": name,
            "level": level,
            "verified": verified,
        }

        existing = lookup.get(key)

        if existing is None:
            lookup[key] = candidate
        elif level > existing["level"]:
            lookup[key] = candidate
        elif level == existing["level"] and verified:
            lookup[key] = candidate

    return lookup


def _prepare_requirements(career_requirements: list[dict]) -> list[dict]:
    """Validate and deduplicate career skill requirements.

    Duplicate requirements use the highest target level and highest weight.
    Their weights are not added together.
    """
    lookup = {}

    for requirement in career_requirements or []:
        if not isinstance(requirement, dict):
            continue

        name = _display_name(requirement.get("name"))
        key = _normalise_name(name)

        if not key:
            continue

        target = _parse_number(requirement.get("target_level", 100))
        weight = _parse_number(requirement.get("weight", 1))

        if target is None or weight is None:
            continue

        if target <= 0 or weight <= 0:
            continue

        target = min(target, 100.0)
        weight = max(0.0, weight)

        existing = lookup.get(key)

        if existing is None:
            lookup[key] = {
                "name": name,
                "target_level": target,
                "weight": weight,
            }
        else:
            existing["target_level"] = max(
                existing["target_level"], target
            )
            existing["weight"] = max(existing["weight"], weight)

    return list(lookup.values())


def calculate_skill_score(
    student_skills: list[dict],
    career_requirements: list[dict],
) -> dict:
    """Compare assessed student skills against career requirements.

    Student skill example:
        {"name": "Python", "level": 70, "verified": True}

    Career requirement example:
        {"name": "Python", "target_level": 90, "weight": 2}

    An absent or invalid student skill is not assessed. An explicitly
    recorded level of zero is a valid assessed level.
    """
    requirements = _prepare_requirements(career_requirements)
    student_lookup = _prepare_student_skills(student_skills)

    if not requirements:
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "unassessed_skills": [],
            "total_requirements": 0,
            "assessed_requirements": 0,
            "completeness": 0.0,
        }

    total_assessed_weight = 0.0
    achieved_weight = 0.0

    matched = []
    unassessed = []

    for requirement in requirements:
        name = requirement["name"]
        key = _normalise_name(name)
        target = requirement["target_level"]
        weight = requirement["weight"]

        student_skill = student_lookup.get(key)

        if student_skill is None:
            unassessed.append({
                "name": name,
                "current_level": None,
                "target_level": target,
                "gap": None,
                "status": "not_assessed",
            })
            continue

        current = student_skill["level"]
        contribution = min(current / target, 1.0) * weight

        achieved_weight += contribution
        total_assessed_weight += weight

        matched.append({
            "name": name,
            "current_level": current,
            "target_level": target,
            "gap": round(max(0.0, target - current), 2),
            "verified": student_skill["verified"],
            "status": (
                "at_target" if current >= target else "needs_improvement"
            ),
        })

    score = None

    if total_assessed_weight > 0:
        score = round(
            (achieved_weight / total_assessed_weight) * 100, 2
        )

    total_count = len(requirements)
    assessed_count = len(matched)

    completeness = (
        assessed_count / total_count
    ) * 100

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": unassessed,
        "unassessed_skills": unassessed,
        "total_requirements": total_count,
        "assessed_requirements": assessed_count,
        "completeness": round(completeness, 2),
    }


def _education_score(actual: Any, required: Any) -> float | None:
    """Compare recognised education levels.

    A higher recognised qualification meets a lower minimum requirement.
    Unknown labels are compared only when they match exactly.
    """
    actual_name = _normalise_name(actual)
    required_name = _normalise_name(required)

    if not actual_name or not required_name:
        return None

    actual_level = EDUCATION_LEVELS.get(actual_name)
    required_level = EDUCATION_LEVELS.get(required_name)

    if actual_level is not None and required_level is not None:
        return 100.0 if actual_level >= required_level else 0.0

    if actual_name == required_name:
        return 100.0

    # An unknown qualification must not receive an arbitrary score.
    return None


def _normalise_interests(values: list) -> set[str]:
    """Clean and deduplicate interest names."""
    if not isinstance(values, (list, tuple, set)):
        return set()

    return {
        _normalise_name(value)
        for value in values
        if _normalise_name(value)
    }


def calculate_career_score(
    student: dict,
    career: dict,
    weights: dict | None = None,
) -> dict:
    """Calculate a weighted, explainable career compatibility score.

    Components without sufficient information are excluded and the
    remaining valid component weights are rebalanced.
    """
    student = student if isinstance(student, dict) else {}
    career = career if isinstance(career, dict) else {}

    selected_weights = {**DEFAULT_WEIGHTS, **(weights or {})}

    requirements = career.get("required_skills", [])
    if not isinstance(requirements, list):
        requirements = []

    student_skills = student.get("skills", [])
    if not isinstance(student_skills, list):
        student_skills = []

    skill_result = calculate_skill_score(
        student_skills,
        requirements,
    )

    components = {}

    if skill_result["score"] is not None:
        components["skills"] = skill_result["score"]

    education_required = career.get("education_level")
    education_actual = student.get("education_level")

    education_result = _education_score(
        education_actual,
        education_required,
    )

    if education_result is not None:
        components["education"] = education_result

    required_interests = _normalise_interests(
        career.get("interests", [])
    )
    student_interests = _normalise_interests(
        student.get("interests", [])
    )

    if required_interests and student_interests:
        components["interests"] = round(
            len(required_interests & student_interests)
            / len(required_interests) * 100,
            2,
        )

    if skill_result["matched_skills"]:
        verified_count = sum(
            1 for item in skill_result["matched_skills"]
            if item["verified"]
        )

        components["evidence"] = round(
            verified_count / len(skill_result["matched_skills"]) * 100,
            2,
        )

    valid_weights = {}

    for key in components:
        weight = _parse_number(selected_weights.get(key))

        if weight is not None and weight > 0:
            valid_weights[key] = weight

    active_weight = sum(valid_weights.values())

    overall_score = None

    if active_weight > 0:
        overall_score = sum(
            components[key] * weight
            for key, weight in valid_weights.items()
        ) / active_weight

    # Profile completeness is based on available information, not scores.
    completeness_sections = {
        "skills": skill_result["completeness"],
        "education": (
            100.0 if education_actual else 0.0
        ),
        "interests": (
            100.0 if student_interests else 0.0
        ),
    }

    data_completeness = sum(
        completeness_sections.values()
    ) / len(completeness_sections)

    return {
        "career_id": career.get("id"),
        "career_title": career.get("title", "Unnamed career"),
        "compatibility_score": (
            round(overall_score, 2)
            if overall_score is not None else None
        ),
        "components": {
            key: round(value, 2)
            for key, value in components.items()
        },
        "skill_analysis": skill_result,
        "data_completeness": round(data_completeness, 2),
        "data_completeness_by_section": {
            key: round(value, 2)
            for key, value in completeness_sections.items()
        },
    }
