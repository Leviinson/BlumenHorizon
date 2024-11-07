from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class MainPageSliderImages(models.Model):
    image = models.ImageField(verbose_name="Фото на главном слайде")
    is_active = models.BooleanField(default=False, verbose_name="Активное?")

    class Meta:
        verbose_name = "Фото слайдера главной страницы"
        verbose_name_plural = "Фотографии слайдера главной страницы"


class IndividualOrder(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="individual_orders",
        verbose_name="Связанный аккаунт",
        null=True,
        blank=False,
    )
    first_name = models.CharField(max_length=40)
    phonenumber = PhoneNumberField(
        max_length=15,
        verbose_name=_("Номер телефона"),
        null=True,
        blank=True,
        unique=True,
    )
