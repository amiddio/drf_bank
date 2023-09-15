from collections import OrderedDict

from django.test import TestCase
from django.urls import reverse

from account.models import AccountType
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
        logged_user = self.get_user_by_username('testuser1')
        profile = logged_user.profile
        account_type = profile.account_type
        serializer = ProfileSerializer(profile)
        self.assertEqual(
            {'gender': 'M', 'gender_display': 'Male',
             'account_type': OrderedDict([('id', account_type.pk), ('name', 'Personal')])},
            serializer.data
        )


class CustomUserSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        logged_user = self.get_user_by_username('testuser1')
        serializer = CustomUserSerializer(logged_user)
        self.assertEqual(
            {'id': logged_user.pk, 'username': 'testuser1', 'first_name': 'john', 'last_name': 'dow',
             'email': 'testuser1@home.local', 'profile': OrderedDict([('gender', 'M'), ('gender_display', 'Male'), (
                'account_type', OrderedDict([('id', logged_user.pk), ('name', 'Personal')]))])},
            serializer.data
        )


class CustomUserCreatePasswordRetypeSerializerTestCase(GeneralTestCaseMixin, TestCase):

    def setUp(self):
        pass

    def test_data_fields(self):
        account_type = AccountType.objects.all()[0]
        serializer = CustomUserCreatePasswordRetypeSerializer(data={
            'username': 'john_dow',
            'password': 'Qwerty#1234',
            're_password': 'Qwerty#1234',
            'first_name': 'john',
            'last_name': 'dow',
            'email': 'john.dow@home.local',
            'account_type': account_type.pk,
            'gender': 'M',
        })
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            {'username': 'john_dow', 'first_name': 'john', 'last_name': 'dow', 'email': 'john.dow@home.local'},
            serializer.data
        )
