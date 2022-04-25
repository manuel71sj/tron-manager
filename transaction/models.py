from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from framework.module.BaseMixin import BaseModelMixin
from framework.module.choices import ResultChoices, ConfirmedChoices, TxTypeChoices
from framework.user.models import User


class Transaction(BaseModelMixin):
    # babe489c3ae34c87ac764018a0ec5f644745d7d795589bc102a0b41edf0feb7f
    tx_id = models.CharField(_('트랜잭션ID'), max_length=64, null=False)
    result = models.CharField(_('결과'), choices=ResultChoices.choices, default=ResultChoices.FAILED, max_length=7,
                              help_text=_('트랜잭션 결과값'))
    status = models.CharField(_('상태'), choices=ConfirmedChoices.choices, default=ConfirmedChoices.UNCONFIRMED,
                              max_length=11, help_text=_('컨펌상태에 의한 결과값 ( > 20 일 경우 True'))

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("user"))

    tx_type = models.CharField(_('거래구분'), choices=TxTypeChoices.choices, default=TxTypeChoices.CREATE_CONTRACT,
                               max_length=21)
    json_result = models.JSONField(_('결과JSON'), null=True, blank=True)

    contract_address = models.CharField(_('컨트랙트 주소'), max_length=34, null=True, blank=True)

    class Meta:
        verbose_name = _('트랜잭션')
        verbose_name_plural = _('트랜잭션')

    @classmethod
    def crate_contract(cls, tx_id: str, result: dict, user: User):
        save = cls(
            tx_id=tx_id,
            result=result['receipt']['result'],
            user=user,
            tx_type=TxTypeChoices.CREATE_CONTRACT,
            json_result=result,
            contract_address=result['contract_address']
        )

        save.save()

        return save
