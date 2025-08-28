from django.urls import path, include
from rest_framework_nested import routers
from pet.views import (
    PetViewSet,
    CategoryViewSet,
)


router = routers.DefaultRouter()
router.register("pets", PetViewSet, basename="pets")
router.register("categories", CategoryViewSet)

pet_router = routers.NestedDefaultRouter(router, "pets", lookup="pet")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(pet_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
