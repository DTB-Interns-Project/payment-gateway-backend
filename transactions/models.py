from django.conf import settings
from django.db import models

from payments.models import Payment


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"

    payment = models.OneToOneField(
        Payment,
        on_delete=models.PROTECT,
        related_name="transaction",
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transactions_as_customer",
    )

    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transactions_as_merchant",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.PAYMENT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Transaction #{self.id} - {self.amount}"