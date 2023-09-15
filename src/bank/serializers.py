from rest_framework import serializers

from bank.models import Account, TransferHistory, Merchant
from bank.services.account_service import AccountService
from bank.services.merchant_service import MerchantService


class AccountSerializer(serializers.ModelSerializer):
    """
    Сериалайзер банковских аккаунтов пользователей
    """

    class Meta:
        model = Account
        fields = '__all__'


class TransferHistorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер истории транзакций пользователей
    """

    class Meta:
        model = TransferHistory
        fields = '__all__'


class MerchantSerializer(serializers.ModelSerializer):
    """
    Сериалайзер списка мерчантов
    """

    class Meta:
        model = Merchant
        fields = '__all__'


class TransferSerializer(serializers.Serializer):
    """
    Сериалайзер денежных переводов
    """

    account_from = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    account_to = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def validate(self, data):
        account_from = AccountService.get_by_account_name(name=data.get('account_from'))
        account_to = AccountService.get_by_account_name(name=data.get('account_to'))
        amount = data.get('amount')
        commission = AccountService.calculate_commission(
            account_from=account_from, account_to=account_to, amount=data.get('amount')
        )

        if not account_from:
            raise serializers.ValidationError({'account_from': "Account From not exist"})
        if not account_to:
            raise serializers.ValidationError({'account_to': "Account To not exist"})
        if amount <= 0:
            raise serializers.ValidationError({'amount': "Amount must be greater than zero"})
        if account_from.user.id != self.context['request'].user.id:
            raise serializers.ValidationError({
                'account_from': f"This user has not permissions to '{data.get('account_from')}'"
            })
        if account_from.amount < (amount + commission):
            raise serializers.ValidationError({'account_from': "There are not enough funds in the account"})
        return data


class PayABillSerializer(serializers.Serializer):
    """
    Сериалайзер оплаты счетов
    """

    merchant_id = serializers.IntegerField()
    account = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def validate(self, data):
        merchant = MerchantService.get_by_id(pk=data.get('merchant_id'))
        account = AccountService.get_by_account_name(name=data.get('account'))
        amount = data.get('amount')

        if not merchant:
            raise serializers.ValidationError({'merchant_id': "Merchant not exist"})
        if not account:
            raise serializers.ValidationError({'account': "Account not exist"})
        if amount <= 0:
            raise serializers.ValidationError({'amount': "Amount must be greater than zero"})
        if account.user.id != self.context['request'].user.id:
            raise serializers.ValidationError({
                'account': f"This user has not permissions to '{data.get('account')}'"
            })
        if account.amount < (amount + merchant.commission):
            raise serializers.ValidationError({'account': "There are not enough funds in the account"})

        return data
