from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase, APIRequestFactory

from bank.models import Merchant
from bank.serializers import AccountSerializer, TransferHistorySerializer, MerchantSerializer, TransferSerializer, \
    PayABillSerializer
from bank.services.account_service import AccountService
from bank.services.transfer_history_service import TransferHistoryService
from bank.tasks import money_transfer_task
from config.mixins_test import GeneralTestCaseMixin


class AccountSerializerTestCase(GeneralTestCaseMixin, APITestCase):

    def test_data_fields(self):
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        account = AccountService.get_user_accounts(user=user)[0]
        serializer = AccountSerializer(account)
        self.assertEqual(
            {'user', 'created', 'id', 'updated', 'name', 'amount'},
            set(serializer.data.keys())
        )


class TransferHistorySerializerTestCase(GeneralTestCaseMixin, APITestCase):

    def test_data_fields(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=100)
        # Some transactions
        money_transfer_task(account_from=accounts[0].name, account_to=accounts[1].name, amount='11')
        item = TransferHistoryService.get_all(user=user)[0]
        serializer = TransferHistorySerializer(item)
        self.assertEqual(
            {'id', 'action', 'account', 'account_external', 'amount', 'commission', 'created', 'user'},
            set(serializer.data.keys())
        )


class MerchantSerializerTestCase(GeneralTestCaseMixin, APITestCase):

    def test_data_fields(self):
        merchant = Merchant.objects.all().first()
        serializer = MerchantSerializer(merchant)
        self.assertEqual(
            {'id', 'name', 'commission'},
            set(serializer.data.keys())
        )


class TransferSerializerTestCase(GeneralTestCaseMixin, APITestCase):

    def test_check_validation(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=100)
        data = {
            'account_from': accounts[0].name,
            'account_to': accounts[1].name,
            'amount': 10,
        }
        request = APIRequestFactory()
        request.user = user
        serializer = TransferSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            {'account_from', 'account_to', 'amount'},
            set(serializer.data.keys())
        )
        self.assertEqual(
            {'account_from': accounts[0].name, 'account_to': accounts[1].name, 'amount': '10.00'},
            serializer.data
        )

    def test_check_validation_negative_not_enough_funds(self):
        # Created accounts
        self.create_account()
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        accounts = AccountService.get_user_accounts(user=user)
        # Added amount
        self.add_amount_to_account(account_id=accounts[0].pk, amount=10)
        data = {
            'account_from': accounts[0].name,
            'account_to': accounts[1].name,
            'amount': 11,
        }
        request = APIRequestFactory()
        request.user = user
        serializer = TransferSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class PayABillSerializerTestCase(GeneralTestCaseMixin, APITestCase):

    def test_check_validation(self):
        # Created accounts
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        account = AccountService.get_user_accounts(user=user)[0]
        merchant = Merchant.objects.get(name="Electricity Company")
        # Added amount
        self.add_amount_to_account(account_id=account.pk, amount=10)
        data = {
            'merchant_id': merchant.pk,
            'account': account.name,
            'amount': 3,
        }
        request = APIRequestFactory()
        request.user = user
        serializer = PayABillSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            {'merchant_id', 'account', 'amount'},
            set(serializer.data.keys())
        )
        self.assertEqual(
            {'merchant_id': merchant.pk, 'account': account.name, 'amount': '3.00'},
            serializer.data
        )

    def test_check_validation_negative_not_enough_funds(self):
        # Created accounts
        self.create_account()
        user = self.get_user_by_username(username='testuser1')
        account = AccountService.get_user_accounts(user=user)[0]
        merchant = Merchant.objects.get(name="Electricity Company")
        # Added amount
        self.add_amount_to_account(account_id=account.pk, amount=10)
        data = {
            'merchant_id': merchant.pk,
            'account': account.name,
            'amount': 11,
        }
        request = APIRequestFactory()
        request.user = user
        serializer = PayABillSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
