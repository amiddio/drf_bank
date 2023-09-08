from bank.models import Merchant


class MerchantService:

    @staticmethod
    def get_by_id(pk: int) -> Merchant:
        return Merchant.objects.filter(pk=pk).first()
