from django.contrib.auth.models import User
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from django.db import IntegrityError, transaction
from rest_framework import serializers

from account.models import Profile, AccountType


class AccountTypeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер типов акаунта
    """

    class Meta:
        model = AccountType
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериалайзер профиля пользователя
    """

    account_type = AccountTypeSerializer()
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('gender', 'gender_display', 'account_type')

    def get_gender_display(self, obj):
        """Возвращает человекопонятное имя пола пользователя"""
        return obj.get_gender_display()


class CustomUserSerializer(UserSerializer):
    """
    Переопределяем djoser-й сериалайзер отображения пользователя,
    для добавления в него дополнительных полей
    """

    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'profile'
        )


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    """
    Переопределяем djoser-й сериалайзер создания пользователя.
    Т.к. необходимо, при создании пользователя, передавать дополнительные поля.
    """

    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    account_type = serializers.IntegerField(write_only=True)
    gender = serializers.CharField(write_only=True, min_length=1, max_length=1)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'email', 'account_type', 'gender'
        )

    def validate(self, attrs):
        self.account_type = attrs.pop('account_type', None)
        self.gender = attrs.pop('gender', None)
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = self.perform_create(validated_data)
                self._create_profile(user=user)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def _create_profile(self, user):
        """Создание профайла пользователя"""
        account_type = AccountType.objects.get(pk=self.account_type)
        Profile.objects.create(user=user, gender=self.gender, account_type=account_type)
