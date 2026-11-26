from intelligence_engine.skill_extraction import extract_skills
from intelligence_engine.document_extraction import extract_document
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Q
from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .auth_serializers import RegisterSerializer
from .models import (
    StudentProfile,
    Skill,
    StudentSkill,
    StudentDocument,
    JobApplication,
    Vacancy,
    IntelligenceAnalysis,
)
from .serializers import (
    StudentProfileSerializer,
    SkillSerializer,
    StudentSkillSerializer,
    VacancySerializer,
)
from .permissions import IsStudentRecordOwner, IsStudent
import os
import uuid
import zipfile

from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.utils.text import get_valid_filename

from rest_framework.parsers import MultiPartParser, FormParser

from .models import StudentDocument
from .serializers import StudentDocumentSerializer

def api_status(request):
    """Public backend health-check endpoint."""
    return JsonResponse({
        "project": "Career Intelligence",
        "message": "Backend is running successfully",
        "status": "success",
    })


class RegisterView(APIView):
    """Register a student, employer or university account."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        profile = user.career_profile

        return Response(
            {
                "message": "Account created successfully.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": profile.role,
                    "phone_number": profile.phone_number,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CurrentUserView(APIView):
    """Return details for the currently authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "career_profile", None)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": profile.role if profile else None,
            "phone_number": profile.phone_number if profile else None,
        })


class StudentProfileView(APIView):
    """Retrieve and update the authenticated student's own profile."""

    permission_classes = [IsStudentRecordOwner]

    def get_object(self):
        student = get_object_or_404(
            StudentProfile.objects.select_related(
                "user_profile",
                "university",
            ),
            user_profile__user=self.request.user,
        )

        self.check_object_permissions(self.request, student)
        return student

    def get(self, request):
        student = self.get_object()
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data)

    def patch(self, request):
        student = self.get_object()

        serializer = StudentProfileSerializer(
            student,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Student profile updated successfully.",
            "profile": serializer.data,
        })


