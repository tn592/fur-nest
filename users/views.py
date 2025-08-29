from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import DepositSerializer, UserSerializer
from users.models import User
from drf_yasg.utils import swagger_auto_schema


class AccountBalanceViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="This allow customer to add money to the account",
        operation_description="This allow to add money for future adoption",
        request_body=DepositSerializer,
        responses={201: DepositSerializer, 400: "Bad Request"},
    )
    @action(detail=False, methods=["post"])
    def deposit(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            values = serializer.validated_data["values"]
            user = request.user
            user.account_balance += values
            user.save()
            return Response(
                {
                    "account_balance": user.account_balance,
                }
            )
