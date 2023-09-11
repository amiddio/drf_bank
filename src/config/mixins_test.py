from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

from account.models import AccountType, Profile


class GeneralTestCaseMixin:

    @classmethod
    def setUpTestData(cls):
        account_type1 = AccountType.objects.create(name='Personal', commission='1')
        AccountType.objects.create(name='Business', commission='3')
        user = User.objects.create_user(
            username='testuser1', password='12345', email='testuser1@home.local',
            first_name='john', last_name='dow'
        )
        Profile.objects.create(gender='M', account_type=account_type1, user=user)

    def setUp(self):
        self.user_login()

    def user_login(self):
        self.client.post(reverse('login'), data={'username': 'testuser1', 'password': '12345'})
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
