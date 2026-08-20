from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Payment


User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "customer",
            "merchant",
            "amount",
            "description",
            "status",
            "created_at",
            "updated_at",
            "paid_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "paid_at",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Payment amount must be greater than zero."
            )

        return value

    def validate(self, data):
        customer = data["customer"]
        merchant = data["merchant"]

        if customer == merchant:
            raise serializers.ValidationError(
                "Customer and merchant cannot be the same user."
            )

        return data