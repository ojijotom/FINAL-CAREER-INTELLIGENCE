from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from .career_guidance import StudentCareerGuidanceView


urlpatterns = [
    path("", views.api_status, name="api_status"),

    path(
        "auth/register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/me/",
        views.CurrentUserView.as_view(),
        name="current_user",
    ),

    path(
        "student/profile/",
        views.StudentProfileView.as_view(),
        name="student_profile",
    ),

    path(
        "skills/",
        views.SkillCatalogueView.as_view(),
        name="skill_catalogue",
    ),
    path(
        "student/skills/",
        views.StudentSkillsView.as_view(),
        name="student_skills",
    ),
    path(
        "student/skills/<int:pk>/",
        views.StudentSkillDetailView.as_view(),
        name="student_skill_detail",
    ),
    path(
        "student/documents/",
        views.StudentDocumentsView.as_view(),
        name="student_documents",
    ),
    path(
        "student/documents/<int:pk>/",
        views.StudentDocumentDetailView.as_view(),
        name="student_document_detail",
    ),
    path(
        "student/career-guidance/",
        StudentCareerGuidanceView.as_view(),
        name="student_career_guidance",
    ),
]
