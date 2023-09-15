from bank.models import Merchant
from bank.services.account_service import AccountService
from bank.tasks import money_transfer_task, pay_a_bill_task
from config.mixins_test import GeneralTestCaseMixin

from rest_framework.test import APITestCase


class TasksTestCase(GeneralTestCaseMixin, APITestCase):

    def test_money_transfer_task(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=100)
        # Made transfer
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='25')
        accounts[0].refresh_from_db()
        accounts[1].refresh_from_db()
        # Asserting
        self.assertEqual(75, accounts[0].amount)
        self.assertEqual(25, accounts[1].amount)

    def test_pay_a_bill_task(self):
        # Created accounts
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        account = AccountService.get_user_accounts(user=user)[0]
        merchant = Merchant.objects.get(name="Electricity Company")
        # Added amount
        self.add_amount_to_account(account_id=account.pk, amount=100)
        pay_a_bill_task(merchant_id=merchant.pk, account=account.name, amount='10')
        account.refresh_from_db()
        self.assertEqual(89.50, account.amount)
