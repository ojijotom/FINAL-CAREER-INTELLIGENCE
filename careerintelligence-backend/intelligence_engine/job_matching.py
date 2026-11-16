
"""Evaluate and rank student suitability for specific job vacancies."""

from .scoring import (
    _education_score,
    _normalise_name,
    _parse_number,
    _prepare_requirements,
    _prepare_student_skills,
)


DEFAULT_JOB_WEIGHTS = {
    "required_skills": 0.50,
    "preferred_skills": 0.15,
    "education": 0.20,
    "experience": 0.15,
}


def _analyse_job_skills(
    student_skills: list[dict],
    requirements: list[dict],
) -> dict:
    """Evaluate student skills against vacancy requirements."""

    prepared_requirements = _prepare_requirements(requirements)
    student_lookup = _prepare_student_skills(student_skills)

    results = []
    achieved_weight = 0.0
    assessed_weight = 0.0

    for requirement in prepared_requirements:
        name = requirement["name"]
        target = requirement["target_level"]
        weight = requirement["weight"]

        student_skill = student_lookup.get(_normalise_name(name))

        if student_skill is None:
            results.append({
                "skill": name,
                "current_level": None,
                "required_level": target,
                "status": "not_assessed",
                "verified": False,
            })
            continue

        current = student_skill["level"]
        met = current >= target

        achieved_weight += (
            min(current / target, 1.0) * weight
        )
        assessed_weight += weight

        results.append({
            "skill": name,
            "current_level": current,
            "required_level": target,
            "status": "met" if met else "not_met",
            "verified": student_skill["verified"],
        })

    score = None

    if assessed_weight > 0:
        score = round(
            achieved_weight / assessed_weight * 100, 2
        )

    total = len(prepared_requirements)
    assessed = sum(
        1 for item in results
        if item["status"] != "not_assessed"
    )

    return {
        "score": score,
        "total_requirements": total,
        "assessed_requirements": assessed,
        "completeness": (
            round(assessed / total * 100, 2)
            if total else 0.0
        ),
        "met": sum(
            1 for item in results if item["status"] == "met"
        ),
        "not_met": sum(
            1 for item in results if item["status"] == "not_met"
        ),
        "not_assessed": sum(
            1 for item in results
            if item["status"] == "not_assessed"
        ),
        "requirements": results,
    }


def _analyse_experience(
    student: dict,
    job: dict,
) -> dict:
    """Compare documented student experience with vacancy requirements."""

    required = _parse_number(
        job.get("minimum_experience_years")
    )

    if required is None:
        return {
            "score": None,
            "status": "not_required",
            "required_years": None,
            "student_years": None,
        }

    if required < 0:
        return {
            "score": None,
            "status": "invalid_requirement",
            "required_years": required,
            "student_years": None,
        }

    actual = _parse_number(
        student.get("experience_years")
    )

    if actual is None or actual < 0:
        return {
            "score": None,
            "status": "not_assessed",
            "required_years": required,
            "student_years": None,
        }

    score = (
        100.0 if required == 0
        else min(actual / required, 1.0) * 100
    )

    return {
        "score": round(score, 2),
        "status": "met" if actual >= required else "not_met",
        "required_years": required,
        "student_years": actual,
    }


def _mandatory_status(
    required_skills: dict,
    education: dict,
    experience: dict,
) -> str:
    """Determine whether the listed mandatory criteria are met."""

    statuses = []

    for item in required_skills["requirements"]:
        statuses.append(item["status"])

    if education["status"] not in ("not_required",):
        statuses.append(education["status"])

    if experience["status"] not in ("not_required",):
        statuses.append(experience["status"])

    if "not_met" in statuses:
        return "not_met"

    if "not_assessed" in statuses or "invalid_requirement" in statuses:
        return "not_assessed"

    return "met"


