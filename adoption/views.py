from rest_framework import viewsets, permissions
from adoption.models import AdoptionHistory
from adoption.serializers import AdoptionHistorySerializer, CreateAdoptionSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response


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
