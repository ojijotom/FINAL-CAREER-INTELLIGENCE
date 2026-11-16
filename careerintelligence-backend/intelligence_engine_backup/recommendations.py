"""Generate practical learning actions from identified skill gaps."""


DEFAULT_LEARNING_RESOURCES = {
    "python": [
        "Practise Python fundamentals and build a small application."
    ],
    "sql": [
        "Practise SELECT, JOIN, GROUP BY and database design."
    ],
    "javascript": [
        "Build interactive web pages using JavaScript."
    ],
    "statistics": [
        "Practise descriptive statistics and interpreting datasets."
    ],
    "excel": [
        "Practise formulas, pivot tables and data cleaning."
    ],
    "communication": [
        "Practise technical presentations and written explanations."
    ],
}


def generate_learning_recommendations(
    skill_gap_result: dict,
    max_recommendations: int = 10,
) -> list[dict]:
    """Create learning suggestions ordered by skill-gap priority."""
    recommendations = []

    for item in skill_gap_result.get("gaps", []):
        if item.get("gap", 0) <= 0:
            continue

        skill_name = item["skill"]
        resources = DEFAULT_LEARNING_RESOURCES.get(
            skill_name.casefold(),
            [
                f"Study the fundamentals of {skill_name} and practise "
                f"with a small practical project."
            ],
        )

        recommendations.append({
            "skill": skill_name,
            "priority": item.get("priority_weight", 1) * item["gap"],
            "current_level": item["current_level"],
            "target_level": item["target_level"],
            "actions": resources,
            "suggested_project": (
                f"Build a practical project demonstrating {skill_name}."
            ),
        })

    return recommendations[:max(1, max_recommendations)]
