from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampAdbstractModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания"),
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления"),
        editable=False,
    )

    class Meta:
        abstract = True
