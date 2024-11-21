from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalogue.models import Bouquet, Product, generate_sku
from core.base_models import TimeStampAdbstractModel


class Order(TimeStampAdbstractModel, models.Model):
    STATUS_CHOICES = [
        ("processing", _("В обработке")),
        ("declined", _("Отказан")),
        ("awaiting_payment", _("Ожидание оплаты")),
        ("shipping", _("В доставке")),
        ("delivered", _("Доставлен")),
    ]
    user = models.ForeignKey(
        get_user_model(),
        related_name="orders",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
    )
    clarify_address = models.BooleanField(default=False, verbose_name="Уточнить адрес?")
    country = models.CharField(verbose_name="Страна", max_length=40, null=True)
    city = models.CharField(verbose_name="Город", max_length=40, null=True)
    email = models.EmailField(verbose_name="Почта")
    postal_code = models.CharField(
        verbose_name="Почтовый индекс", max_length=40, null=True
    )
    street = models.CharField(verbose_name="Улица", max_length=255, null=True)
    building = models.CharField(verbose_name="Здание", max_length=40, null=True)
    flat = models.CharField(verbose_name="Квартира/офис", max_length=40, null=True)
    recipient_name = models.CharField(verbose_name="Имя получателя", max_length=80)
    recipient_phonenumber = models.CharField(
        verbose_name="Номер телефона получателя", max_length=30
    )
    is_recipient = models.BooleanField(
        default=False, verbose_name="Заказчик - получатель?"
    )
    is_surprise = models.BooleanField(
        default=False, verbose_name="Доставка с сюрпризом?"
    )
    code = models.CharField(
        max_length=60, verbose_name="Код заказа", default=generate_sku
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="awaiting_payment",
        verbose_name="Статус заказа",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.code} - {self.status}"


class OrderProducts(TimeStampAdbstractModel, models.Model):
    order = models.ForeignKey(
        Order, related_name="products", verbose_name="Заказ", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product, related_name="orders", verbose_name="Продукт", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Продукт в заказе"
        verbose_name_plural = "Продукты в заказах"

    def __str__(self):
        return f"{self.pk}"


class OrderBouquets(TimeStampAdbstractModel, models.Model):
    order = models.ForeignKey(
        Order, related_name="bouquets", verbose_name="Заказ", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Bouquet, related_name="orders", verbose_name="Букет", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Букет в заказе"
        verbose_name_plural = "Букеты в заказах"

        def __str__(self):
            return f"{self.pk}"
