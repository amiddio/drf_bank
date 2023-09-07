from decimal import Decimal

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from bank.models import Account


class AccountService:

    @staticmethod
    def get_by_account_name(name: str):
        return Account.objects.filter(name=name).first()

    @staticmethod
    def get_user_accounts(user: User) -> list[Account]:
        return Account.objects.filter(user=user)

    @staticmethod
    def get_user_account_by_id(user: User, pk: int) -> Account:
        query = AccountService.get_user_accounts(user=user)
        return query.get(pk=pk)

    @staticmethod
    def delete(account: Account) -> None:
        if account.amount > 0:
            raise Exception("Unable to delete. There is money in the account.")
        account.delete()

    @staticmethod
    def calculate_commission(account_from: Account, account_to: Account, amount: Decimal) -> Decimal:
        if account_from.user == account_to.user:
            return Decimal(0)
        bank_commission_value = account_from.user.profile.account_type.commission
        commission = (Decimal(amount) / Decimal(100)) * Decimal(bank_commission_value)
        return commission.quantize(Decimal('0.00'))

    @staticmethod
    def generate_account_number(user: User) -> str:
        letter1 = user.first_name[0]
        letter2 = user.last_name[0]
        account_number = ''.join([letter1, letter2, str(user.pk)]).upper()
        while True:
            account_number_postfix = get_random_string(
                Account.ACCOUNT_LENGTH - len(account_number), allowed_chars='0123456789'
            )
            if not Account.objects.filter(name=account_number + account_number_postfix):
                account_number += account_number_postfix
                break

        return account_number
