from django.conf import settings
from django.db import models


class AccountType(models.Model):
    """
    Модель типа акаунта пользователей.
    Например: Бизнес или Индивидуальный
    """

    name = models.CharField(max_length=50)
    commission = models.FloatField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Модель Profile расширяет стандартную модель User дополнительными полями"""

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    gender = models.CharField(blank=True, null=True, choices=GENDER, max_length=1)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"#{self.user.pk}:{self.user.username}"
