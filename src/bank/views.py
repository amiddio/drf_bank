from decimal import Decimal

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bank.models import Account
from bank.serializers import AccountSerializer, TransferSerializer
from bank.services.account_service import AccountService
from bank.tasks import money_transfer_task


class AccountViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AccountService.get_user_accounts(user=self.request.user)

    def get_object(self, pk):
        return AccountService.get_user_account_by_id(user=self.request.user, pk=pk)

    def list(self, request):
        serializer_data = AccountSerializer(self.get_queryset(), many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def create(self, request):
        data = {
            'name': AccountService.generate_account_number(user=self.request.user),
            'user': self.request.user.pk
        }
        serializer = AccountSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'result': True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            AccountService.delete(account=self.get_object(pk=pk))
            return Response({'result': True}, status=status.HTTP_200_OK)
        except (Account.DoesNotExist, Exception) as e:
            return Response({'result': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def add_amount(self, request, pk=None):
        try:
            instance = self.get_object(pk=pk)
            data = {
                'amount': instance.amount + abs(Decimal(request.data.get('amount')))
            }
            serializer = AccountSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        except Account.DoesNotExist as e:
            return Response({'result': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransferAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TransferSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Money transfer task
        money_transfer_task.delay(
            account_from=serializer.data.get('account_from'),
            account_to=serializer.data.get('account_to'),
            amount=serializer.data.get('amount')
        )

        return Response({'result': True}, status=status.HTTP_200_OK)
