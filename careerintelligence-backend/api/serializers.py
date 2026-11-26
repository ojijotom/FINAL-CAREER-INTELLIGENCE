
from rest_framework import serializers

from .models import (
    StudentProfile,
    StudentSkill,
    Skill,
    Career,
    CareerSkillRequirement,
    UniversityProfile,
    StudentDocument,
    Vacancy,
    VacancySkill,
)


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serialize a student's academic and personal profile."""

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "university",
            "programme",
            "education_level",
            "graduation_year",
            "experience_years",
            "interests",
            "location",
            "bio",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class SkillSerializer(serializers.ModelSerializer):
    """Expose the shared skills catalogue."""

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "category",
            "description",
        ]
        read_only_fields = fields

class StudentSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(
        source="skill.name",
        read_only=True,
    )

    skill_category = serializers.CharField(
        source="skill.category",
        read_only=True,
    )

    class Meta:
        model = StudentSkill
        fields = [
            "id",
            "skill",
            "skill_name",
            "skill_category",
            "level",
            "verified",
            "source",
            "evidence_description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "skill_name",
            "skill_category",
            "verified",
            "source",
            "created_at",
            "updated_at",
        ]

class CareerSkillRequirementSerializer(serializers.ModelSerializer):
    """Expose the skill requirements associated with a career."""

    skill_name = serializers.CharField(
        source="skill.name",
        read_only=True,
    )

    class Meta:
        model = CareerSkillRequirement
        fields = [
            "id",
            "skill",
            "skill_name",
            "target_level",
            "weight",
        ]
        read_only_fields = fields


class CareerSerializer(serializers.ModelSerializer):
    """Expose career information and required skills."""

    skill_requirements = CareerSkillRequirementSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Career
        fields = [
            "id",
            "title",
            "industry",
            "description",
            "education_level",
            "skill_requirements",
        ]
        read_only_fields = fields

class VacancySkillSerializer(serializers.ModelSerializer):
    """Expose the skills required by a job vacancy."""

    skill_name = serializers.CharField(
        source="skill.name",
        read_only=True,
    )
    skill_category = serializers.CharField(
        source="skill.category",
        read_only=True,
    )

    class Meta:
        model = VacancySkill
        fields = [
            "id",
            "skill",
            "skill_name",
            "skill_category",
            "requirement_type",
            "target_level",
            "weight",
        ]
        read_only_fields = fields


class VacancySerializer(serializers.ModelSerializer):
    """Expose vacancy information and its skill requirements."""

    company = serializers.CharField(
        source="employer.company_name",
        read_only=True,
    )

    skill_requirements = VacancySkillSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Vacancy
        fields = [
            "id",
            "title",
            "company",
            "description",
            "industry",
            "location",
            "employment_type",
            "work_mode",
            "status",
            "education_level",
            "minimum_experience_years",
            "posted_at",
            "closing_date",
            "created_at",
            "skill_requirements",
        ]
        read_only_fields = fields
        
class StudentDocumentSerializer(serializers.ModelSerializer):
    """Serialize document metadata without exposing private storage paths."""

    class Meta:
        model = StudentDocument
        fields = [
            "id",
            "document_type",
            "original_filename",
            "mime_type",
            "size_bytes",
            "extraction_status",
            "review_status",
            "uploaded_at",
        ]
        read_only_fields = fields

