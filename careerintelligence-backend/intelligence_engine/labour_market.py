
"""Analyse employer-posted vacancies for labour-market demand.

This module analyses only the vacancy records supplied to it.
It does not claim that platform data represents the entire labour market.
"""

from collections import defaultdict
from datetime import date, datetime
from typing import Any


ACTIVE_STATUSES = {"active", "open", "published"}
EXCLUDED_STATUSES = {
    "closed",
    "expired",
    "cancelled",
    "canceled",
    "draft",
    "paused",
    "inactive",
}


def _normalise(value: Any) -> str:
    """Return a consistent, lowercase text value."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().lower().split())


def _display(value: Any) -> str:
    """Return cleaned display text."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.strip().split())


def _parse_date(value: Any) -> date | None:
    """Accept date, datetime, or ISO date strings."""
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if isinstance(value, str) and value.strip():
        try:
            return date.fromisoformat(value.strip()[:10])
        except ValueError:
            return None

    return None


def _as_of(value: Any = None) -> date:
    """Resolve the date used to determine current vacancy status."""
    if value is None:
        return date.today()

    parsed = _parse_date(value)
    if parsed is None:
        raise ValueError("as_of_date must be a valid date or ISO date string.")

    return parsed


def _extract_skills(items: Any) -> dict[str, str]:
    """Return unique skills keyed by normalised name."""
    result = {}

    if not isinstance(items, list):
        return result

    for item in items:
        if isinstance(item, str):
            name = _display(item)
        elif isinstance(item, dict):
            name = _display(item.get("name"))
        else:
            continue

        key = _normalise(name)
        if key and key not in result:
            result[key] = name

    return result


def _employer_key(vacancy: dict) -> str:
    """Identify an employer using its ID or name."""
    employer_id = vacancy.get("employer_id")

    if employer_id is not None and str(employer_id).strip():
        return f"id:{str(employer_id).strip()}"

    employer = _normalise(
        vacancy.get("company") or vacancy.get("employer")
    )

    return f"name:{employer}" if employer else ""


def _vacancy_is_active(vacancy: dict, today: date) -> tuple[bool, str]:
    """Determine whether a vacancy qualifies as currently active."""
    status = _normalise(vacancy.get("status"))

    if status in EXCLUDED_STATUSES:
        return False, status

    if status not in ACTIVE_STATUSES:
        return False, "unknown_or_missing_status"

    closing_date_value = vacancy.get("closing_date")

    if closing_date_value:
        closing_date = _parse_date(closing_date_value)

        if closing_date is None:
            return False, "invalid_closing_date"

        if closing_date < today:
            return False, "expired_by_closing_date"

    posted_date_value = vacancy.get("posted_date")

    if posted_date_value:
        posted_date = _parse_date(posted_date_value)

        if posted_date is None:
            return False, "invalid_posted_date"

        if posted_date > today:
            return False, "not_yet_posted"

    return True, "active"


def _aggregate_dimensions(
    records: list[tuple[str, str, str]],
) -> list[dict]:
    """Aggregate vacancy and employer counts by a dimension."""
    grouped = defaultdict(lambda: {
        "name": "",
        "vacancy_ids": set(),
        "employers": set(),
    })

    for name, vacancy_id, employer in records:
        key = _normalise(name)
        if not key:
            continue

        group = grouped[key]
        group["name"] = group["name"] or name
        group["vacancy_ids"].add(vacancy_id)

        if employer:
            group["employers"].add(employer)

    results = []

    for group in grouped.values():
        results.append({
            "name": group["name"],
            "vacancy_count": len(group["vacancy_ids"]),
            "employer_count": len(group["employers"]),
        })

    results.sort(
        key=lambda item: (
            item["vacancy_count"],
            item["employer_count"],
            item["name"].lower(),
        ),
        reverse=True,
    )

    return results


def analyse_labour_market(
    vacancies: list[dict],
    as_of_date: Any = None,
) -> dict:
    """Analyse skills, industries and locations in active vacancies."""
    if not isinstance(vacancies, list):
        raise ValueError("vacancies must be a list.")

    today = _as_of(as_of_date)

    active_vacancies = []
    excluded_counts = defaultdict(int)

    for index, vacancy in enumerate(vacancies):
        if not isinstance(vacancy, dict):
            excluded_counts["invalid_vacancy_record"] += 1
            continue

        is_active, reason = _vacancy_is_active(vacancy, today)

        if not is_active:
            excluded_counts[reason] += 1
            continue

        # Use a stable fallback identifier for records without database IDs.
        vacancy_id = str(vacancy.get("id", f"record-{index}"))

        active_vacancies.append({
            "id": vacancy_id,
            "employer": _employer_key(vacancy),
            "required_skills": _extract_skills(
                vacancy.get("required_skills")
            ),
            "preferred_skills": _extract_skills(
                vacancy.get("preferred_skills")
            ),
            "industry": _display(vacancy.get("industry")),
            "location": _display(vacancy.get("location")),
        })

    skill_groups = defaultdict(lambda: {
        "name": "",
        "required_vacancies": set(),
        "preferred_vacancies": set(),
        "required_employers": set(),
        "preferred_employers": set(),
    })

    industry_records = []
    location_records = []

    for vacancy in active_vacancies:
        vacancy_id = vacancy["id"]
        employer = vacancy["employer"]

        for key, name in vacancy["required_skills"].items():
            group = skill_groups[key]
            group["name"] = group["name"] or name
            group["required_vacancies"].add(vacancy_id)

            if employer:
                group["required_employers"].add(employer)

        for key, name in vacancy["preferred_skills"].items():
            group = skill_groups[key]
            group["name"] = group["name"] or name
            group["preferred_vacancies"].add(vacancy_id)

            if employer:
                group["preferred_employers"].add(employer)

        if vacancy["industry"]:
            industry_records.append((
                vacancy["industry"], vacancy_id, employer
            ))

        if vacancy["location"]:
            location_records.append((
                vacancy["location"], vacancy_id, employer
            ))

    skill_results = []

    for group in skill_groups.values():
        required_ids = group["required_vacancies"]
        preferred_ids = group["preferred_vacancies"]
        all_ids = required_ids | preferred_ids

        skill_results.append({
            "skill": group["name"],
            "required_vacancy_count": len(required_ids),
            "preferred_vacancy_count": len(preferred_ids),
            "total_vacancy_count": len(all_ids),
            "required_employer_count": len(
                group["required_employers"]
            ),
            "preferred_employer_count": len(
                group["preferred_employers"]
            ),
        })

    skill_results.sort(
        key=lambda item: (
            item["required_vacancy_count"],
            item["total_vacancy_count"],
            item["required_employer_count"],
            item["skill"].lower(),
        ),
        reverse=True,
    )

    employer_ids = {
        vacancy["employer"]
        for vacancy in active_vacancies
        if vacancy["employer"]
    }

    return {
        "report_date": today.isoformat(),
        "data_scope": "platform_employer_posted_vacancies",
        "coverage_note": (
            "This report describes only the supplied platform vacancy "
            "records. It must not be interpreted as a complete national "
            "or regional labour-market estimate."
        ),
        "summary": {
            "total_records_received": len(vacancies),
            "active_vacancies_analysed": len(active_vacancies),
            "excluded_records": sum(excluded_counts.values()),
            "distinct_employers": len(employer_ids),
            "distinct_skills": len(skill_results),
        },
        "exclusion_breakdown": dict(excluded_counts),
        "skill_demand": skill_results,
        "industry_demand": _aggregate_dimensions(industry_records),
        "location_demand": _aggregate_dimensions(location_records),
    }
