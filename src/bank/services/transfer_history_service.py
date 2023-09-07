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
