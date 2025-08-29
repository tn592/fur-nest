from rest_framework import viewsets, permissions
from adoption.models import AdoptionHistory, Adopt
from adoption.serializers import AdoptionHistorySerializer, CreateAdoptionSerializer
from drf_yasg.utils import swagger_auto_schema


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
        operation_description="This allow an admin or customer to adopt a pet",
        request_body=AdoptionHistorySerializer,
        responses={201: AdoptionHistorySerializer, 400: "Bad Request"},
    )
    def perform_create(self, serializer):
        user = self.request.user
        adopt = Adopt.objects.filter(user=user).first()
        if not adopt:
            adopt = Adopt.objects.create(user=user)

        serializer.save(adopt=adopt)
