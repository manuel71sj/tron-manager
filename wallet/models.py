from django.db import models
from django.utils.translation import gettext_lazy as _

from framework.module.BaseMixin import BaseModelMixin
from framework.user.models import User


# Create your models here.


class Wallet(BaseModelMixin):
    # _id = ObjectIdField()

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, verbose_name=_("user"))

    address = models.CharField(_('지갑주소'), max_length=34, null=False)
    private_key = models.CharField(_('개인키'), max_length=64, null=False)
    passphrase = models.CharField(_('암호'), max_length=255, null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('지갑')
        verbose_name_plural = _('지갑')

    def __str__(self):
        return '%s(%s)' % (self.user.email, self.address)
