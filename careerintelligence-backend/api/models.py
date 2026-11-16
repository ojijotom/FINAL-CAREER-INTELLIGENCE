
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# ============================================================
# 1. USER ACCOUNTS AND PORTAL PROFILES
# ============================================================

class UserProfile(models.Model):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        EMPLOYER = "employer", "Employer"
        UNIVERSITY = "university", "University"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="career_profile",
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    phone_number = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class UniversityProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="university_profile",
    )
    institution_name = models.CharField(max_length=200)
    institution_type = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.institution_name


class StudentProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    university = models.ForeignKey(
        UniversityProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    programme = models.CharField(max_length=200, blank=True)
    education_level = models.CharField(max_length=100, blank=True)
    graduation_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    experience_years = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    interests = models.JSONField(default=list, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student: {self.user_profile.user.username}"


class EmployerProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="employer_profile",
    )
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


# ============================================================
# 2. SHARED SKILLS CATALOGUE AND STUDENT SKILLS
# ============================================================

class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    class Source(models.TextChoices):
        SELF_REPORTED = "self_reported", "Self reported"
        CV_EXTRACTED = "cv_extracted", "CV extracted"
        TRANSCRIPT_EXTRACTED = "transcript_extracted", "Transcript extracted"
        ASSESSMENT = "assessment", "Assessment"
        EDUCATOR = "educator_verified", "Educator verified"
        EMPLOYER = "employer_verified", "Employer verified"

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="skills",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name="student_records",
    )
    level = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency from 0 to 100. NULL means not assessed.",
    )
    verified = models.BooleanField(default=False)
    source = models.CharField(
        max_length=30,
        choices=Source.choices,
        default=Source.SELF_REPORTED,
    )
    evidence_description = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_student_skills",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "skill"],
                name="uniq_student_skill",
            )
        ]
        ordering = ["skill__name"]

    def __str__(self):
        return f"{self.student} - {self.skill}"


# ============================================================
# 3. CAREER CATALOGUE AND CAREER SKILL REQUIREMENTS
# ============================================================

class Career(models.Model):
    title = models.CharField(max_length=200, unique=True)
    industry = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    education_level = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class CareerSkillRequirement(models.Model):
    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name="skill_requirements",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name="career_requirements",
    )
    target_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1.00,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["career", "skill"],
                name="uniq_career_skill_req",
            )
        ]

    def __str__(self):
        return f"{self.career} - {self.skill}"


# ============================================================
# 4. EMPLOYER VACANCIES AND VACANCY SKILL REQUIREMENTS
# ============================================================

class Vacancy(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "Paused"
        CLOSED = "closed", "Closed"
        EXPIRED = "expired", "Expired"

    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full time"
        PART_TIME = "part_time", "Part time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"
        TEMPORARY = "temporary", "Temporary"

    class WorkMode(models.TextChoices):
        ONSITE = "onsite", "On-site"
        HYBRID = "hybrid", "Hybrid"
        REMOTE = "remote", "Remote"

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="vacancies",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    industry = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        blank=True,
    )
    work_mode = models.CharField(
        max_length=20,
        choices=WorkMode.choices,
        default=WorkMode.ONSITE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    education_level = models.CharField(max_length=100, blank=True)
    minimum_experience_years = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    posted_at = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["status", "closing_date"],
                name="vac_status_close_idx",
            ),
            models.Index(
                fields=["employer", "status"],
                name="vac_employer_status_idx",
            ),
        ]

    def __str__(self):
        return self.title


class VacancySkill(models.Model):
    class RequirementType(models.TextChoices):
        REQUIRED = "required", "Required"
        PREFERRED = "preferred", "Preferred"

    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name="skill_requirements",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.PROTECT,
        related_name="vacancy_requirements",
    )
    requirement_type = models.CharField(
        max_length=20,
        choices=RequirementType.choices,
        default=RequirementType.REQUIRED,
    )
    target_level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1.00,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vacancy", "skill", "requirement_type"],
                name="uniq_vac_skill_type",
            )
        ]

    def __str__(self):
        return f"{self.vacancy} - {self.skill}"


# ============================================================
# 5. JOB APPLICATIONS
# ============================================================

class JobApplication(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        REVIEWING = "reviewing", "Reviewing"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        OFFERED = "offered", "Offered"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "vacancy"],
                name="uniq_student_vacancy",
            )
        ]
        ordering = ["-applied_at"]
        indexes = [
            models.Index(
                fields=["status", "applied_at"],
                name="app_status_date_idx",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.vacancy}"


# ============================================================
# 6. STUDENT DOCUMENTS
# ============================================================

class StudentDocument(models.Model):
    class DocumentType(models.TextChoices):
        CV = "cv", "CV"
        TRANSCRIPT = "transcript", "Transcript"
        CERTIFICATE = "certificate", "Certificate"
        OTHER = "other", "Other"

    class ExtractionStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    class ReviewStatus(models.TextChoices):
        PENDING = "pending", "Pending review"
        REVIEWED = "reviewed", "Reviewed"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
    )
    original_filename = models.CharField(max_length=255)
    storage_key = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=100, blank=True)
    size_bytes = models.PositiveBigIntegerField(null=True, blank=True)
    extraction_status = models.CharField(
        max_length=20,
        choices=ExtractionStatus.choices,
        default=ExtractionStatus.PENDING,
    )
    review_status = models.CharField(
        max_length=20,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
    )
    extracted_data = models.JSONField(default=dict, blank=True)
    reviewed_data = models.JSONField(default=dict, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.original_filename} ({self.document_type})"


# ============================================================
# 7. INTELLIGENCE ANALYSIS HISTORY
# ============================================================

class IntelligenceAnalysis(models.Model):
    class AnalysisType(models.TextChoices):
        CAREER_MATCH = "career_match", "Career matching"
        JOB_MATCH = "job_match", "Job suitability"
        SKILL_GAP = "skill_gap", "Skill gap"
        LEARNING_PLAN = "learning_plan", "Learning plan"
        LABOUR_MARKET = "labour_market", "Labour-market analysis"

    class Status(models.TextChoices):
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    analysis_type = models.CharField(
        max_length=30,
        choices=AnalysisType.choices,
    )
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="intelligence_analyses",
    )
    career = models.ForeignKey(
        Career,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analysis_history",
    )
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analysis_history",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.COMPLETED,
    )
    engine_version = models.CharField(max_length=50, blank=True)
    input_snapshot = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_intelligence_analyses",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["student", "analysis_type"],
                name="analysis_student_type_idx",
            ),
            models.Index(
                fields=["analysis_type", "created_at"],
                name="analysis_type_date_idx",
            ),
        ]

    def __str__(self):
        return f"{self.analysis_type} - {self.created_at}"
