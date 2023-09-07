from decimal import Decimal

from bank.models import Account, CommissionIncome


class CommissionIncomeService:

    @staticmethod
    def add(account: Account, commission: Decimal) -> None:
        CommissionIncome.objects.create(commission=commission, account=account)

