from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from adoption.models import AdoptionHistory, Payment
from adoption.serializers import (
    AdoptionHistorySerializer,
    CreateAdoptionSerializer,
    PaymentSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings as main_settings
from django.shortcuts import HttpResponseRedirect, redirect


class AdoptionHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return AdoptionHistory.objects.none()

        return AdoptionHistory.objects.filter(
            adopt__user=self.request.user
        ).select_related("pet")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAdoptionSerializer
        return AdoptionHistorySerializer

    @swagger_auto_schema(
        operation_summary="View all adoption histories",
        operation_description="This allows a customer to view their adoption histories",
        responses={200: AdoptionHistorySerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Adopt a pet",
        operation_description="This allows a customer to adopt a pet if they have sufficient balance",
        request_body=CreateAdoptionSerializer,
        responses={201: AdoptionHistorySerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only customer can adopt pet"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adoption_history = serializer.save()

        response_serializer = AdoptionHistorySerializer(adoption_history)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    adoption_id = request.data.get("adoptionId")
    settings = {
        "store_id": "furne68ea8e6be6f18",
        "store_pass": "furne68ea8e6be6f18@ssl",
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body["total_amount"] = amount
    post_body["currency"] = "BDT"
    post_body["tran_id"] = f"txn_{adoption_id}"
    post_body["success_url"] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body["fail_url"] = "http://localhost:5173/dashboard/adoption-history"
    post_body["cancel_url"] = "http://localhost:5173/dashboard/adoption-history"
    post_body["emi_option"] = 0
    post_body["cus_name"] = f"{user.first_name} {user.last_name}"
    post_body["cus_email"] = user.email
    post_body["cus_phone"] = user.phone_number
    post_body["cus_add1"] = user.address
    post_body["cus_city"] = "Dhaka"
    post_body["cus_country"] = "Bangladesh"
    post_body["shipping_method"] = "NO"
    post_body["multi_card_name"] = ""
    post_body["num_of_item"] = 1
    post_body["product_name"] = "Furnest Pet"
    post_body["product_category"] = "Test Category"
    post_body["product_profile"] = "general"

    response = sslcz.createSession(post_body)  # API response

    if response.get("status") == "SUCCESS":
        return Response({"payment_url": response["GatewayPageURL"]})
    return Response(
        {"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST", "GET"])
def payment_success(request):
    tran_id = request.data.get("tran_id") or request.GET.get("tran_id")

    if not tran_id:
        return Response({"error": "Transaction ID not found"}, status=400)

    try:
        adoption_id = tran_id.split("_")[1]
        adoption = AdoptionHistory.objects.get(id=adoption_id)
        user = adoption.adopt.user

        Payment.objects.create(
            user=user,
            adoption=adoption,
            amount=adoption.pet.adoption_cost,
            transaction_id=tran_id,
            status="Completed",
        )

        return redirect(f"{main_settings.FRONTEND_URL}/dashboard/payment/success/")
    except AdoptionHistory.DoesNotExist:
        return Response({"error": "Adoption not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


class PaymentHistory(viewsets.generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-created_at")


class HasAdoptedPet(APIView):
    """
    Check if the authenticated user has adopted a specific pet.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pet_id):
        user = request.user
        has_adopted = AdoptionHistory.objects.filter(
            adopt__user=user, pet_id=pet_id
        ).exists()
        return Response({"hasAdopted": has_adopted}, status=status.HTTP_200_OK)
