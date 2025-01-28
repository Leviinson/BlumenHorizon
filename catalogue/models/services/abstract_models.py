from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from random import randint

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel
from core.services.repositories.site import SiteRepository
from core.services.types import AbsoluteUrl


def generate_sku():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = randint(1000, 9999)
    return f"SKU-{timestamp}-{random_part}"


class MetaDataAbstractModel(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Название в ссылке",
        unique=True,
        max_length=80,
    )
    is_active = models.BooleanField(
        verbose_name="Активный?",
        default=True,
    )
    amount_of_orders = models.IntegerField(
        verbose_name="Количество заказов",
        editable=False,
        default=0,
    )
    amount_of_savings = models.IntegerField(
        verbose_name="Количество добавлений в корзину",
        editable=False,
        default=0,
    )
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=4000,
        default="""<title> | BlumenHorizon</title>
<meta name="description" content="Описание">""",
    )

    class Meta:
        abstract = True

    def get_absolute_url(self) -> AbsoluteUrl:
        from core.services.utils.urls import build_absolute_url

        if not getattr(self, "get_relative_url"):
            raise AttributeError(
                f"У ресурса {self.__class__.__name__} нереализован "
                f"метод «get_relative_url»"
            )
        return build_absolute_url(self.get_relative_url())


class CategoryAbstractModel(models.Model):
    code_value = models.CharField(max_length=50, unique=True, default=generate_sku)

    class Meta:
        abstract = True


class ProductAbstractModel(TimeStampAdbstractModel, MetaDataAbstractModel):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Цена продукта до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99",
    )
    discount = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name="Скидка",
        null=True,
        default=0,
    )
    discount_expiration_datetime = models.DateTimeField(
        verbose_name="Время истечения скидки", default=timezone.now
    )
    description = HTMLField(
        verbose_name="Описание",
    )
    specs = HTMLField(
        verbose_name="Характеристики",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def clean_subcategory(self):
        if self.subcategory is None:
            self.is_active = False

    def _get_tax_percent(self) -> Decimal:
        tax_percent = SiteRepository.get_tax_percent()
        return Decimal(tax_percent)

    @property
    def discount_price(self) -> Decimal:
        if self.has_discount:
            discount_factor = Decimal(1) - (Decimal(self.discount) / 100)
            return (self.price * discount_factor).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        return self.price

    @property
    def tax_price(self) -> Decimal:
        tax_percent = self._get_tax_percent()
        return (self.price * (Decimal(1) + tax_percent / 100)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def tax_price_discounted(self) -> Decimal:
        tax_percent = self._get_tax_percent()
        discounted_price = self.discount_price
        return (discounted_price * (Decimal(1) + tax_percent / 100)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def has_discount(self) -> bool:
        return self.discount and (timezone.now() < self.discount_expiration_datetime)


class ItemReview(TimeStampAdbstractModel):
    author_name = models.CharField(max_length=80, verbose_name="Имя автора")
    email = models.EmailField(blank=True, null=True, verbose_name="Email автора")
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг",
    )
    description = models.TextField(verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Прошло модерацию?")

    @property
    def rate_range(self) -> range:
        return range(self.rate)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        abstract = True

    def short_description(self):
        return (
            self.description[:100] + " ..."
            if len(self.description) > 100
            else self.description
        )

    def __str__(self):
        return f"{self.author_name} — {self.rate}"