class SkillCatalogueView(APIView):
    """Return the shared catalogue of active skills."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = Skill.objects.filter(
            is_active=True
        ).order_by("name")

        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


class StudentSkillsView(APIView):
    """List and add skills belonging to the authenticated student."""

    permission_classes = [IsStudentRecordOwner]

    def get_student(self):
        return get_object_or_404(
            StudentProfile,
            user_profile__user=self.request.user,
        )

    def get(self, request):
        student = self.get_student()

        skills = StudentSkill.objects.filter(
            student=student
        ).select_related("skill").order_by("skill__name")

        serializer = StudentSkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = self.get_student()

        serializer = StudentSkillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        skill = serializer.validated_data["skill"]

        if StudentSkill.objects.filter(
            student=student,
            skill=skill,
        ).exists():
            return Response(
                {"skill": ["You have already added this skill."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student_skill = serializer.save(student=student)

        return Response(
            {
                "message": "Skill added successfully.",
                "skill": StudentSkillSerializer(student_skill).data,
            },
            status=status.HTTP_201_CREATED,
        )


class StudentSkillDetailView(APIView):
    """Update or delete one skill belonging to the authenticated student."""

    permission_classes = [IsStudentRecordOwner]

    def get_object(self, pk):
        student_skill = get_object_or_404(
            StudentSkill.objects.select_related("student", "skill"),
            pk=pk,
            student__user_profile__user=self.request.user,
        )

        self.check_object_permissions(self.request, student_skill)
        return student_skill

    def patch(self, request, pk):
        student_skill = self.get_object(pk)

        serializer = StudentSkillSerializer(
            student_skill,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        new_skill = serializer.validated_data.get(
            "skill",
            student_skill.skill,
        )

        duplicate_exists = StudentSkill.objects.filter(
            student=student_skill.student,
            skill=new_skill,
        ).exclude(pk=student_skill.pk).exists()

        if duplicate_exists:
            return Response(
                {"skill": ["You have already added this skill."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response({
            "message": "Skill updated successfully.",
            "skill": serializer.data,
        })

    def delete(self, request, pk):
        student_skill = self.get_object(pk)
        student_skill.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# ============================================================
# 7. STUDENT DOCUMENT MANAGEMENT
# ============================================================

MAX_DOCUMENT_SIZE = 5 * 1024 * 1024

ALLOWED_DOCUMENT_TYPES = {
    "application/pdf": {
        "extension": ".pdf",
        "signature": b"%PDF-",
    },
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "extension": ".docx",
        "signature": None,
    },
}


def validate_student_document(uploaded_file):
    """Validate document size, extension and actual file structure."""

    if uploaded_file.size > MAX_DOCUMENT_SIZE:
        raise ValueError("The maximum document size is 5 MB.")

    if uploaded_file.size == 0:
        raise ValueError("The uploaded document is empty.")

    original_name = Path(uploaded_file.name).name
    extension = Path(original_name).suffix.lower()

    if extension not in (".pdf", ".docx"):
        raise ValueError("Only PDF and DOCX documents are allowed.")

    uploaded_file.seek(0)
    file_start = uploaded_file.read(8)
    uploaded_file.seek(0)

    if extension == ".pdf":
        if not file_start.startswith(b"%PDF-"):
            raise ValueError("The uploaded file is not a valid PDF.")

    elif extension == ".docx":
        if not zipfile.is_zipfile(uploaded_file):
            raise ValueError("The uploaded DOCX file is invalid.")

        uploaded_file.seek(0)

        try:
            with zipfile.ZipFile(uploaded_file) as archive:
                names = set(archive.namelist())

                required_files = {
                    "[Content_Types].xml",
                    "word/document.xml",
                }

                if not required_files.issubset(names):
                    raise ValueError("The uploaded DOCX structure is invalid.")

        except zipfile.BadZipFile:
            raise ValueError("The uploaded DOCX file is invalid.")

    uploaded_file.seek(0)

    return extension


class StudentDocumentsView(APIView):
    """List and upload documents belonging to the authenticated student."""

    permission_classes = [IsStudentRecordOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_student(self):
        return get_object_or_404(
            StudentProfile,
            user_profile__user=self.request.user,
        )

    def get(self, request):
        student = self.get_student()

        documents = StudentDocument.objects.filter(
            student=student
        ).order_by("-uploaded_at")

        serializer = StudentDocumentSerializer(
            documents,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        student = self.get_student()

        uploaded_file = request.FILES.get("file")
        document_type = request.data.get("document_type")

        if uploaded_file is None:
            return Response(
                {"file": ["Please select a document to upload."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        allowed_types = [
            choice[0]
            for choice in StudentDocument.DocumentType.choices
        ]

        if document_type not in allowed_types:
            return Response(
                {"document_type": ["Select a valid document type."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            extension = validate_student_document(uploaded_file)
        except ValueError as error:
            return Response(
                {"file": [str(error)]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        original_filename = get_valid_filename(
            Path(uploaded_file.name).name
        )[:255]

        storage_directory = Path("student_documents") / str(student.pk)

        storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=None,
        )

        storage_key = (
            storage_directory / f"{uuid.uuid4().hex}{extension}"
        ).as_posix()

        saved_name = None

        try:
            saved_name = storage.save(storage_key, uploaded_file)

            document = StudentDocument.objects.create(
                student=student,
                document_type=document_type,
                original_filename=original_filename,
                storage_key=saved_name,
                mime_type=(
                    "application/pdf"
                    if extension == ".pdf"
                    else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ),
                size_bytes=uploaded_file.size,
            )

       
        except Exception:
            if saved_name and storage.exists(saved_name):
                storage.delete(saved_name)

            raise

       
       
        # Extract readable text from the saved document.
        document.extraction_status = (
            StudentDocument.ExtractionStatus.PROCESSING
        )
        document.save(update_fields=["extraction_status"])

        try:
            extraction = extract_document(
                storage.path(saved_name)
            )

            document.extracted_data = {
                "text": extraction["text"],
                "pages": extraction.get("page_count", 0),
                "characters": extraction.get("character_count", 0),
                "metadata": extraction.get("metadata", {}),
                "truncated": extraction.get("truncated", False),
                "is_empty": extraction.get("is_empty", False),
                "requires_ocr": extraction.get("requires_ocr", False),
                "format": extraction.get("format", ""),
                "error": None,
            }

            document.extraction_status = (
                StudentDocument.ExtractionStatus.COMPLETED
            )

            # Automatically detect skills from CVs and transcripts.
            detected_skill_data = []

            if document.document_type in ["cv", "transcript"]:
                try:
                    detected_skills = extract_skills(
                        extraction.get("text", ""),
                        Skill.objects.filter(is_active=True),
                    )

                    if document.document_type == "cv":
                        skill_source = (
                            StudentSkill.Source.CV_EXTRACTED
                        )
                    else:
                        skill_source = (
                            StudentSkill.Source.TRANSCRIPT_EXTRACTED
                        )

                    for item in detected_skills:
                        skill = item["skill"]

                        StudentSkill.objects.get_or_create(
                            student=student,
                            skill=skill,
                            defaults={
                                "level": None,
                                "verified": False,
                                "source": skill_source,
                                "evidence_description": item["evidence"],
                            },
                        )

                        detected_skill_data.append({
                            "name": skill.name,
                            "matched_alias": item["matched_alias"],
                            "evidence": item["evidence"],
                        })

                    document.extracted_data["detected_skills"] = (
                        detected_skill_data
                    )

                except Exception as skill_error:
                    document.extracted_data["skill_extraction_error"] = (
                        str(skill_error)
                    )

        except Exception as error:
            document.extracted_data = {
                "text": "",
                "pages": 0,
                "characters": 0,
                "metadata": {},
                "truncated": False,
                "is_empty": True,
                "requires_ocr": False,
                "error": str(error),
            }

            document.extraction_status = (
                StudentDocument.ExtractionStatus.FAILED
            )

        # Extracted information must always await student review.
        document.review_status = (
            StudentDocument.ReviewStatus.PENDING
        )

        document.save(
            update_fields=[
                "extracted_data",
                "extraction_status",
                "review_status",
            ]
        )

        serializer = StudentDocumentSerializer(document)


        return Response(
            {
                "message": "Document uploaded successfully.",
                "document": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )



class StudentDocumentDetailView(APIView):
    """Download or delete a document owned by the authenticated student."""

    permission_classes = [IsStudentRecordOwner]

    def get_object(self, pk):
        document = get_object_or_404(
            StudentDocument.objects.select_related("student"),
            pk=pk,
            student__user_profile__user=self.request.user,
        )

        self.check_object_permissions(self.request, document)

        return document

    def get(self, request, pk):
        document = self.get_object(pk)

        storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=None,
        )

        if not storage.exists(document.storage_key):
            return Response(
                {"error": "The requested document file is missing."},
                status=status.HTTP_404_NOT_FOUND,
            )

        file_handle = storage.open(document.storage_key, "rb")

        response = FileResponse(
            file_handle,
            as_attachment=True,
            filename=document.original_filename,
            content_type="application/octet-stream",
        )

        response["X-Content-Type-Options"] = "nosniff"
        response["Cache-Control"] = "private, no-store"

        return response

    def delete(self, request, pk):
        document = self.get_object(pk)

        storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=None,
        )

        storage.delete(document.storage_key)
        document.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentVacanciesView(APIView):
    """Return currently available vacancies for authenticated students."""

    permission_classes = [IsStudent]

    def get(self, request):
        vacancies = Vacancy.objects.filter(
            status=Vacancy.Status.ACTIVE
        ).filter(
            Q(closing_date__isnull=True)
            | Q(closing_date__gte=timezone.localdate())
        ).select_related(
            "employer"
        ).prefetch_related(
            "skill_requirements__skill"
        ).order_by("-created_at")

        serializer = VacancySerializer(
            vacancies,
            many=True,
        )

        return Response(serializer.data)
    
class StudentDashboardView(APIView):
    """Return real dashboard information for the authenticated student."""

    permission_classes = [IsStudent]

    def get(self, request):
        student = get_object_or_404(
            StudentProfile.objects.select_related(
                "user_profile__user",
                "university",
            ),
            user_profile__user=request.user,
        )

        user = student.user_profile.user

        # Student's actual skills
        skills = StudentSkill.objects.filter(
            student=student
        ).select_related("skill").order_by("skill__name")

        assessed_skills = skills.exclude(level__isnull=True)
        average_level = assessed_skills.aggregate(
            average=Avg("level")
        )["average"]

        # Student's actual documents
        documents = StudentDocument.objects.filter(student=student)

        # Student's actual job applications
        applications = JobApplication.objects.filter(
            student=student
        ).select_related(
            "vacancy",
            "vacancy__employer",
        ).order_by("-applied_at")

        # Currently available vacancies
        active_vacancies = Vacancy.objects.filter(
            status=Vacancy.Status.ACTIVE
        ).filter(
            Q(closing_date__isnull=True)
            | Q(closing_date__gte=timezone.localdate())
        ).select_related(
            "employer"
        ).order_by("-created_at")

        # Previously saved intelligence analyses
        analyses = IntelligenceAnalysis.objects.filter(
            student=student,
            status=IntelligenceAnalysis.Status.COMPLETED,
        ).select_related(
            "career",
            "vacancy",
        ).order_by("-created_at")

        return Response({
            "student": {
                "id": student.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "programme": student.programme,
                "education_level": student.education_level,
                "graduation_year": student.graduation_year,
                "university": (
                    student.university.institution_name
                    if student.university else None
                ),
            },

            "statistics": {
                "skills_count": skills.count(),
                "assessed_skills_count": assessed_skills.count(),
                "average_skill_level": (
                    round(float(average_level), 1)
                    if average_level is not None else None
                ),
                "documents_count": documents.count(),
                "verified_documents_count": documents.filter(
                    review_status=StudentDocument.ReviewStatus.VERIFIED
                ).count(),
                "applications_count": applications.count(),
                "active_vacancies_count": active_vacancies.count(),
            },

            "skills": [
                {
                    "id": item.id,
                    "name": item.skill.name,
                    "category": item.skill.category,
                    "level": item.level,
                    "verified": item.verified,
                    "source": item.source,
                    "evidence_description": item.evidence_description,
                }
                for item in skills
            ],

            "applications": [
                {
                    "id": item.id,
                    "job_title": item.vacancy.title,
                    "company": item.vacancy.employer.company_name,
                    "status": item.status,
                    "applied_at": item.applied_at.isoformat(),
                }
                for item in applications[:5]
            ],

            "vacancies": [
                {
                    "id": item.id,
                    "title": item.title,
                    "company": item.employer.company_name,
                    "location": item.location,
                    "employment_type": item.employment_type,
                    "work_mode": item.work_mode,
                    "closing_date": (
                        item.closing_date.isoformat()
                        if item.closing_date else None
                    ),
                }
                for item in active_vacancies[:5]
            ],

            "career_analyses": [
                {
                    "id": item.id,
                    "analysis_type": item.analysis_type,
                    "career": (
                        item.career.title if item.career else None
                    ),
                    "result": item.result,
                    "created_at": item.created_at.isoformat(),
                }
                for item in analyses[:5]
            ],
        })
