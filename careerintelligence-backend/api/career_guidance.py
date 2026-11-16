"""Student career guidance API powered by deterministic scoring and OpenAI."""

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Career, StudentProfile, StudentSkill
from .permissions import IsStudent

from intelligence_engine.ai_service import (
    AIConfigurationError,
    AIGenerationError,
    generate_guidance,
    is_ai_configured,
)
from intelligence_engine.career_matching import match_careers
from intelligence_engine.prompts import build_career_guidance_prompt
from intelligence_engine.recommendations import generate_learning_recommendations
from intelligence_engine.skill_gap import analyse_skill_gaps


class StudentCareerGuidanceView(APIView):
    """
    Generate personalised career guidance for the authenticated student.

    Career compatibility is calculated by the Python engine.
    OpenAI only explains the calculated results.
    """

    permission_classes = [IsStudent]

    def post(self, request):
        if not is_ai_configured():
            return Response(
                {"detail": "AI guidance is not configured on the server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        student_profile = get_object_or_404(
            StudentProfile.objects.select_related("user_profile"),
            user_profile__user=request.user,
        )

        skill_records = list(
            StudentSkill.objects.filter(
                student=student_profile
            ).select_related("skill").order_by("skill__name")
        )

        student_skills = [
            {
                "name": record.skill.name,
                "level": record.level,
                "verified": record.verified,
                "source": record.source,
            }
            for record in skill_records
        ]

        student_data = {
            "education_level": student_profile.education_level,
            "interests": student_profile.interests or [],
            "skills": student_skills,
        }

        careers = Career.objects.filter(
            is_active=True
        ).prefetch_related(
            "skill_requirements__skill"
        ).order_by("title")

        career_inputs = []
        career_details = {}

        for career in careers:
            requirements = [
                {
                    "name": requirement.skill.name,
                    "target_level": requirement.target_level,
                    "weight": float(requirement.weight),
                }
                for requirement in career.skill_requirements.all()
            ]

            career_data = {
                "id": career.pk,
                "title": career.title,
                "industry": career.industry,
                "description": career.description,
                "education_level": career.education_level,
                "required_skills": requirements,
            }

            career_inputs.append(career_data)
            career_details[career.pk] = career_data

        if not career_inputs:
            return Response(
                {"detail": "The career catalogue has no active careers yet."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Python calculates and ranks the compatibility scores.
        calculated_results = match_careers(
            student_data,
            career_inputs,
            limit=10,
        )

        enriched_results = []

        for result in calculated_results:
            career = career_details[result["career_id"]]

            gaps = analyse_skill_gaps(
                student_skills,
                career["required_skills"],
            )

            recommendations = generate_learning_recommendations(
                gaps,
                max_recommendations=10,
            )

            enriched_results.append({
                **result,
                "industry": career["industry"],
                "description": career["description"],
                "skill_gaps": gaps,
                "learning_recommendations": recommendations,
            })

        student_summary = {
            "programme": student_profile.programme,
            "education_level": student_profile.education_level,
            "graduation_year": student_profile.graduation_year,
            "experience_years": (
                str(student_profile.experience_years)
                if student_profile.experience_years is not None
                else None
            ),
            "interests": student_profile.interests or [],
            "skills": student_skills,
        }

        prompt = build_career_guidance_prompt(
            student_summary,
            enriched_results,
        )

        try:
            guidance = generate_guidance(prompt)

        except AIConfigurationError:
            return Response(
                {"detail": "AI guidance is not configured on the server."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except AIGenerationError:
            return Response(
                {
                    "detail": (
                        "Career guidance could not be generated right now. "
                        "Please try again later."
                    )
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {
                "student_summary": student_summary,
                "career_results": enriched_results,
                "guidance": guidance,
            },
            status=status.HTTP_200_OK,
        )
