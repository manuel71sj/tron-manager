from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        abstract = True
