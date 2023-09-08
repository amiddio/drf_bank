from django.contrib.auth.models import User

from bank.models import TransferHistory


class TransferHistoryService:

    @staticmethod
    def add(action, account, account_external, amount, commission=0):
        TransferHistory.objects.create(
            action=action,
            account=account.name,
            account_external=account_external.name,
            amount=amount,
            commission=commission,
            user=account.user
        )

    @staticmethod
    def get_all(user: User) -> list[TransferHistory]:
        return TransferHistory.objects.filter(user=user)
