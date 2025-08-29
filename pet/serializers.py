from rest_framework import serializers
from pet.models import Category, Pet, Review
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "pet_count"]

    pet_count = serializers.IntegerField(
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


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name="get_user")

    class Meta:
        model = Review
        fields = ["id", "user", "pet", "ratings", "comment"]
        read_only_fields = ["user", "pet"]

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def validate(self, data):
        request = self.context["request"]
        pet_id = self.context.get("pet_id")
        user = request.user

        from adoption.models import AdoptionHistory

        if not AdoptionHistory.objects.filter(adopt__user=user, pet_id=pet_id).exists():
            raise serializers.ValidationError(
                "You can only review pets you have adopted."
            )

        return data

    def create(self, validated_data):
        pet_id = self.context["pet_id"]
        return Review.objects.create(pet_id=pet_id, **validated_data)
