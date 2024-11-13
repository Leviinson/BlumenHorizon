from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.base_models import TimeStampAdbstractModel


class MainPageSliderImages(models.Model):
    image = models.ImageField(
        upload_to="mainpage-slider/",
        verbose_name="Фото на главном слайде",
    )
    is_active = models.BooleanField(default=False, verbose_name="Активное?")
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = "Фото слайдера главной страницы"
        verbose_name_plural = "Фотографии слайдера главной страницы"

    def __str__(self):
        return f"{self.image} - {"Активно" if self.is_active else "Неактивно"}"


class IndividualOrder(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="individual_orders",
        verbose_name="Связанный аккаунт",
        null=True,
        blank=False,
    )
    first_name = models.CharField(max_length=40, verbose_name="Имя")
    contact_method = models.TextField(
        max_length=100,
        verbose_name=_("Способ связи с клиентом"),
    )
    recall_me = models.BooleanField(
        verbose_name="Разрешил ли клиент звонить ему", default=False
    )

    class Meta:
        verbose_name = "Индивидуальный заказ"
        verbose_name_plural = "Индивидуальные заказы"

    def __str__(self):
        return f"{self.first_name} {self.phonenumber}"


class SeoBlock(TimeStampAdbstractModel, models.Model):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="seoblock/",
    )
    image_alt = models.CharField(max_length=100, verbose_name="Описание картинки")

    class Meta:
        verbose_name = "СЕО Блок"
        verbose_name_plural = "СЕО Блоки"

    def __str__(self):
        return f"{self.image} ...... {self.alt}"
