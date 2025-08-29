from django_filters.rest_framework import FilterSet
from pet.models import Pet


class PetFilter(FilterSet):
    class Meta:
        model = Pet
        fields = {"category_id": ["exact"], "price": ["gt", "lt"]}
