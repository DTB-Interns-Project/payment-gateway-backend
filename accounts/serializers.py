from django.contrib.auth.models import User
from rest_framework import serializers


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

        if password:
            instance.set_password(password)

        instance.save()

        return instance