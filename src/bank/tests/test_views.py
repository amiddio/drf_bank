from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from bank.models import Merchant
from bank.services.account_service import AccountService
from config.mixins_test import GeneralTestCaseMixin
from rest_framework.test import APITestCase
from bank.tasks import money_transfer_task
from config.paginations import TransferHistoryPagination


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


class TransferAPITestCase(GeneralTestCaseMixin, APITestCase):

    def test_transfer(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=100)
        # Checking only POST data
        data = {
            'account_from': accounts[0].name,
            'account_to': accounts[1].name,
            'amount': '25',
        }
        response = self.client.post(reverse('bank:transfer'), data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'result': True}, response.data)


class PayABillAPITestCase(GeneralTestCaseMixin, APITestCase):

    def test_pay_a_bill(self):
        # Created accounts
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        account = AccountService.get_user_accounts(user=user)[0]
        # Added amount
        self.add_amount_to_account(account_id=account.pk, amount=100)
        merchant = Merchant.objects.get(name="Electricity Company")
        # Checking only POST data
        data = {
            'merchant_id': merchant.pk,
            'account': account.name,
            'amount': '10',
        }
        response = self.client.post(reverse('bank:pay_a_bill'), data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'result': True}, response.data)


class TransferHistoryTestCase(GeneralTestCaseMixin, APITestCase):

    def test_list_of_history(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=100)
        # Some transactions
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='10')
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='7')
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='25')
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='5')
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='12')
        response = self.client.get(reverse('bank:transfer_history'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(10, response.data.get('count'))
        self.assertTrue(response.data.get('next').endswith('?page=2'))
        self.assertFalse(response.data.get('previous'))
        self.assertEqual(TransferHistoryPagination.page_size, len(response.data.get('results')))


class MerchantTestCase(GeneralTestCaseMixin, APITestCase):

    def test_list_of_merchants(self):
        response = self.client.get(reverse('bank:merchant'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))
