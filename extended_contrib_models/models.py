from colorfield.fields import ColorField
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


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


class Social(models.Model):
    absolute_url = models.URLField(verbose_name="Ссылка на соц. сеть", unique=True)
    outline_hex_code = ColorField(
        verbose_name=_("HEX код цвета обводки (#f4678a к примеру)"),
        help_text=_(
            "Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат)."
        ),
    )
    background_hex_code = ColorField(
        verbose_name=_("HEX код цвета фона (#f4678a к примеру)"),
        help_text=_(
            "Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат)."
        ),
    )
    icon_hex_code = ColorField(
        verbose_name=_("HEX код цвета иконки (#f4678a к примеру)"),
        help_text=_(
            "Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат)."
        ),
    )
    bootstrap_icon = models.CharField(
        max_length=40,
        verbose_name="Название класса иконки",
        help_text="https://icons.getbootstrap.com/",
    )
    extended_site = models.ForeignKey(
        ExtendedSite,
        on_delete=models.PROTECT,
        related_name="socials",
    )

    class Meta:
        verbose_name = "Соц. сеть"
        verbose_name_plural = "Соц. сети"

    def __str__(self):
        return f"{self.bootstrap_icon} - {self.absolute_url}"


@receiver(post_save, sender=Site)
def create_extended_site(sender, instance, created, **kwargs):
    if not ExtendedSite.objects.filter(site=instance).exists():
        ExtendedSite.objects.create(
            site=instance,
            currency_code="USD",
            currency_symbol="$",
            country="Германия",
            city="Берлин",
        )