def calculate_job_suitability(
    student: dict,
    job: dict,
    weights: dict | None = None,
) -> dict:
    """Calculate explainable suitability for one specific vacancy.

    Expected vacancy structure:

        {
            "id": 1,
            "title": "Junior Data Analyst",
            "company": "Example Company",
            "required_skills": [
                {"name": "SQL", "target_level": 80, "weight": 2}
            ],
            "preferred_skills": [
                {"name": "Python", "target_level": 70}
            ],
            "education_level": "bachelor",
            "minimum_experience_years": 1
        }

    Student experience_years and skill levels must be documented.
    Missing information is not treated as zero.
    """

    student = student if isinstance(student, dict) else {}
    job = job if isinstance(job, dict) else {}

    required_skills = job.get("required_skills", [])
    preferred_skills = job.get("preferred_skills", [])

    if not isinstance(required_skills, list):
        required_skills = []

    if not isinstance(preferred_skills, list):
        preferred_skills = []

    student_skills = student.get("skills", [])

    if not isinstance(student_skills, list):
        student_skills = []

    required_result = _analyse_job_skills(
        student_skills,
        required_skills,
    )

    preferred_result = _analyse_job_skills(
        student_skills,
        preferred_skills,
    )

    education_required = job.get("education_level")
    education_actual = student.get("education_level")

    if not education_required:
        education_result = {
            "score": None,
            "status": "not_required",
            "required_level": None,
            "student_level": None,
        }
    else:
        education_score = _education_score(
            education_actual,
            education_required,
        )

        education_status = (
            "not_assessed" if education_score is None
            else "met" if education_score == 100
            else "not_met"
        )

        education_result = {
            "score": education_score,
            "status": education_status,
            "required_level": education_required,
            "student_level": education_actual,
        }

    experience_result = _analyse_experience(student, job)

    components = {}

    if required_result["score"] is not None:
        components["required_skills"] = required_result["score"]

    if preferred_result["score"] is not None:
        components["preferred_skills"] = preferred_result["score"]

    if education_result["score"] is not None:
        components["education"] = education_result["score"]

    if experience_result["score"] is not None:
        components["experience"] = experience_result["score"]

    selected_weights = {
        **DEFAULT_JOB_WEIGHTS,
        **(weights or {}),
    }

    valid_weights = {}

    for component in components:
        weight = _parse_number(
            selected_weights.get(component)
        )

        if weight is not None and weight > 0:
            valid_weights[component] = weight

    active_weight = sum(valid_weights.values())

    suitability_score = None

    if active_weight > 0:
        suitability_score = sum(
            components[key] * weight
            for key, weight in valid_weights.items()
        ) / active_weight

    mandatory_status = _mandatory_status(
        required_result,
        education_result,
        experience_result,
    )

    return {
        "job_id": job.get("id"),
        "job_title": job.get("title", "Unnamed vacancy"),
        "company": job.get("company"),
        "suitability_score": (
            round(suitability_score, 2)
            if suitability_score is not None else None
        ),
        "components": {
            key: round(value, 2)
            for key, value in components.items()
        },
        "required_skills_analysis": required_result,
        "preferred_skills_analysis": preferred_result,
        "education_analysis": education_result,
        "experience_analysis": experience_result,
        "mandatory_requirements_status": mandatory_status,
        "eligibility_status": {
            "met": "meets_listed_mandatory_requirements",
            "not_met": "does_not_meet_listed_mandatory_requirements",
            "not_assessed": "pending_assessment",
        }[mandatory_status],
    }


def match_jobs(
    student: dict,
    jobs: list[dict],
    limit: int = 10,
) -> list[dict]:
    """Rank vacancies by mandatory criteria and suitability score."""

    if not isinstance(student, dict):
        student = {}

    if not isinstance(jobs, list):
        return []

    results = [
        calculate_job_suitability(student, job)
        for job in jobs
        if isinstance(job, dict)
    ]

    status_priority = {
        "met": 0,
        "not_assessed": 1,
        "not_met": 2,
    }

    results.sort(
        key=lambda item: (
            status_priority[item["mandatory_requirements_status"]],
            item["suitability_score"] is None,
            -(item["suitability_score"] or 0),
        )
    )

    if isinstance(limit, bool):
        limit = 10

    try:
        limit = max(1, min(int(limit), 100))
    except (TypeError, ValueError, OverflowError):
        limit = 10

    return results[:limit]
