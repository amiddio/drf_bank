from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from account.models import AccountType, Profile


class GeneralTestCaseMixin:

    @classmethod
    def setUpTestData(cls):
        account_type1 = AccountType.objects.create(name='Personal', commission='1')
        account_type2 = AccountType.objects.create(name='Business', commission='3')
        user1 = User.objects.create_user(
            username='testuser1', password='12345', email='testuser1@home.local',
            first_name='john', last_name='dow'
        )
        user2 = User.objects.create_user(
            username='testuser2', password='12345', email='testuser2@home.local',
            first_name='michael', last_name='smith'
        )
        Profile.objects.create(gender='M', account_type=account_type1, user=user1)
        Profile.objects.create(gender='M', account_type=account_type2, user=user2)

    def setUp(self):
        self.user_login()

    def user_login(self, username='testuser1'):
        self.client.post(reverse('login'), data={'username': username, 'password': '12345'})
        token = Token.objects.get(user__username=username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_account(self):
        return self.client.post(reverse('bank:account-list'))

    def add_amount_to_account(self, account_id, amount):
        return self.client.patch(
            reverse('bank:account-add-amount', args=(account_id,)),
            data={'amount': amount}
        )

    def get_user_by_username(self, username):
        return User.objects.get(username=username)
