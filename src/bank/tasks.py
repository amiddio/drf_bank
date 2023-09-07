from celery import shared_task
from django.db import transaction
from django.db.models import F

from bank.services.account_service import AccountService


@shared_task
def money_transfer_task(account_from, account_to, amount):
    account_from = AccountService.get_by_account_name(name=account_from)
    account_to = AccountService.get_by_account_name(name=account_to)
    with transaction.atomic():
        account_from.amount = F('amount') - amount
        account_to.amount = F('amount') + amount
        account_from.save()
        account_to.save()
