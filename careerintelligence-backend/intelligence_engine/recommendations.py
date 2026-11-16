
"""Generate practical learning actions from identified skill gaps."""


DEFAULT_LEARNING_RESOURCES = {
    "python": [
        "Practise Python fundamentals and build a small application.",
        "Study functions, data structures, file handling and error handling.",
    ],
    "sql": [
        "Practise SELECT, JOIN, GROUP BY and database design.",
        "Work with a relational database and write increasingly complex queries.",
    ],
    "javascript": [
        "Build interactive web pages using JavaScript.",
        "Practise DOM manipulation, events, asynchronous code and APIs.",
    ],
    "statistics": [
        "Practise descriptive statistics and interpreting datasets.",
        "Study probability, distributions and basic statistical inference.",
    ],
    "excel": [
        "Practise formulas, pivot tables and data cleaning.",
        "Analyse a real dataset and create a clear spreadsheet report.",
    ],
    "communication": [
        "Practise technical presentations and written explanations.",
        "Explain a technical project to someone without a technical background.",
    ],
}


def _normalise_limit(value: int) -> int:
    """Validate the maximum number of recommendations."""
    if isinstance(value, bool):
        return 10

    try:
        limit = int(value)
    except (TypeError, ValueError, OverflowError):
        return 10

    return max(1, min(limit, 50))


def _learning_resources(skill_name: str) -> list[str]:
    """Return learning actions for a particular skill."""
    return DEFAULT_LEARNING_RESOURCES.get(
        skill_name.strip().casefold(),
        [
            f"Study the fundamentals of {skill_name} and practise "
            f"with a small practical exercise.",
            f"Find a structured learning resource for {skill_name} "
            f"and apply what you learn.",
        ],
    )


def generate_learning_recommendations(
    skill_gap_result: dict,
    max_recommendations: int = 10,
) -> list[dict]:
    """Create learning suggestions from measured and unassessed skills.

    Measured gaps receive learning actions.
    Unassessed skills receive assessment suggestions.
    Skills already at target are excluded.
    """
    if not isinstance(skill_gap_result, dict):
        return []

    limit = _normalise_limit(max_recommendations)

    gaps = skill_gap_result.get("gaps", [])

    if not isinstance(gaps, list):
        return []

    recommendations = []

    for item in gaps:
        if not isinstance(item, dict):
            continue

        skill_name = item.get("skill")

        if not isinstance(skill_name, str) or not skill_name.strip():
            continue

        skill_name = skill_name.strip()
        status = item.get("status")

        if status == "not_assessed":
            recommendations.append({
                "skill": skill_name,
                "recommendation_type": "assessment",
                "priority": item.get("estimated_priority"),
                "priority_basis": "estimated_not_assessed",
                "current_level": None,
                "target_level": item.get("target_level"),
                "actions": [
                    f"Complete a short assessment of your current {skill_name} ability.",
                    f"Try a practical {skill_name} exercise to demonstrate your current ability.",
                ],
                "suggested_project": (
                    f"Complete a beginner-friendly practical exercise "
                    f"using {skill_name} to establish your current level."
                ),
                "explanation": (
                    "Your current level has not yet been assessed. "
                    "Complete an assessment before a measured skill gap "
                    "or learning requirement is assigned."
                ),
            })
            continue

        if status == "target_reached":
            continue

        if status != "needs_improvement":
            continue

        gap = item.get("gap")
        priority = item.get("priority_score")

        # Reject malformed or non-positive measured gaps.
        if (
            isinstance(gap, bool)
            or not isinstance(gap, (int, float))
            or gap <= 0
        ):
            continue

        if (
            isinstance(priority, bool)
            or not isinstance(priority, (int, float))
        ):
            priority = gap * item.get("priority_weight", 1)

        recommendations.append({
            "skill": skill_name,
            "recommendation_type": "learning",
            "priority": round(priority, 2),
            "priority_basis": "measured_gap",
            "current_level": item.get("current_level"),
            "target_level": item.get("target_level"),
            "actions": _learning_resources(skill_name),
            "suggested_project": (
                f"Build a practical project demonstrating {skill_name}."
            ),
            "explanation": (
                f"Your assessed {skill_name} level is below the "
                f"required target. Focus on the learning actions "
                f"and practise through a practical project."
            ),
        })

    # Measured learning gaps should appear before assessment suggestions.
    recommendations.sort(
        key=lambda item: (
            0 if item["recommendation_type"] == "learning" else 1,
            -(
                item["priority"]
                if isinstance(item["priority"], (int, float))
                else 0
            ),
            item["skill"].casefold(),
        )
    )

    return recommendations[:limit]
