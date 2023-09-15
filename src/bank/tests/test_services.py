from decimal import Decimal

from django.db.models import QuerySet
from rest_framework.test import APITestCase

from bank.models import Account
from bank.services.account_service import AccountService
from config.mixins_test import GeneralTestCaseMixin


class AccountServiceTestCase(GeneralTestCaseMixin, APITestCase):

    def setUp(self):
        self.user_login(username='testuser2')
        self.create_account()
        self.create_account()
        super().setUp()
        self.user = self.get_user_by_username(username='testuser1')
        self.create_account()
        self.create_account()
        self.create_account()

    def test_get_by_account_name_method(self):
        account = AccountService.get_user_accounts(user=self.user)[0]
        result = AccountService.get_by_account_name(name=account.name)
        self.assertIsInstance(result, Account)
        self.assertEqual(result.name, account.name)

    def test_get_user_accounts_method(self):
        accounts = AccountService.get_user_accounts(user=self.user)
        self.assertIsInstance(accounts, QuerySet)
        self.assertIsInstance(accounts[0], Account)
        self.assertEqual(3, len(accounts))

    def test_get_user_account_by_id_method(self):
        account = AccountService.get_user_accounts(user=self.user)[0]
        result = AccountService.get_user_account_by_id(user=self.user, pk=account.pk)
        self.assertIsInstance(result, Account)
        self.assertEqual(result.pk, account.pk)

    def test_delete_method(self):
        account = AccountService.get_user_accounts(user=self.user)[0]
        AccountService.delete(account=account)
        accounts = AccountService.get_user_accounts(user=self.user)
        self.assertEqual(2, len(accounts))

    def test_delete_method_negative(self):
        account = AccountService.get_user_accounts(user=self.user)[0]
        account.amount = 10
        account.save()
        with self.assertRaises(Exception):
            AccountService.delete(account=account)
        accounts = AccountService.get_user_accounts(user=self.user)
        self.assertEqual(3, len(accounts))

    def test_calculate_commission_method(self):
        account_from = AccountService.get_user_accounts(user=self.user)[0]
        account_from.amount = 100
        account_from.save()
        account_from.refresh_from_db()
        account_to = AccountService.get_user_accounts(
            user=self.get_user_by_username(username='testuser2')
        )[0]
        commission = AccountService.calculate_commission(account_from, account_to, Decimal(50))
        self.assertEqual(0.5, commission)
        account_to = AccountService.get_user_accounts(user=self.user)[1]
        commission = AccountService.calculate_commission(account_from, account_to, Decimal(10))
        self.assertEqual(0, commission)

    def test_generate_account_number_method(self):
        account_number = AccountService.generate_account_number(user=self.user)
        self.assertTrue(Account.ACCOUNT_LENGTH == len(account_number))
