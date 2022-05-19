from framework.module.BaseMixin import BaseModelSerializerMixin
from transaction.models import Transaction


class TransactionSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Transaction
        exclude = ("deleted",)
