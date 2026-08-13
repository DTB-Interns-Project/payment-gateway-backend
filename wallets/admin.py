from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "available_balance",
        "pending_balance",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )