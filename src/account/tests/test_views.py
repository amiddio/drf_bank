from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from config.mixins_test import GeneralTestCaseMixin


class UserTestCase(GeneralTestCaseMixin, APITestCase):

    def setUp(self):
        pass

    def test_user_login(self):
        url = reverse('login')
        data = {'username': 'testuser1', 'password': '12345'}
        response = self.client.post(url, data=data)
        token = Token.objects.get(user__username='testuser1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(token.key)
        self.assertEqual(40, len(token.key))

    def test_user_login_negative(self):
        url = reverse('login')
        data = {'username': 'user_not_exist', 'password': '12345'}
        with self.assertRaises(Token.DoesNotExist):
            self.client.post(url, data=data)
            Token.objects.get(user__username='user_not_exist')

    def test_user_logout(self):
        self.user_login()
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(response.data)

    def test_user_logout_negative(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_detail(self):
        self.user_login()
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            {'id': 1, 'username': 'testuser1', 'first_name': 'john', 'last_name': 'dow',
             'email': 'testuser1@home.local', 'profile': None},
            response.data
        )

    def test_user_update(self):
        self.user_login()
        url = reverse('user-me')
        data = {'username': 'testuser11'}
        response = self.client.put(url, data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user = User.objects.get(pk=1)
        self.assertEqual('testuser11', user.username)

    def test_user_delete(self):
        self.user_login()
        url = reverse('user-me')
        data = {'current_password': '12345'}
        response = self.client.delete(url, data=data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(response.data)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=1)

    def test_user_register(self):
        url = reverse('user-list')
        data = {
            'username': 'john_dow',
            'password': 'Qwerty#1234',
            're_password': 'Qwerty#1234',
            'first_name': 'john',
            'last_name': 'dow',
            'email': 'john.dow@home.local',
            'account_type': 1,
            'gender': 'M',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(
            {'id': 2, 'username': 'john_dow', 'first_name': 'john', 'last_name': 'dow', 'email': 'john.dow@home.local'},
            response.data
        )
        user = User.objects.get(pk=2)
        self.assertEqual('john_dow', user.username)
        self.assertEqual(1, user.profile.account_type.pk)
        self.assertEqual('M', user.profile.gender)


class AccountTypeTestCase(GeneralTestCaseMixin, APITestCase):

    def setUp(self):
        pass

    def test_account_type_list(self):
        url = reverse('account:account_types')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))
