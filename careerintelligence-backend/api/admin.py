
from django.contrib import admin

from .models import (
    UserProfile,
    UniversityProfile,
    StudentProfile,
    EmployerProfile,
    Skill,
    StudentSkill,
    Career,
    CareerSkillRequirement,
    Vacancy,
    VacancySkill,
    JobApplication,
    StudentDocument,
    IntelligenceAnalysis,
)


admin.site.register([
    UserProfile,
    UniversityProfile,
    StudentProfile,
    EmployerProfile,
    Skill,
    StudentSkill,
    Career,
    CareerSkillRequirement,
    Vacancy,
    VacancySkill,
    JobApplication,
    StudentDocument,
    IntelligenceAnalysis,
])
