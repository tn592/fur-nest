from pet.models import Pet, Category
from pet.serializers import PetSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from pet.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

# from api.permissions import FullDjangoModelPermission


class PetViewSet(ModelViewSet):
    serializer_class = PetSerializer
    pagination_class = DefaultPagination
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Pet.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(pet_count=Count("pets")).all()
    serializer_class = CategorySerializer
