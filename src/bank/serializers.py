from rest_framework import serializers

from bank.models import Account
from bank.services.account_service import AccountService


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransferSerializer(serializers.Serializer):
    account_from = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    account_to = serializers.CharField(max_length=Account.ACCOUNT_LENGTH)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def validate(self, data):
        account_from = AccountService.get_by_account_name(name=data.get('account_from'))
        account_to = AccountService.get_by_account_name(name=data.get('account_to'))
        commission = AccountService.calculate_commission(
            account_from=account_from, account_to=account_to, amount=data.get('amount')
        )
        if not account_from:
            raise serializers.ValidationError({'account_from': "Account From not exist"})
        if not account_to:
            raise serializers.ValidationError({'account_to': "Account To not exist"})
        if account_from.user.id != self.context['request'].user.id:
            raise serializers.ValidationError({
                'account_from': f"This user has not permissions to '{data.get('account_from')}'"
            })
        if account_from.amount < (data.get('amount') + commission):
            raise serializers.ValidationError({'account_from': "There are not enough funds in the account"})
        return data
