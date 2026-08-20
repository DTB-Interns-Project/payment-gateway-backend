from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password_confirm = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "role",
        ]

    def validate(self, attrs):
        # Check that passwords match
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password": "Passwords do not match."
            })

        # Prevent users from registering as administrators
        if str(attrs.get("role", "")).upper() == "ADMIN":
            raise serializers.ValidationError({
                "role": "Admin accounts cannot be created through registration."
            })

        return attrs

    def create(self, validated_data):
        # Remove password confirmation
        validated_data.pop("password_confirm")

        # Extract password so create_user() can hash it
        password = validated_data.pop("password")

        # Create the user using Django's password hashing
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
        ]

        read_only_fields = [
            "id",
            "username",
            "email",
            "role",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    confirmPassword = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirmPassword",
        ]

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirmPassword")

        # Only validate passwords when the user is changing them
        if password or confirm_password:

            if not password:
                raise serializers.ValidationError({
                    "password": "Please enter a new password."
                })

            if not confirm_password:
                raise serializers.ValidationError({
                    "confirmPassword": "Please confirm your new password."
                })

            if password != confirm_password:
                raise serializers.ValidationError({
                    "confirmPassword": "Passwords do not match."
                })

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", "")
        validated_data.pop("confirmPassword", "")

        # Update profile information
        instance.first_name = validated_data.get(
            "first_name",
            instance.first_name
        )

        instance.last_name = validated_data.get(
            "last_name",
            instance.last_name
        )

        instance.username = validated_data.get(
            "username",
            instance.username
        )

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        # Update password only when a new password was provided
        if password:
            instance.set_password(password)

        instance.save()

        return instance