from django.conf import settings
from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet",
    )

    available_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    pending_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"