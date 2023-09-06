from rest_framework import serializers

from bank.models import Account
from bank.services.account_service import AccountService


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransferFromSerializer(serializers.Serializer):
    account_from = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def validate(self, data):
        account = AccountService.get_by_account_name(name=data.get('account_from'))
        if not account:
            raise serializers.ValidationError({'account_from': "Account From not exist"})
        if account.user.id != self.context['request'].user.id:
            raise serializers.ValidationError({
                'account_from': f"This user has not permissions to '{data.get('account_from')}'"
            })
        if account.amount < data.get('amount'):
            raise serializers.ValidationError({'account_from': "There are not enough funds in the account"})
        return data


class TransferToSerializer(serializers.Serializer):
    account_to = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)

    def validate(self, data):
        account = AccountService.get_by_account_name(name=data.get('account_to'))
        if not account:
            raise serializers.ValidationError({'account_from': "Account From not exist"})
        return data
