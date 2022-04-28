from django.db import models
from django.utils.translation import gettext_lazy as _
from tronpy import Contract as TronContract

from framework.module.BaseMixin import BaseModelMixin
from framework.module.choices import TrcTypeChoices
from framework.user.models import User
from transaction.models import Transaction
from wallet.models import Wallet


# Create your models here.


class Contract(BaseModelMixin):
    tx = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('트랜잭션'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("user"))
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('지갑'))

    contract_address = models.CharField(_('컨트랙트 주소'), max_length=34, null=True, blank=True)
    trc_type = models.CharField(_('TRC 타입'), choices=TrcTypeChoices.choices, default=TrcTypeChoices.TRC721,
                                max_length=6)

    name = models.CharField(_('토큰이름'), max_length=100)
    symbol = models.CharField(_('토큰심볼'), max_length=10)

    json_contract = models.JSONField(_('컨트랙트JSON'), null=True, blank=True)

    class Meta:
        verbose_name = _('컨트랙트')
        verbose_name_plural = _('컨트랙트')

    @classmethod
    def create_nft_contract(cls, tx: Transaction, wallet: Wallet, user: User, contract: TronContract, symbol: str):
        save = cls(
            tx=tx,
            user=user,
            wallet=wallet,
            contract_address=contract.contract_address,
            trc_type=TrcTypeChoices.TRC721,
            name=contract.name,
            symbol=symbol,
            json_contract={
                'abi': contract.abi,
                'name': contract.name,
                'contract_address': contract.contract_address,
                'origin_address': contract.origin_address,
                'origin_energy_limit': contract.origin_energy_limit,
                'owner_address': contract.owner_address,
                'user_resource_percent': contract.user_resource_percent
            },
        )

        save.save()

        return save
