from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from account.models import AccountType, Profile
from account.serializers import AccountTypeSerializer, ProfileSerializer, CustomUserSerializer, \
    CustomUserCreatePasswordRetypeSerializer
from config.mixins_test import GeneralTestCaseMixin


class AccountTypeSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        url = reverse('account:account_types')
        response = self.client.get(url)
        types = AccountType.objects.all()
        serializer = AccountTypeSerializer(types, many=True)
        self.assertEqual(response.data, serializer.data)


class ProfileSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        profile = Profile.objects.get(pk=1)
        serializer = ProfileSerializer(profile)
        self.assertEqual(
            {'gender': 'M', 'gender_display': 'Male', 'account_type': OrderedDict([('id', 1), ('name', 'Personal')])},
            serializer.data
        )


class CustomUserSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        user = User.objects.get(pk=1)
        serializer = CustomUserSerializer(user)
        self.assertEqual(
            {'id': 1, 'username': 'testuser1', 'first_name': 'john', 'last_name': 'dow',
             'email': 'testuser1@home.local', 'profile': OrderedDict([('gender', 'M'), ('gender_display', 'Male'), (
                'account_type', OrderedDict([('id', 1), ('name', 'Personal')]))])},
            serializer.data
        )


class CustomUserCreatePasswordRetypeSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        user = User.objects.get(pk=1)
        user.re_password = '12345'
        user.password = '12345'
        serializer = CustomUserCreatePasswordRetypeSerializer(data={
            'username': 'john_dow',
            'password': 'Qwerty#1234',
            're_password': 'Qwerty#1234',
            'first_name': 'john',
            'last_name': 'dow',
            'email': 'john.dow@home.local',
            'account_type': 1,
            'gender': 'M',
        })
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            {'username': 'john_dow', 'first_name': 'john', 'last_name': 'dow', 'email': 'john.dow@home.local'},
            serializer.data
        )
