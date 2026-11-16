
from rest_framework.permissions import BasePermission


def _is_admin(user):
    """Return True for Django staff and superuser accounts."""
    return bool(
        user
        and user.is_authenticated
        and (user.is_staff or user.is_superuser)
    )


class BaseRolePermission(BasePermission):
    """
    Base permission for users with a specific Career Intelligence role.
    """

    allowed_roles = ()

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        profile = getattr(user, "career_profile", None)

        if profile is None:
            return False

        return profile.role in self.allowed_roles


class IsStudent(BaseRolePermission):
    """Allow only student accounts."""
    allowed_roles = ("student",)


class IsEmployer(BaseRolePermission):
    """Allow only employer accounts."""
    allowed_roles = ("employer",)


class IsUniversity(BaseRolePermission):
    """Allow only university accounts."""
    allowed_roles = ("university",)


class IsStudentOrUniversity(BaseRolePermission):
    """Allow students and university accounts."""
    allowed_roles = ("student", "university")


class IsEmployerOrUniversity(BaseRolePermission):
    """Allow employers and university accounts."""
    allowed_roles = ("employer", "university")


class IsCareerAdmin(BasePermission):
    """Allow Django staff and superuser accounts."""

    def has_permission(self, request, view):
        return _is_admin(request.user)


class BaseOwnedRecordPermission(BaseRolePermission):
    """
    Base class for permissions that check both account role
    and ownership of an individual database record.
    """

    def has_permission(self, request, view):
        return (
            _is_admin(request.user)
            or super().has_permission(request, view)
        )

    def has_object_permission(self, request, view, obj):
        if _is_admin(request.user):
            return True

        profile = getattr(request.user, "career_profile", None)

        if profile is None or profile.role not in self.allowed_roles:
            return False

        return self.owns_record(request.user, profile, obj)

    def owns_record(self, user, profile, obj):
        raise NotImplementedError(
            "Subclasses must implement owns_record()."
        )


class IsStudentRecordOwner(BaseOwnedRecordPermission):
    """
    Students can access their own profiles, skills, documents,
    applications and student-linked analyses.
    """

    allowed_roles = ("student",)

    def owns_record(self, user, profile, obj):
        student = getattr(profile, "student_profile", None)

        if student is None:
            return False

        model_name = obj._meta.model_name

        if model_name == "studentprofile":
            return obj.pk == student.pk

        if model_name in (
            "studentskill",
            "studentdocument",
            "jobapplication",
        ):
            return getattr(obj, "student_id", None) == student.pk

        if model_name == "intelligenceanalysis":
            return (
                getattr(obj, "student_id", None) == student.pk
                and getattr(obj, "created_by_id", None)
                in (None, user.pk)
            )

        return False


class IsEmployerRecordOwner(BaseOwnedRecordPermission):
    """
    Employers can access their own profile, vacancies,
    vacancy skills and applications to their vacancies.
    """

    allowed_roles = ("employer",)

    def owns_record(self, user, profile, obj):
        employer = getattr(profile, "employer_profile", None)

        if employer is None:
            return False

        model_name = obj._meta.model_name

        if model_name == "employerprofile":
            return obj.pk == employer.pk

        if model_name == "vacancy":
            return obj.employer_id == employer.pk

        if model_name == "vacancyskill":
            return obj.vacancy.employer_id == employer.pk

        if model_name == "jobapplication":
            return obj.vacancy.employer_id == employer.pk

        # Private student analyses are not automatically
        # accessible to employers.
        return False


class IsUniversityRecordOwner(BaseOwnedRecordPermission):
    """
    Universities can access their own institution profile
    and student profiles linked to that institution.

    Access to private student documents and applications
    requires a separate access policy.
    """

    allowed_roles = ("university",)

    def owns_record(self, user, profile, obj):
        university = getattr(profile, "university_profile", None)

        if university is None:
            return False

        model_name = obj._meta.model_name

        if model_name == "universityprofile":
            return obj.pk == university.pk

        if model_name == "studentprofile":
            return obj.university_id == university.pk

        return False
