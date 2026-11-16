"""Calculate explainable career compatibility scores."""

from typing import Any


DEFAULT_WEIGHTS = {
    "skills": 0.65,
    "education": 0.15,
    "interests": 0.15,
    "evidence": 0.05,
}


def _normalise(value: Any) -> float:
    """Convert a numeric value to a safe percentage between 0 and 100."""
    try:
        return max(0.0, min(float(value), 100.0))
    except (TypeError, ValueError):
        return 0.0


def calculate_skill_score(
    student_skills: list[dict],
    career_requirements: list[dict],
) -> dict:
    """
    Compare student skill levels against career requirements.

    Expected student skill:
        {"name": "Python", "level": 70, "verified": True}

    Expected career requirement:
        {"name": "Python", "target_level": 90, "weight": 2}
    """
    if not career_requirements:
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "completeness": 0.0,
        }

    student_lookup = {
        str(skill.get("name", "")).strip().casefold(): skill
        for skill in student_skills
        if skill.get("name")
    }

    total_weight = 0.0
    achieved_weight = 0.0
    matched = []
    missing = []
    available_count = 0

    for requirement in career_requirements:
        name = str(requirement.get("name", "")).strip()
        key = name.casefold()

        try:
            target = max(1.0, float(requirement.get("target_level", 100)))
            weight = max(0.0, float(requirement.get("weight", 1)))
        except (TypeError, ValueError):
            continue

        if not name or weight <= 0:
            continue

        total_weight += weight
        student_skill = student_lookup.get(key)

        if student_skill is None:
            missing.append({
                "name": name,
                "current_level": 0,
                "target_level": target,
                "gap": target,
            })
            continue

        current = _normalise(student_skill.get("level", 0))
        contribution = min(current / target, 1.0) * weight
        achieved_weight += contribution
        available_count += 1

        matched.append({
            "name": name,
            "current_level": current,
            "target_level": target,
            "gap": max(0.0, target - current),
            "verified": bool(student_skill.get("verified", False)),
        })

    if total_weight == 0:
        return {
            "score": None,
            "matched_skills": matched,
            "missing_skills": missing,
            "completeness": 0.0,
        }

    return {
        "score": round((achieved_weight / total_weight) * 100, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "completeness": round(
            available_count / len(career_requirements) * 100, 2
        ),
    }


def calculate_career_score(
    student: dict,
    career: dict,
    weights: dict | None = None,
) -> dict:
    """
    Calculate a weighted compatibility score.

    Optional components are excluded and remaining weights are
    rebalanced. Missing information is not silently treated as zero.
    """
    selected_weights = {**DEFAULT_WEIGHTS, **(weights or {})}

    requirements = career.get("required_skills", [])
    skill_result = calculate_skill_score(
        student.get("skills", []),
        requirements,
    )

    components = {}

    if skill_result["score"] is not None:
        components["skills"] = skill_result["score"]

    education_required = career.get("education_level")
    education_actual = student.get("education_level")

    if education_required and education_actual:
        components["education"] = (
            100.0 if str(education_actual).casefold()
            == str(education_required).casefold() else 50.0
        )

    required_interests = {
        str(item).casefold()
        for item in career.get("interests", [])
    }
    student_interests = {
        str(item).casefold()
        for item in student.get("interests", [])
    }

    if required_interests and student_interests:
        components["interests"] = (
            len(required_interests & student_interests)
            / len(required_interests)
        ) * 100

    if skill_result["matched_skills"]:
        verified_count = sum(
            1 for item in skill_result["matched_skills"]
            if item["verified"]
        )
        components["evidence"] = (
            verified_count / len(skill_result["matched_skills"])
        ) * 100

    active_weight = sum(
        max(0.0, float(selected_weights.get(key, 0)))
        for key in components
    )

    if active_weight <= 0:
        overall_score = None
    else:
        overall_score = sum(
            score * max(0.0, float(selected_weights.get(key, 0)))
            for key, score in components.items()
        ) / active_weight

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
        "data_completeness": round(
            sum(
                1 for value in (
                    bool(student.get("skills")),
                    bool(student.get("education_level")),
                    bool(student.get("interests")),
                ) if value
            ) / 3 * 100,
            2,
        ),
    }
