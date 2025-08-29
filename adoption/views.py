from rest_framework import viewsets, permissions
from adoption.models import AdoptionHistory, Adopt
from adoption.serializers import AdoptionHistorySerializer, CreateAdoptionSerializer


class AdoptionHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AdoptionHistory.objects.filter(
            adopt__user=self.request.user
        ).select_related("pet")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAdoptionSerializer
        return AdoptionHistorySerializer

    def perform_create(self, serializer):
        user = self.request.user
        adopt = Adopt.objects.filter(user=user).first()
        if not adopt:
            adopt = Adopt.objects.create(user=user)

        serializer.save(adopt=adopt)
