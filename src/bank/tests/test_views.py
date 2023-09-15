from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from bank.services.account_service import AccountService
from config.mixins_test import GeneralTestCaseMixin
from rest_framework.test import APITestCase


class AccountTestCase(GeneralTestCaseMixin, APITestCase):

    def test_create_account(self):
        # Checked accounts before adding
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        self.assertEqual(0, len(accounts))
        # Generating account
        response = self.create_account()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual({'result': True}, response.data)
        # Checked accounts after adding
        accounts = AccountService.get_user_accounts(user=user)
        self.assertEqual(1, len(accounts))

    def test_list_accounts(self):
        self.create_account()
        self.create_account()
        self.create_account()
        response = self.client.get(reverse('bank:account-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

    def test_account_delete(self):
        # Checked accounts before adding
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        self.assertEqual(0, len(accounts))
        # Creating
        self.create_account()
        account = AccountService.get_user_accounts(user=user)[0]
        # Deleting
        response = self.client.delete(reverse('bank:account-detail', args=(account.pk,)))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'result': True}, response.data)
        # Checked accounts after deleted
        accounts = AccountService.get_user_accounts(user=user)
        self.assertEqual(0, len(accounts))

    def test_account_delete_negative(self):
        # Creating
        self.create_account()
        # Added amount
        self.add_amount_to_account(account_id=1, amount=10)
        # Trying to delete
        response = self.client.delete(reverse('bank:account-detail', args=(1,)))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertFalse(response.data.get('result'))

    def test_add_amount_to_account(self):
        user = self.get_user_by_username(username='testuser1')
        # Creating
        self.create_account()
        # Checked amount before
        account = AccountService.get_user_accounts(user=user)[0]
        self.assertEqual(Decimal(0), account.amount)
        # Added amount
        self.add_amount_to_account(account_id=account.pk, amount=100)
        # Checked amount after
        account.refresh_from_db()
        self.assertEqual(Decimal(100), account.amount)
