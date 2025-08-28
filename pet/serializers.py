from decimal import Decimal
from rest_framework import serializers
from pet.models import Category, Pet
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "pet_count"]

    product_count = serializers.IntegerField(
        read_only=True, help_text="Return the number of pets in this category"
    )


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "category",
            "breed",
            "age",
            "description",
            "availability",
            "price",
        ]  # other

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could not be negative")
        return price


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_current_user_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def get_current_user_name(self, obj):
        return obj.get_full_name()
