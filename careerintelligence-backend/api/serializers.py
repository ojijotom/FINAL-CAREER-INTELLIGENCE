
from rest_framework import serializers

from .models import (
    StudentProfile,
    StudentSkill,
    Skill,
    Career,
    CareerSkillRequirement,
    UniversityProfile,
    StudentDocument,
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
    """Serialize skills reported by a student."""

    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.filter(is_active=True)
    )

    class Meta:
        model = StudentSkill
        fields = [
            "id",
            "skill",
            "level",
            "verified",
            "source",
            "evidence_description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
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

