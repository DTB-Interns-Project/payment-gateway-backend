from django.contrib import admin

from .models import Settlement


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "merchant",
        "amount",
        "status",
        "settlement_date",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "settlement_date",
    )

    search_fields = (
        "merchant__username",
        "merchant__email",
    )