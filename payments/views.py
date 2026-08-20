from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from wallets.models import Wallet
from transactions.models import Transaction

from .models import Payment
from .serializers import PaymentSerializer


class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        customer = serializer.validated_data["customer"]
        merchant = serializer.validated_data["merchant"]
        amount = serializer.validated_data["amount"]
        description = serializer.validated_data.get("description", "")

        # Get both wallets
        try:
            customer_wallet = Wallet.objects.select_for_update().get(
                user=customer
            )
            merchant_wallet = Wallet.objects.select_for_update().get(
                user=merchant
            )
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Customer or merchant wallet does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check customer's balance
        if customer_wallet.available_balance < amount:
            return Response(
                {"error": "Insufficient wallet balance."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct from customer
        customer_wallet.available_balance -= amount
        customer_wallet.save()

        # Credit merchant
        merchant_wallet.available_balance += amount
        merchant_wallet.save()

        # Create payment
        payment = Payment.objects.create(
            customer=customer,
            merchant=merchant,
            amount=amount,
            description=description,
            status="PAID",
            paid_at=timezone.now(),
        )

        # Create transaction
        Transaction.objects.create(
            payment=payment,
            customer=customer,
            merchant=merchant,
            amount=amount,
            transaction_type="PAYMENT",
        )

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )