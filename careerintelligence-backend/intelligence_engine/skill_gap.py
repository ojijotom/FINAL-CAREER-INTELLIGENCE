
"""Identify and rank the skills a student needs to improve."""

from .scoring import (
    _normalise_name,
    _prepare_requirements,
    _prepare_student_skills,
)


def analyse_skill_gaps(
    student_skills: list[dict],
    career_requirements: list[dict],
) -> dict:
    """Compare assessed student skills against career target levels.

    Missing or invalid student skill records are reported as not assessed.
    Their estimated learning priority is not presented as a measured gap.
    """

    student_lookup = _prepare_student_skills(student_skills)
    requirements = _prepare_requirements(career_requirements)

    gaps = []

    for requirement in requirements:
        name = requirement["name"]
        key = _normalise_name(name)

        target = requirement["target_level"]
        weight = requirement["weight"]

        current_skill = student_lookup.get(key)

        if current_skill is None:
            # We do not know the student's actual skill level.
            # Therefore, no numerical skill gap can be calculated.
            gaps.append({
                "skill": name,
                "current_level": None,
                "target_level": round(target, 2),
                "gap": None,
                "priority_weight": round(weight, 2),
                "priority_score": None,
                "estimated_priority": round(target * weight, 2),
                "priority_basis": "estimated_not_assessed",
                "verified": False,
                "status": "not_assessed",
            })
            continue

        current = current_skill["level"]
        gap = max(0.0, target - current)

        gaps.append({
            "skill": name,
            "current_level": round(current, 2),
            "target_level": round(target, 2),
            "gap": round(gap, 2),
            "priority_weight": round(weight, 2),
            "priority_score": round(gap * weight, 2),
            "estimated_priority": None,
            "priority_basis": "measured_gap",
            "verified": current_skill["verified"],
            "status": (
                "needs_improvement" if gap > 0
                else "target_reached"
            ),
        })

    # Measured gaps come first, ranked by their weighted gap.
    # Unassessed skills follow, ranked by estimated priority.
    gaps.sort(
        key=lambda item: (
            0 if item["status"] != "not_assessed" else 1,
            -(
                item["priority_score"]
                if item["priority_score"] is not None
                else item["estimated_priority"]
            ),
            item["skill"].casefold(),
        )
    )

    requiring_improvement = sum(
        1 for item in gaps
        if item["status"] == "needs_improvement"
    )

    at_target = sum(
        1 for item in gaps
        if item["status"] == "target_reached"
    )

    not_assessed = sum(
        1 for item in gaps
        if item["status"] == "not_assessed"
    )

    return {
        "total_required_skills": len(gaps),
        "skills_requiring_improvement": requiring_improvement,
        "skills_at_target": at_target,
        "skills_not_assessed": not_assessed,
        "gaps": gaps,
    }
