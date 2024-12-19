from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from telegram.helpers import escape_markdown

from catalogue.models import Bouquet, Product, generate_sku
from core.base_models import TimeStampAdbstractModel
from tg_bot import send_message_to_telegram


class Order(TimeStampAdbstractModel, models.Model):
    STATUS_CHOICES = [
        ("processing", _("В обработке")),
        ("declined", _("Отказан")),
        ("awaiting_payment", _("Ожидание оплаты")),
        ("shipping", _("В доставке")),
        ("delivered", _("Доставлен")),
    ]
    ADDRESS_FORM_CHOICES = [
        ("Mr.", _("Уважаемый")),
        ("Mrs.", _("Уважаемая")),
    ]
    user = models.ForeignKey(
        get_user_model(),
        related_name="orders",
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
    )
    session_key = models.CharField(max_length=255)
    clarify_address = models.BooleanField(default=False, verbose_name="Уточнить адрес?")
    country = models.CharField(verbose_name="Страна", max_length=40)
    city = models.CharField(verbose_name="Город", max_length=40)
    email = models.EmailField(verbose_name="Почта")
    address_form = models.CharField(
        max_length=20,
        choices=ADDRESS_FORM_CHOICES,
        default="Mr.",
        verbose_name="Форма обращения к заказчику",
    )
    name = models.CharField(verbose_name="Имя заказчика", max_length=80)
    postal_code = models.CharField(
        verbose_name="Почтовый индекс", max_length=40, null=True, blank=True
    )
    street = models.CharField(
        verbose_name="Улица", max_length=255, null=True, blank=True
    )
    building = models.CharField(
        verbose_name="Здание", max_length=40, null=True, blank=True
    )
    flat = models.CharField(
        verbose_name="Квартира/офис", max_length=40, null=True, blank=True
    )
    delivery_date = models.DateField(verbose_name="Дата доставки")
    delivery_time = models.TimeField(verbose_name="Время доставки")
    message_card = models.TextField(
        verbose_name="Записка к букету", max_length=10000, null=True, blank=True
    )
    instructions = models.TextField(
        verbose_name="Инструкции к доставке", max_length=800, null=True, blank=True
    )
    recipient_address_form = models.CharField(
        max_length=20,
        choices=ADDRESS_FORM_CHOICES,
        default="Mr.",
        verbose_name="Форма обращения к получателю",
    )
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
    sub_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Чистая стоимость"),
        help_text="Без налога",
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Налоговая стоимость"),
        help_text="Стоимость налога",
    )
    tax_percent = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name=_("НДС"),
        help_text="%",
        default=0,
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Итоговая стоимость"),
        help_text="С налогом",
    )
    language_code = models.CharField(
        max_length=2,
        verbose_name="Язык пользователя на сайте"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.code} - {self.status}"
    



@receiver(post_save, sender=Order)
def order_created(sender: Order, instance: Order, created, **kwargs):
    if created:
        order = instance
        text = (
            f"*Новый заказ оформлен!* 🎉\n\n"
            f"*ID заказа*: `{order.id}`\n"
            f"*Стоимость*: `{order.grand_total} EUR`\n"
            f"*Страна*: `{escape_markdown(order.country)}`\n"
            f"*Город*: `{escape_markdown(order.city)}`\n\n"
            f"Вперёд за работу! 🚀"
        )

        send_message_to_telegram(text)


class OrderItem(models.Model):
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта",
    )
    product_discount = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name="Скидка на продукт",
        null=True,
        default=0,
    )
    product_discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта cо скидкой",
    )
    product_tax_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта с налогом",
    )
    product_tax_price_discounted = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена продукта со скидкой и налогом",
    )
    quantity = models.IntegerField(verbose_name="Количество продукта")

    class Meta:
        abstract = True


class OrderProducts(TimeStampAdbstractModel, OrderItem):
    order = models.ForeignKey(
        Order, related_name="products", verbose_name="Заказ", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product, related_name="orders", verbose_name="Продукт", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Продукт в заказе"
        verbose_name_plural = "Продукты в заказе"

    def __str__(self):
        return f"{self.pk}"


class OrderBouquets(TimeStampAdbstractModel, OrderItem):
    order = models.ForeignKey(
        Order, related_name="bouquets", verbose_name="Заказ", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Bouquet, related_name="orders", verbose_name="Букет", on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Букет в заказе"
        verbose_name_plural = "Букеты в заказе"

        def __str__(self):
            return f"{self.pk}"
