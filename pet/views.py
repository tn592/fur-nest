from pet.models import Pet, Category
from pet.serializers import PetSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from pet.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from pet.filters import PetFilter
from drf_yasg.utils import swagger_auto_schema

# from api.permissions import FullDjangoModelPermission


class PetViewSet(ModelViewSet):
    """
    API endpoint for managing pets in the pet-adoption platform
    - Allows authenticated admin to add, update, and delete pets
    - Allows users to adopt and filter pets
    - Support searching by category
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
