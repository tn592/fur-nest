from rest_framework import serializers
from adoption.models import Adopt, AdoptionHistory, Payment
from pet.models import Pet
from pet.serializers import PetImageSerializer


class SimplePetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "category", "price", "images"]


class AdoptionHistorySerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer(read_only=True)
    adopted_at = serializers.SerializerMethodField()

    class Meta:
        model = AdoptionHistory
        fields = ["id", "pet", "adopted_at", "price"]

    def get_adopted_at(self, obj):
        return obj.adopt.adopted_at


class CreateAdoptionSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = AdoptionHistory
        fields = ["pet_id"]

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Pet with id {value} does not exist")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        pet_id = validated_data["pet_id"]
        pet = Pet.objects.get(id=pet_id)

        adopt = Adopt.objects.filter(user=user).first()
        if not adopt:
            adopt = Adopt.objects.create(user=user)

        if pet.price > user.account_balance:
            raise serializers.ValidationError(
                "You do not have sufficient balance to adopt this pet"
            )

        if AdoptionHistory.objects.filter(adopt=adopt, pet=pet).exists():
            raise serializers.ValidationError("already adopted this pet")

        user.account_balance -= pet.price
        user.save(update_fields=["account_balance"])

        adoption_history = AdoptionHistory.objects.create(
            adopt=adopt, pet=pet, price=pet.price
        )

        pet.availability = False
        pet.save(update_fields=["availability"])

        return adoption_history


class PaymentSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "pet", "amount", "transaction_id", "status", "created_at"]
