from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers
from adoption.serializers import AdoptionHistorySerializer
from adoption.models import AdoptionHistory


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
            "account_balance",
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
        ]

    def get_adoption_history(self, obj):
        # Fetch all adoption histories for this user
        histories = AdoptionHistory.objects.filter(adopt__user=obj).select_related(
            "pet"
        )
        return AdoptionHistorySerializer(histories, many=True).data
