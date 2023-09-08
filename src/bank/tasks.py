from decimal import Decimal

from celery import shared_task
from django.db import transaction
from django.db.models import F

from bank.models import TransferHistory
from bank.services.account_service import AccountService
from bank.services.commission_income_service import CommissionIncomeService
from bank.services.merchant_service import MerchantService
from bank.services.transfer_history_service import TransferHistoryService


@shared_task
def money_transfer_task(account_from, account_to, amount):
    account_from = AccountService.get_by_account_name(name=account_from)
    account_to = AccountService.get_by_account_name(name=account_to)
    commission = AccountService.calculate_commission(account_from=account_from, account_to=account_to, amount=amount)
    with transaction.atomic():
        # Make money transfer between accounts
        account_from.amount = F('amount') - (Decimal(amount) + commission)
        account_to.amount = F('amount') + Decimal(amount)
        account_from.save()
        account_to.save()
        # Save bank commission, if it's not 0.00
        if commission:
            CommissionIncomeService.add(account=account_from, commission=commission)
        # Save transfer to history
        TransferHistoryService.add(
            action=TransferHistory.SEND,
            account=account_from,
            account_external=account_to.name,
            amount=str('-' + amount),
            commission=commission
        )
        TransferHistoryService.add(
            action=TransferHistory.RECEIVE,
            account=account_to,
            account_external=account_from.name,
            amount=str(amount)
        )


@shared_task
def pay_a_bill_task(merchant_id, account, amount):
    merchant = MerchantService.get_by_id(pk=merchant_id)
    account = AccountService.get_by_account_name(name=account)
    with transaction.atomic():
        # Make Pay a bill transfer
        account.amount = F('amount') - (Decimal(amount) + merchant.commission)
        account.save()
        # Save bank commission, if it's not 0.00
        if merchant.commission:
            CommissionIncomeService.add(account=account, commission=merchant.commission)
        # Save transfer to history
        TransferHistoryService.add(
            action=TransferHistory.SEND,
            account=account,
            account_external=merchant.name,
            amount=str('-' + amount),
            commission=merchant.commission
        )
