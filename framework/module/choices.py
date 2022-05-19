from django.db import models
from django.utils.translation import gettext_lazy as _


class ResultChoices(models.TextChoices):
    SUCCESS = "SUCCESS", _("성공")
    FAILED = "FAILED", _("실패")
    PENDING = "PENDING", _("대기")


class ConfirmedChoices(models.TextChoices):
    CONFIRMED = "CONFIRMED", _("컨펌됨")
    UNCONFIRMED = "UNCONFIRMED", _("컨펌대기중")


class TxTypeChoices(models.TextChoices):
    CREATE_CONTRACT = "CREATE_SMART_CONTRACT", _("스마트컨트랙트 생성")
    SEND_TRX = "SEND_TRX", _("TRX 전송")


class TrcTypeChoices(models.TextChoices):
    TRC10 = "TRC10", _("TRC10")
    TRC20 = "TRC20", _("TRC20")
    TRC721 = "TRC721", _("TRC721")
