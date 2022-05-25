from rest_framework import serializers

from framework.module.BaseMixin import BaseModelSerializerMixin
from transaction.models import Transaction


class TransactionSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Transaction
        exclude = ("deleted",)


class SendTrxSerializer(serializers.Serializer):
    """
        [
      {
        "_id": {"$oid": "60ee86cdbf731bb2a5641455"},
        "product_num_id": {"$oid": "60ee86cdbf731bb2a5641453"},
        "reg_date": {"$date": "2021-07-14T15:40:13.789Z"},
        "reg_user": "9ba5a774-3cf7-484c-93e5-8d53984e9e3e",
        "update": "2021-07-14",
        "upload": "Y"
      },
    ]
    """

    from_address = serializers.CharField(required=True, max_length=34, min_length=34)
    to_address = serializers.CharField(required=True, max_length=34, min_length=34)
    amount = serializers.FloatField(required=True)
    message = serializers.CharField(required=False, max_length=256)
    callback_url = serializers.CharField(required=False, max_length=256)


class GetTrxResultByTxId(serializers.Serializer):
    tx_id = serializers.CharField(required=True, max_length=64, min_length=64)
