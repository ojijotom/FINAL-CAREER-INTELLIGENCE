from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import (
    Career,
    CareerSkillRequirement,
    Skill,
    StudentProfile,
    StudentSkill,
    UserProfile,
)

from intelligence_engine.ai_service import AIGenerationError


User = get_user_model()


class StudentCareerGuidanceTests(TestCase):
    """Tests for the student AI career-guidance endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("student_career_guidance")

        self.student_user = User.objects.create_user(
            username="guidance_student",
            email="guidance@example.com",
            password="CareerTest@2026Secure",
        )

        self.student_user.career_profile = UserProfile.objects.create(
            user=self.student_user,
            role=UserProfile.Role.STUDENT,
        )

        self.student = StudentProfile.objects.create(
            user_profile=self.student_user.career_profile,
            programme="Computer Science",
            education_level="Undergraduate",
        )

        self.employer_user = User.objects.create_user(
            username="guidance_employer",
            email="employer-guidance@example.com",
            password="CareerTest@2026Secure",
        )

        UserProfile.objects.create(
            user=self.employer_user,
            role=UserProfile.Role.EMPLOYER,
        )

    def create_career(self):
        skill = Skill.objects.create(name="Python")

        career = Career.objects.create(
            title="Software Developer",
            industry="Technology",
            description="Develops software applications.",
            education_level="Undergraduate",
            is_active=True,
        )

        CareerSkillRequirement.objects.create(
            career=career,
            skill=skill,
            target_level=80,
            weight=1.0,
        )

        StudentSkill.objects.create(
            student=self.student,
            skill=skill,
            level=70,
        )

        return career

    def test_unauthenticated_user_cannot_access_guidance(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_employer_cannot_access_student_guidance(self):
        self.client.force_authenticate(user=self.employer_user)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    @patch("api.career_guidance.generate_guidance")
    @patch("api.career_guidance.generate_learning_recommendations")
    @patch("api.career_guidance.analyse_skill_gaps")
    @patch("api.career_guidance.match_careers")
    @patch("api.career_guidance.is_ai_configured", return_value=True)
    def test_student_receives_guidance_and_python_score_is_preserved(
        self,
        mock_configured,
        mock_match,
        mock_gaps,
        mock_recommendations,
        mock_generate,
    ):
        self.client.force_authenticate(user=self.student_user)

        career = self.create_career()

        expected_score = 87.5

        mock_match.return_value = [
            {
                "career_id": career.pk,
                "career_title": career.title,
                "compatibility_score": expected_score,
                "components": {"skills": 87.5},
            }
        ]

        mock_gaps.return_value = {
            "gaps": [],
            "summary": {"total_gaps": 0},
        }

        mock_recommendations.return_value = []

        mock_generate.return_value = (
            "Your skills provide a good foundation for software development."
        )

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["career_results"][0]["compatibility_score"],
            expected_score,
        )

        self.assertEqual(
            response.data["guidance"],
            "Your skills provide a good foundation for software development.",
        )

        self.assertEqual(
            response.data["career_results"][0]["career_title"],
            "Software Developer",
        )

        mock_match.assert_called_once()
        mock_generate.assert_called_once()

    @patch("api.career_guidance.generate_guidance")
    @patch("api.career_guidance.is_ai_configured", return_value=False)
    def test_unconfigured_ai_returns_service_unavailable(
        self,
        mock_configured,
        mock_generate,
    ):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

        mock_generate.assert_not_called()

    @patch("api.career_guidance.generate_guidance")
    @patch("api.career_guidance.is_ai_configured", return_value=True)
    def test_no_active_careers_returns_service_unavailable(
        self,
        mock_configured,
        mock_generate,
    ):
        self.client.force_authenticate(user=self.student_user)

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

        mock_generate.assert_not_called()

    @patch(
        "api.career_guidance.generate_guidance",
        side_effect=AIGenerationError("Provider unavailable"),
    )
    @patch("api.career_guidance.generate_learning_recommendations")
    @patch("api.career_guidance.analyse_skill_gaps")
    @patch(
        "api.career_guidance.match_careers",
        return_value=[
            {
                "career_id": 1,
                "career_title": "Software Developer",
                "compatibility_score": 80.0,
            }
        ],
    )
    @patch("api.career_guidance.is_ai_configured", return_value=True)
    def test_ai_generation_failure_returns_bad_gateway(
        self,
        mock_configured,
        mock_match,
        mock_gaps,
        mock_recommendations,
        mock_generate,
    ):
        self.client.force_authenticate(user=self.student_user)

        career = self.create_career()

        mock_match.return_value = [
            {
                "career_id": career.pk,
                "career_title": career.title,
                "compatibility_score": 80.0,
            }
        ]

        mock_gaps.return_value = {"gaps": []}
        mock_recommendations.return_value = []

        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_502_BAD_GATEWAY,
        )

        self.assertIn("detail", response.data)
        self.assertNotIn("Provider unavailable", str(response.data))
