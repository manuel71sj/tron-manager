from rest_framework import serializers

from framework.module.BaseMixin import BaseModelSerializerMixin
from wallet.models import Wallet


class WalletSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Wallet
        exclude = ('deleted',)


class WalletCreateSerializer(serializers.Serializer):
    passphrase = serializers.CharField(required=False, max_length=255, allow_null=True)
