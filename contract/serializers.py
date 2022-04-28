from contract.models import Contract
from framework.module.BaseMixin import BaseModelSerializerMixin


class ContractSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Contract
        exclude = ('deleted',)
