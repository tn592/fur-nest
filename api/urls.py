from django.urls import path, include
from rest_framework import routers
from pet.views import PetViewSet, CategoryViewSet
from adoption.views import AdoptionHistoryViewSet

router = routers.DefaultRouter()
router.register("pets", PetViewSet, basename="pets")
router.register("categories", CategoryViewSet)
router.register("adoptions", AdoptionHistoryViewSet, basename="adoptions")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
