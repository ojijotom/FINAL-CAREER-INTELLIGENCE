from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from rest_framework import status

from .models import (
    UserProfile,
    StudentProfile,
    EmployerProfile,
    UniversityProfile,
    Skill,
    StudentSkill,
    Vacancy,
    VacancySkill,
    JobApplication,
    StudentDocument,
    IntelligenceAnalysis,
)
from types import SimpleNamespace
from django.contrib.auth.models import AnonymousUser

from .permissions import (
    IsStudent,
    IsEmployer,
    IsUniversity,
    IsStudentOrUniversity,
    IsCareerAdmin,
    IsStudentRecordOwner,
    IsEmployerRecordOwner,
    IsUniversityRecordOwner,
)
import io
import tempfile
import zipfile

from pathlib import Path

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from .models import StudentDocument
User = get_user_model()


class AuthenticationAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"
        self.refresh_url = "/api/auth/token/refresh/"
        self.me_url = "/api/auth/me/"

        self.password = "CareerTest@2026Secure"

    def register_user(self, role="student", username="teststudent"):
        data = {
            "username": username,
            "email": f"{username}@example.com",
            "password": self.password,
            "password_confirm": self.password,
            "first_name": "Test",
            "last_name": "User",
            "role": role,
            "phone_number": "0700000000",
        }

        if role == "employer":
            data["company_name"] = "Test Technologies"

        elif role == "university":
            data["institution_name"] = "Test University"

        return self.client.post(
            self.register_url,
            data,
            format="json",
        )

    def test_student_registration(self):
        response = self.register_user()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(username="teststudent")

        self.assertTrue(user.check_password(self.password))
        self.assertTrue(
            hasattr(user.career_profile, "student_profile")
        )
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_employer_registration(self):
        response = self.register_user(
            role="employer",
            username="testemployer",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(username="testemployer")

        self.assertEqual(
            user.career_profile.role,
            UserProfile.Role.EMPLOYER,
        )

        self.assertFalse(
            user.career_profile.employer_profile.is_verified
        )

    def test_university_registration(self):
        response = self.register_user(
            role="university",
            username="testuniversity",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = User.objects.get(username="testuniversity")

        self.assertEqual(
            user.career_profile.role,
            UserProfile.Role.UNIVERSITY,
        )

        self.assertFalse(
            user.career_profile.university_profile.is_verified
        )

    def test_passwords_must_match(self):
        data = {
            "username": "mismatchuser",
            "email": "mismatch@example.com",
            "password": self.password,
            "password_confirm": "DifferentPassword@2026",
            "role": "student",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            User.objects.filter(username="mismatchuser").exists()
        )

    def test_duplicate_email_is_rejected(self):
        self.register_user()

        response = self.client.post(
            self.register_url,
            {
                "username": "anotherstudent",
                "email": "TESTSTUDENT@example.com",
                "password": self.password,
                "password_confirm": self.password,
                "role": "student",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_returns_tokens(self):
        self.register_user()

        response = self.client.post(
            self.login_url,
            {
                "username": "teststudent",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_authenticated_user_can_access_profile(self):
        registration = self.register_user()

        access_token = registration.data["tokens"]["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["role"],
            "student",
        )

    def test_unauthenticated_user_cannot_access_profile(self):
        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token_returns_new_access_token(self):
        registration = self.register_user()

        refresh_token = registration.data["tokens"]["refresh"]

        response = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)

class RolePermissionTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username="permission_student",
            password="TestPassword@2026",
        )
        UserProfile.objects.create(
            user=self.student,
            role=UserProfile.Role.STUDENT,
        )

        self.employer = User.objects.create_user(
            username="permission_employer",
            password="TestPassword@2026",
        )
        UserProfile.objects.create(
            user=self.employer,
            role=UserProfile.Role.EMPLOYER,
        )

        self.university = User.objects.create_user(
            username="permission_university",
            password="TestPassword@2026",
        )
        UserProfile.objects.create(
            user=self.university,
            role=UserProfile.Role.UNIVERSITY,
        )

    def check_permission(self, permission_class, user):
        request = SimpleNamespace(user=user)
        return permission_class().has_permission(request, None)

    def test_student_access_is_role_restricted(self):
        self.assertTrue(
            self.check_permission(IsStudent, self.student)
        )
        self.assertFalse(
            self.check_permission(IsStudent, self.employer)
        )

    def test_employer_access_is_role_restricted(self):
        self.assertTrue(
            self.check_permission(IsEmployer, self.employer)
        )
        self.assertFalse(
            self.check_permission(IsEmployer, self.student)
        )

    def test_university_access_is_role_restricted(self):
        self.assertTrue(
            self.check_permission(IsUniversity, self.university)
        )
        self.assertFalse(
            self.check_permission(IsUniversity, self.employer)
        )

    def test_combined_student_university_permission(self):
        self.assertTrue(
            self.check_permission(
                IsStudentOrUniversity,
                self.student,
            )
        )
        self.assertTrue(
            self.check_permission(
                IsStudentOrUniversity,
                self.university,
            )
        )
        self.assertFalse(
            self.check_permission(
                IsStudentOrUniversity,
                self.employer,
            )
        )

    def test_admin_permission_requires_staff_account(self):
        admin = User.objects.create_user(
            username="permission_admin",
            password="TestPassword@2026",
            is_staff=True,
        )

        self.assertTrue(
            self.check_permission(IsCareerAdmin, admin)
        )
        self.assertFalse(
            self.check_permission(IsCareerAdmin, self.student)
        )

    def test_user_without_profile_is_denied(self):
        user = User.objects.create_user(
            username="no_profile",
            password="TestPassword@2026",
        )

        self.assertFalse(
            self.check_permission(IsStudent, user)
        )

    def test_anonymous_user_is_denied(self):
        self.assertFalse(
            self.check_permission(IsStudent, AnonymousUser())
        )

class RecordOwnershipTests(TestCase):

    def setUp(self):
        self.student_user = self.create_user(
            "owner_student", UserProfile.Role.STUDENT
        )
        self.other_student_user = self.create_user(
            "other_student", UserProfile.Role.STUDENT
        )

        self.employer_user = self.create_user(
            "owner_employer", UserProfile.Role.EMPLOYER
        )
        self.other_employer_user = self.create_user(
            "other_employer", UserProfile.Role.EMPLOYER
        )

        self.university_user = self.create_user(
            "owner_university", UserProfile.Role.UNIVERSITY
        )
        self.other_university_user = self.create_user(
            "other_university", UserProfile.Role.UNIVERSITY
        )

        self.university = UniversityProfile.objects.create(
            user_profile=self.university_user.career_profile,
            institution_name="University One",
        )

        self.other_university = UniversityProfile.objects.create(
            user_profile=self.other_university_user.career_profile,
            institution_name="University Two",
        )

        self.student = StudentProfile.objects.create(
            user_profile=self.student_user.career_profile,
            university=self.university,
        )

        self.other_student = StudentProfile.objects.create(
            user_profile=self.other_student_user.career_profile,
            university=self.other_university,
        )

        self.employer = EmployerProfile.objects.create(
            user_profile=self.employer_user.career_profile,
            company_name="Company One",
        )

        self.other_employer = EmployerProfile.objects.create(
            user_profile=self.other_employer_user.career_profile,
            company_name="Company Two",
        )

        self.skill = Skill.objects.create(name="Python")

        self.student_skill = StudentSkill.objects.create(
            student=self.student,
            skill=self.skill,
            level=70,
        )

        self.other_student_skill = StudentSkill.objects.create(
            student=self.other_student,
            skill=self.skill,
            level=50,
        )

        self.vacancy = Vacancy.objects.create(
            employer=self.employer,
            title="Python Developer",
            description="Python development position.",
        )

        self.other_vacancy = Vacancy.objects.create(
            employer=self.other_employer,
            title="Junior Developer",
            description="Junior development position.",
        )

        self.vacancy_skill = VacancySkill.objects.create(
            vacancy=self.vacancy,
            skill=self.skill,
            target_level=80,
        )

        self.application = JobApplication.objects.create(
            student=self.student,
            vacancy=self.vacancy,
        )

        self.other_application = JobApplication.objects.create(
            student=self.other_student,
            vacancy=self.other_vacancy,
        )

        self.document = StudentDocument.objects.create(
            student=self.student,
            document_type=StudentDocument.DocumentType.CV,
            original_filename="student_cv.pdf",
            storage_key="documents/student_cv.pdf",
        )

        self.other_document = StudentDocument.objects.create(
            student=self.other_student,
            document_type=StudentDocument.DocumentType.CV,
            original_filename="other_cv.pdf",
            storage_key="documents/other_cv.pdf",
        )

        self.analysis = IntelligenceAnalysis.objects.create(
            analysis_type=IntelligenceAnalysis.AnalysisType.CAREER_MATCH,
            student=self.student,
            created_by=self.student_user,
        )

        self.other_analysis = IntelligenceAnalysis.objects.create(
            analysis_type=IntelligenceAnalysis.AnalysisType.CAREER_MATCH,
            student=self.other_student,
            created_by=self.other_student_user,
        )

    def create_user(self, username, role):
        user = User.objects.create_user(
            username=username,
            password="TestPassword@2026",
        )

        UserProfile.objects.create(
            user=user,
            role=role,
        )

        return user

    def can_access(self, permission_class, user, obj):
        request = SimpleNamespace(user=user)

        return permission_class().has_object_permission(
            request,
            None,
            obj,
        )

    def test_student_can_access_own_records(self):
        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.student
            )
        )
        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.student_skill
            )
        )
        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.document
            )
        )
        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.application
            )
        )
        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.analysis
            )
        )

    def test_student_cannot_access_another_students_records(self):
        self.assertFalse(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.other_student
            )
        )
        self.assertFalse(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.other_student_skill
            )
        )
        self.assertFalse(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.other_document
            )
        )
        self.assertFalse(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.other_application
            )
        )
        self.assertFalse(
            self.can_access(
                IsStudentRecordOwner, self.student_user, self.other_analysis
            )
        )

    def test_employer_can_access_own_recruitment_records(self):
        self.assertTrue(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.employer
            )
        )
        self.assertTrue(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.vacancy
            )
        )
        self.assertTrue(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.vacancy_skill
            )
        )
        self.assertTrue(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.application
            )
        )

    def test_employer_cannot_access_another_employers_records(self):
        self.assertFalse(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.other_employer
            )
        )
        self.assertFalse(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.other_vacancy
            )
        )
        self.assertFalse(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.other_application
            )
        )

    def test_employer_cannot_access_private_student_analysis(self):
        self.assertFalse(
            self.can_access(
                IsEmployerRecordOwner, self.employer_user, self.analysis
            )
        )

    def test_university_can_access_own_profile_and_linked_students(self):
        self.assertTrue(
            self.can_access(
                IsUniversityRecordOwner, self.university_user, self.university
            )
        )
        self.assertTrue(
            self.can_access(
                IsUniversityRecordOwner, self.university_user, self.student
            )
        )

    def test_university_cannot_access_unlinked_students(self):
        self.assertFalse(
            self.can_access(
                IsUniversityRecordOwner,
                self.university_user,
                self.other_student,
            )
        )

    def test_university_cannot_access_private_student_documents(self):
        self.assertFalse(
            self.can_access(
                IsUniversityRecordOwner,
                self.university_user,
                self.document,
            )
        )

    def test_university_cannot_access_another_university_profile(self):
        self.assertFalse(
            self.can_access(
                IsUniversityRecordOwner,
                self.university_user,
                self.other_university,
            )
        )

    def test_admin_can_access_records(self):
        admin = User.objects.create_superuser(
            username="ownership_admin",
            email="admin@example.com",
            password="AdminPassword@2026",
        )

        self.assertTrue(
            IsStudentRecordOwner().has_permission(
                SimpleNamespace(user=admin), None
            )
        )

        self.assertTrue(
            self.can_access(
                IsStudentRecordOwner,
                admin,
                self.other_student,
            )
        )


