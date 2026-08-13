from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment",
        "customer",
        "merchant",
        "amount",
        "transaction_type",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    search_fields = (
        "customer__username",
        "customer__email",
        "merchant__username",
        "merchant__email",
    )