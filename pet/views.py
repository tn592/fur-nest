from pet.models import Pet, Category, Review
from pet.serializers import PetSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from pet.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from pet.filters import PetFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from pet.permissions import IsReviewAuthorOrReadonly

# from api.permissions import FullDjangoModelPermission


class PetViewSet(ModelViewSet):
    """
    API endpoint for managing pets in the pet-adoption platform
    - Allows authenticated admin to add, update, and delete pets
    - Allows users to adopt and filter pets
    """

    serializer_class = PetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PetFilter
    ordering_fields = ["price"]
    pagination_class = DefaultPagination
    search_fields = ["name", "description"]
    ordering_fields = ["price"]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Pet.objects.all()

    @swagger_auto_schema(operation_summary="Retrive a list of pets")
    def list(self, request, *args, **kwargs):
        """
        Retrive all the pets
        - Support searching by category
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="add a pet by admin and customer",
        operation_description="This allow an admin to add a pet",
        request_body=PetSerializer,
        responses={201: PetSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can add pet"""
        return super().create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(pet_count=Count("pets")).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(pet_id=self.kwargs.get("pet_pk"))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["pet_id"] = self.kwargs.get("pet_pk")
        return context
