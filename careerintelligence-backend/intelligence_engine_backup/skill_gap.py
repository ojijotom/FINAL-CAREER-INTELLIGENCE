"""Identify and rank the skills a student needs to improve."""


def analyse_skill_gaps(
    student_skills: list[dict],
    career_requirements: list[dict],
) -> dict:
    """Compare current skill levels against career target levels."""
    student_lookup = {
        str(skill.get("name", "")).strip().casefold(): skill
        for skill in student_skills
        if skill.get("name")
    }

    gaps = []

    for requirement in career_requirements:
        name = str(requirement.get("name", "")).strip()

        if not name:
            continue

        try:
            target = max(0.0, float(requirement.get("target_level", 100)))
            weight = max(0.0, float(requirement.get("weight", 1)))
        except (TypeError, ValueError):
            continue

        current_skill = student_lookup.get(name.casefold())
        current = (
            float(current_skill.get("level", 0))
            if current_skill else 0.0
        )
        current = max(0.0, min(current, 100.0))
        gap = max(0.0, target - current)

        gaps.append({
            "skill": name,
            "current_level": round(current, 2),
            "target_level": round(target, 2),
            "gap": round(gap, 2),
            "priority_weight": weight,
            "verified": (
                bool(current_skill.get("verified", False))
                if current_skill else False
            ),
            "status": (
                "missing" if current_skill is None
                else "needs_improvement" if gap > 0
                else "target_reached"
            ),
        })

    gaps.sort(
        key=lambda item: (
            item["gap"] * item["priority_weight"]
        ),
        reverse=True,
    )

    return {
        "total_required_skills": len(gaps),
        "skills_requiring_improvement": sum(
            1 for item in gaps if item["gap"] > 0
        ),
        "skills_at_target": sum(
            1 for item in gaps if item["gap"] == 0
        ),
        "gaps": gaps,
    }
