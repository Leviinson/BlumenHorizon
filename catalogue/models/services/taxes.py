from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.base_models import TimeStampAdbstractModel


class TaxPercent(TimeStampAdbstractModel):
    value = models.IntegerField(
        verbose_name="НДС",
        help_text="Рассчитывается после начисления налога",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        unique=True,
        default=7,
    )
    stripe_id = models.CharField(
        verbose_name="ID налога в Stripe",
        help_text="Нужно запросить у нашего администратора Stripe",
        unique=True,
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.value}% НДС"

    class Meta:
        verbose_name = "НАЛОГ НДС"
        verbose_name_plural = "НАЛОГИ НДС"
