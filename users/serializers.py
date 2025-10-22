from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers
from adoption.serializers import AdoptionHistorySerializer
from adoption.models import AdoptionHistory
from django.contrib.auth import get_user_model

# from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        ]


class UserSerializer(BaseUserSerializer):
    adoption_history = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUser"
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "account_balance",
            "adoption_history",
            "is_staff",
        ]

    read_only_fields = ["id", "email", "adoption_history", "is_staff"]

    def get_adoption_history(self, obj):
        histories = AdoptionHistory.objects.filter(adopt__user=obj).select_related(
            "pet"
        )
        return AdoptionHistorySerializer(histories, many=True).data


class DepositSerializer(serializers.ModelSerializer):
    values = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = get_user_model()
        fields = ["id", "values"]

    def validate_values(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Deposit value must be greater than zero."
            )
        return value
