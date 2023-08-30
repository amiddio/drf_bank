from rest_framework.generics import ListAPIView

from account.models import AccountType
from account.serializers import AccountTypeSerializer


class AccountTypeListAPIView(ListAPIView):
    """Представление вывода списка типов акаунтов пользователей"""

    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