class StudentProfileEndpointTests(TestCase):
    """Test the actual student profile HTTP endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.url = "/api/student/profile/"
        self.password = "CareerTest@2026Secure"

        self.student_user = self.create_student(
            "profile_student"
        )
        self.other_student_user = self.create_student(
            "other_student"
        )

        self.employer_user = User.objects.create_user(
            username="profile_employer",
            email="employer@example.com",
            password=self.password,
        )
        employer_profile = UserProfile.objects.create(
            user=self.employer_user,
            role=UserProfile.Role.EMPLOYER,
        )
        EmployerProfile.objects.create(
            user_profile=employer_profile,
            company_name="Test Company",
        )

        self.student = self.student_user.career_profile.student_profile

    def create_student(self, username):
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password=self.password,
        )

        profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.Role.STUDENT,
        )

        StudentProfile.objects.create(
            user_profile=profile,
        )

        return user

    def test_unauthenticated_user_cannot_access_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_student_can_retrieve_own_profile(self):
        self.client.force_authenticate(
            user=self.student_user
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["id"], self.student.id)

    def test_student_can_update_own_profile(self):
        self.client.force_authenticate(
            user=self.student_user
        )

        response = self.client.patch(
            self.url,
            {
                "programme": "Computer Science",
                "education_level": "Undergraduate",
                "location": "Kenya",
                "bio": "Interested in software engineering.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.student.refresh_from_db()

        self.assertEqual(
            self.student.programme,
            "Computer Science",
        )
        self.assertEqual(
            self.student.education_level,
            "Undergraduate",
        )
        self.assertEqual(
            self.student.location,
            "Kenya",
        )

    def test_student_cannot_access_another_students_profile(self):
        self.client.force_authenticate(
            user=self.other_student_user
        )

        # The endpoint only returns the authenticated
        # student's own profile.
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertNotEqual(
            response.data["id"],
            self.student.id,
        )

    def test_employer_cannot_access_student_profile_endpoint(self):
        self.client.force_authenticate(
            user=self.employer_user
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

class StudentSkillsEndpointTests(TestCase):
    """Test student skills catalogue and ownership-protected endpoints."""

    def setUp(self):
        self.client = APIClient()

        self.catalogue_url = "/api/skills/"
        self.skills_url = "/api/student/skills/"

        self.password = "CareerTest@2026Secure"

        self.student_user = self.create_student("skills_student")
        self.other_student_user = self.create_student("other_skills_student")

        self.employer_user = User.objects.create_user(
            username="skills_employer",
            password=self.password,
        )
        UserProfile.objects.create(
            user=self.employer_user,
            role=UserProfile.Role.EMPLOYER,
        )

        self.python = Skill.objects.create(
            name="Python",
            category="Programming",
            description="Python programming language.",
            is_active=True,
        )

        self.sql = Skill.objects.create(
            name="SQL",
            category="Database",
            description="Database querying language.",
            is_active=True,
        )

        self.inactive_skill = Skill.objects.create(
            name="Inactive Skill",
            category="Other",
            is_active=False,
        )

        self.student = self.student_user.career_profile.student_profile
        self.other_student = (
            self.other_student_user.career_profile.student_profile
        )

        self.student_skill = StudentSkill.objects.create(
            student=self.student,
            skill=self.python,
            level=70,
        )

        self.other_student_skill = StudentSkill.objects.create(
            student=self.other_student,
            skill=self.sql,
            level=50,
        )

    def create_student(self, username):
        user = User.objects.create_user(
            username=username,
            password=self.password,
        )

        profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.Role.STUDENT,
        )

        StudentProfile.objects.create(
            user_profile=profile,
        )

        return user

    def authenticate_student(self):
        self.client.force_authenticate(user=self.student_user)

    def test_unauthenticated_user_cannot_access_catalogue(self):
        response = self.client.get(self.catalogue_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_view_active_skill_catalogue(self):
        self.authenticate_student()

        response = self.client.get(self.catalogue_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_ids = [item["id"] for item in response.data]

        self.assertIn(self.python.id, returned_ids)
        self.assertIn(self.sql.id, returned_ids)
        self.assertNotIn(self.inactive_skill.id, returned_ids)

    def test_student_can_view_own_skills(self):
        self.authenticate_student()

        response = self.client.get(self.skills_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_ids = [item["id"] for item in response.data]

        self.assertIn(self.student_skill.id, returned_ids)
        self.assertNotIn(self.other_student_skill.id, returned_ids)

    def test_student_can_add_skill(self):
        self.authenticate_student()

        response = self.client.post(
            self.skills_url,
            {
                "skill": self.sql.id,
                "level": 65,
                "evidence_description": "Used SQL in a university project.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        new_skill = StudentSkill.objects.get(
            student=self.student,
            skill=self.sql,
        )

        self.assertEqual(new_skill.level, 65)
        self.assertFalse(new_skill.verified)
        self.assertEqual(
            new_skill.source,
            StudentSkill.Source.SELF_REPORTED,
        )

    def test_student_cannot_add_duplicate_skill(self):
        self.authenticate_student()

        response = self.client.post(
            self.skills_url,
            {
                "skill": self.python.id,
                "level": 80,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            StudentSkill.objects.filter(
                student=self.student,
                skill=self.python,
            ).count(),
            1,
        )

    def test_student_cannot_add_inactive_skill(self):
        self.authenticate_student()

        response = self.client.post(
            self.skills_url,
            {
                "skill": self.inactive_skill.id,
                "level": 50,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_student_can_update_own_skill(self):
        self.authenticate_student()

        response = self.client.patch(
            f"{self.skills_url}{self.student_skill.id}/",
            {
                "level": 90,
                "evidence_description": "Completed an advanced Python project.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.student_skill.refresh_from_db()

        self.assertEqual(self.student_skill.level, 90)
        self.assertEqual(
            self.student_skill.evidence_description,
            "Completed an advanced Python project.",
        )

    def test_student_cannot_change_verification_fields(self):
        self.authenticate_student()

        response = self.client.patch(
            f"{self.skills_url}{self.student_skill.id}/",
            {
                "level": 85,
                "verified": True,
                "source": StudentSkill.Source.EMPLOYER,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.student_skill.refresh_from_db()

        self.assertEqual(self.student_skill.level, 85)
        self.assertFalse(self.student_skill.verified)
        self.assertEqual(
            self.student_skill.source,
            StudentSkill.Source.SELF_REPORTED,
        )
        self.assertIsNone(self.student_skill.verified_by)

    def test_student_cannot_access_another_students_skill(self):
        self.authenticate_student()

        response = self.client.patch(
            f"{self.skills_url}{self.other_student_skill.id}/",
            {"level": 100},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_student_cannot_delete_another_students_skill(self):
        self.authenticate_student()

        response = self.client.delete(
            f"{self.skills_url}{self.other_student_skill.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            StudentSkill.objects.filter(
                pk=self.other_student_skill.id
            ).exists()
        )

    def test_student_can_delete_own_skill(self):
        self.authenticate_student()

        response = self.client.delete(
            f"{self.skills_url}{self.student_skill.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            StudentSkill.objects.filter(
                pk=self.student_skill.id
            ).exists()
        )

    def test_employer_cannot_access_student_skills(self):
        self.client.force_authenticate(user=self.employer_user)

        response = self.client.get(self.skills_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

class StudentDocumentEndpointTests(TestCase):
    """Test secure student document upload, listing, download and deletion."""

    def setUp(self):
        self.client = APIClient()

        self.documents_url = "/api/student/documents/"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.storage_settings = override_settings(
            MEDIA_ROOT=self.temp_dir.name
        )
        self.storage_settings.enable()
        self.addCleanup(self.storage_settings.disable)

        self.password = "DocumentTest@2026Secure"

        self.student_user = self.create_student("document_student")
        self.other_student_user = self.create_student("other_document_student")

        self.employer_user = User.objects.create_user(
            username="document_employer",
            password=self.password,
        )
        UserProfile.objects.create(
            user=self.employer_user,
            role=UserProfile.Role.EMPLOYER,
        )

        self.student = (
            self.student_user.career_profile.student_profile
        )
        self.other_student = (
            self.other_student_user.career_profile.student_profile
        )

        self.other_document = StudentDocument.objects.create(
            student=self.other_student,
            document_type=StudentDocument.DocumentType.CV,
            original_filename="other_resume.pdf",
            storage_key="student_documents/other_resume.pdf",
            mime_type="application/pdf",
            size_bytes=100,
        )

    def create_student(self, username):
        user = User.objects.create_user(
            username=username,
            password=self.password,
        )

        profile = UserProfile.objects.create(
            user=user,
            role=UserProfile.Role.STUDENT,
        )

        StudentProfile.objects.create(
            user_profile=profile,
        )

        return user

    def authenticate_student(self):
        self.client.force_authenticate(user=self.student_user)

    def make_pdf(self, filename="resume.pdf"):
        return SimpleUploadedFile(
            filename,
            b"%PDF-1.7\nTest PDF document content",
            content_type="application/pdf",
        )

    def make_docx(self, filename="transcript.docx"):
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr(
                "[Content_Types].xml",
                "<Types></Types>",
            )
            archive.writestr(
                "word/document.xml",
                "<document></document>",
            )

        return SimpleUploadedFile(
            filename,
            buffer.getvalue(),
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
        )

    def test_unauthenticated_user_cannot_list_documents(self):
        response = self.client.get(self.documents_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_employer_cannot_access_student_documents(self):
        self.client.force_authenticate(user=self.employer_user)

        response = self.client.get(self.documents_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_student_can_upload_pdf(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf(),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        document = StudentDocument.objects.get(
            student=self.student,
        )

        self.assertEqual(document.document_type, "cv")
        self.assertEqual(document.extraction_status, "failed")
        self.assertEqual(document.review_status, "pending")
        self.assertEqual(document.extracted_data["text"], "")
        self.assertIsNotNone(document.extracted_data["error"])

        self.assertTrue(
            (Path(settings.MEDIA_ROOT) / document.storage_key).is_file()
        )

    @patch("api.views.extract_document")
    def test_cv_upload_automatically_saves_detected_skills(
        self, mock_extract_document
    ):
        self.authenticate_student()

        cv_text = (
            "Developed applications using Python, Django, "
            "JavaScript and React. Used Git for version control."
        )

        mock_extract_document.return_value = {
            "text": cv_text,
            "page_count": 1,
            "character_count": len(cv_text),
            "metadata": {},
            "truncated": False,
            "is_empty": False,
            "requires_ocr": False,
            "format": "pdf",
        }

        # Ensure the required skills exist in the catalogue.
        skill_names = ["Python", "Django", "JavaScript", "React", "Git"]

        for name in skill_names:
            Skill.objects.get_or_create(
                name=name,
                defaults={
                    "category": "Programming",
                    "is_active": True,
                },
            )

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf(),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        records = StudentSkill.objects.filter(
            student=self.student,
            skill__name__in=skill_names,
        ).select_related("skill")

        self.assertEqual(records.count(), 5)

        for record in records:
            self.assertEqual(
                record.source,
                StudentSkill.Source.CV_EXTRACTED,
            )
            self.assertIsNone(record.level)
            self.assertFalse(record.verified)
            self.assertTrue(record.evidence_description)

        # Upload the same CV again: no duplicate skill records.
        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf("second_resume.pdf"),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            StudentSkill.objects.filter(
                student=self.student,
                skill__name__in=skill_names,
            ).count(),
            5,
        )



    def test_student_can_upload_docx(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "transcript",
                "file": self.make_docx(),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        document = StudentDocument.objects.get(
            student=self.student,
        )

        self.assertEqual(document.document_type, "transcript")
        self.assertTrue(
            (Path(settings.MEDIA_ROOT) / document.storage_key).is_file()
        )

    def test_upload_requires_a_file(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {"document_type": "cv"},
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_upload_rejects_unsupported_extension(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": SimpleUploadedFile(
                    "resume.exe",
                    b"not a document",
                ),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_upload_rejects_invalid_pdf_content(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": SimpleUploadedFile(
                    "fake.pdf",
                    b"this is not a PDF",
                ),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_upload_rejects_invalid_docx_content(self):
        self.authenticate_student()

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "transcript",
                "file": SimpleUploadedFile(
                    "fake.docx",
                    b"this is not a DOCX archive",
                ),
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_upload_rejects_files_larger_than_five_mb(self):
        self.authenticate_student()

        oversized_file = SimpleUploadedFile(
            "large.pdf",
            b"%PDF-" + (b"A" * (5 * 1024 * 1024)),
        )

        response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": oversized_file,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_student_can_list_only_own_documents(self):
        self.authenticate_student()

        self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf(),
            },
            format="multipart",
        )

        response = self.client.get(self.documents_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        returned_ids = [item["id"] for item in response.data]

        self.assertEqual(len(returned_ids), 1)
        self.assertNotIn(self.other_document.id, returned_ids)

    def test_student_can_download_own_document(self):
        self.authenticate_student()

        upload_response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf(),
            },
            format="multipart",
        )

        document_id = upload_response.data["document"]["id"]

        response = self.client.get(
            f"{self.documents_url}{document_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response["Content-Disposition"].split(";")[0],
            "attachment",
        )

        for resource_closer in response._resource_closers:
            resource_closer()
    def test_student_cannot_delete_another_students_document(self):
        self.authenticate_student()

        response = self.client.delete(
            f"{self.documents_url}{self.other_document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            StudentDocument.objects.filter(
                pk=self.other_document.id
            ).exists()
        )

    def test_student_can_delete_own_document_and_file(self):
        self.authenticate_student()

        upload_response = self.client.post(
            self.documents_url,
            {
                "document_type": "cv",
                "file": self.make_pdf(),
            },
            format="multipart",
        )

        document_id = upload_response.data["document"]["id"]

        document = StudentDocument.objects.get(pk=document_id)
        file_path = Path(settings.MEDIA_ROOT) / document.storage_key

        self.assertTrue(file_path.is_file())

        response = self.client.delete(
            f"{self.documents_url}{document_id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            StudentDocument.objects.filter(pk=document_id).exists()
        )
        self.assertFalse(file_path.exists())

    def test_download_returns_404_when_file_is_missing(self):
        self.authenticate_student()

        missing_document = StudentDocument.objects.create(
            student=self.student,
            document_type=StudentDocument.DocumentType.CV,
            original_filename="missing.pdf",
            storage_key="student_documents/missing.pdf",
            mime_type="application/pdf",
            size_bytes=100,
        )

        response = self.client.get(
            f"{self.documents_url}{missing_document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
