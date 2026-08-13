from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "merchant",
        "amount",
        "status",
        "created_at",
        "paid_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "merchant__username",
        "merchant__email",
        "description",
    )