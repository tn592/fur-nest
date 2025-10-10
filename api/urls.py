from django.urls import path, include
from rest_framework import routers
from pet.views import PetImageViewSet, PetViewSet, CategoryViewSet, ReviewViewSet
from adoption.views import AdoptionHistoryViewSet, HasAdoptedPet
from rest_framework_nested import routers
from users.views import AccountBalanceViewset

router = routers.DefaultRouter()
router.register("pets", PetViewSet, basename="pets")
router.register("categories", CategoryViewSet)
router.register("adoptions", AdoptionHistoryViewSet, basename="adoptions")
router.register("balance", AccountBalanceViewset, basename="balance")
pet_router = routers.NestedDefaultRouter(router, "pets", lookup="pet")
pet_router.register("reviews", ReviewViewSet, basename="pet-review")
pet_router.register("images", PetImageViewSet, basename="pet-images")
urlpatterns = [
    path("", include(router.urls)),
    path("", include(pet_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("has-adopted/<int:pet_id>/", HasAdoptedPet.as_view(), name="has-adopted"),
]
