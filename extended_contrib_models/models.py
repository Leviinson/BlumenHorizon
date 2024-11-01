from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ExtendedSite(models.Model):
    site = models.OneToOneField(Site, related_name="extended", on_delete=models.PROTECT)
    currency_code = models.CharField(
        max_length=5, verbose_name="Код валюты", unique=True
    )
    currency_symbol = models.CharField(max_length=5, verbose_name="Знак валюты")
    country = models.CharField(max_length=40, verbose_name="Название страны")
    city = models.CharField(max_length=40, verbose_name="Название города")

    def __str__(self):
        return f"{self.site.name} | {self.site.domain}"

    class Meta:
        verbose_name = "Расширенные данные о сайте"
        verbose_name_plural = verbose_name


@receiver(post_save, sender=Site)
def create_extended_site(sender, instance, created, **kwargs):
    if not ExtendedSite.objects.filter(site=instance).exists():
        ExtendedSite.objects.create(
            site=instance, currency_code="USD", currency_symbol="$", country="Германия", city="Берлин"
        )
