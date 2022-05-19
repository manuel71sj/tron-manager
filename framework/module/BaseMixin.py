from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class BaseModelMixin(models.Model):
    deleted = models.BooleanField(_("is_deleted"), default=False)

    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        abstract = True


class BaseModelSerializerMixin(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        abstract = True
