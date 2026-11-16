
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    UserProfile,
    StudentProfile,
    EmployerProfile,
    UniversityProfile,
)

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    first_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
    )

    role = serializers.ChoiceField(
        choices=UserProfile.Role.choices
    )
    phone_number = serializers.CharField(
        max_length=30,
        required=False,
        allow_blank=True,
    )

    company_name = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=False,
    )
    institution_name = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=False,
    )
    programme = serializers.CharField(
    max_length=200,
    required=False,
    allow_blank=True,
    )
    def validate_username(self, value):
        value = value.strip()

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return value

    def validate(self, attrs):
        password = attrs["password"]

        if password != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Passwords do not match."
            })

        temporary_user = User(
            username=attrs["username"],
            email=attrs["email"],
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )

        validate_password(password, user=temporary_user)

        role = attrs["role"]

        if role == UserProfile.Role.EMPLOYER:
            if not attrs.get("company_name", "").strip():
                raise serializers.ValidationError({
                    "company_name": "Company name is required."
                })

        if role == UserProfile.Role.UNIVERSITY:
            if not attrs.get("institution_name", "").strip():
                raise serializers.ValidationError({
                    "institution_name": "Institution name is required."
                })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")
        role = validated_data.pop("role")
        phone_number = validated_data.pop("phone_number", "")

        company_name = validated_data.pop("company_name", "")
        institution_name = validated_data.pop("institution_name", "")
        programme = validated_data.pop("programme", "")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        user_profile = UserProfile.objects.create(
            user=user,
            role=role,
            phone_number=phone_number,
        )

        if role == UserProfile.Role.STUDENT:
            StudentProfile.objects.create(
                user_profile=user_profile,
                programme=programme.strip(),
            )
        elif role == UserProfile.Role.EMPLOYER:
            EmployerProfile.objects.create(
                user_profile=user_profile,
                company_name=company_name.strip(),
            )
        elif role == UserProfile.Role.UNIVERSITY:
            UniversityProfile.objects.create(
                user_profile=user_profile,
                institution_name=institution_name.strip(),
            )

        return user
class EmailOrUsernameTokenObtainPairSerializer(
    TokenObtainPairSerializer
):
    """
    Allow users to log in with either their email or username.
    """

    def validate(self, attrs):
        login_value = attrs.get(User.USERNAME_FIELD, "")

        if "@" in login_value:
            matching_user = User.objects.filter(
                email__iexact=login_value.strip()
            ).first()

            if matching_user:
                attrs[User.USERNAME_FIELD] = getattr(
                    matching_user,
                    User.USERNAME_FIELD,
                )

        return super().validate(attrs)
