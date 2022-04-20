from framework.module.BaseMixin import BaseModelSerializerMixin
from wallet.models import Wallet


class WalletSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Wallet
        exclude = ('deleted',)
        # fields = '__all__'
