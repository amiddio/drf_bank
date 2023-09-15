from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    """
    Модель банковского аккаунта пользователей
    """

    ACCOUNT_LENGTH = 22

    name = models.CharField(max_length=ACCOUNT_LENGTH, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accounts')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class TransferHistory(models.Model):
    """
    История денежных транзакций пользователей
    """

    SEND = 'S'
    RECEIVE = 'R'
    ACTION = (
        (SEND, 'Send'),
        (RECEIVE, 'Receive')
    )
    action = models.CharField(max_length=1, choices=ACTION)
    account = models.CharField(max_length=Account.ACCOUNT_LENGTH)
    account_external = models.CharField(max_length=50)
    amount = models.CharField(max_length=20)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='transfers')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.pk


class CommissionIncome(models.Model):
    """
    Модель коммиссий поступающих банку после денежных переводов пользователей
    """

    commission = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.commission)


class Merchant(models.Model):
    """
    Модель сервисов для оплаты финансовых услуг.
    Например, комунальных.
    """

    name = models.CharField(max_length=50)
    commission = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
