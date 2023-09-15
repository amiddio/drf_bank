from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from bank.serializers import AccountSerializer
from bank.services.account_service import AccountService
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
