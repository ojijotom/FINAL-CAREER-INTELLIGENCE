"""Rank career options using the deterministic scoring engine."""

from .scoring import calculate_career_score


def match_careers(
    student: dict,
    careers: list[dict],
    limit: int = 10,
) -> list[dict]:
    """Return careers ordered by calculated compatibility."""
    results = [
        calculate_career_score(student, career)
        for career in careers
    ]

    results.sort(
        key=lambda item: (
            item["compatibility_score"] is not None,
            item["compatibility_score"] or 0,
        ),
        reverse=True,
    )

    return results[:max(1, limit)]
