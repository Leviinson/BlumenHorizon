from abc import abstractmethod
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from random import randint

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel
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
        help_text="Цена продукта без налога до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99",
    )

    @property
    @abstractmethod
    def tax_percent(self):
        pass

    discount = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name="Скидка",
        help_text="Будет рассчитано после налога",
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
        return Decimal(self.tax_percent.value)

    @property
    def discount_price(self) -> Decimal:
        """
        Рассчитывает цену продукта с учётом скидки.

        Если на товар есть скидка, вычисляется новая цена, с учетом этой скидки.
        Цена с учетом скидки рассчитывается как:
        Цена = (Базовая цена * (1 - Скидка в процентах / 100)).

        Используется для вычисления цены продукта
        со скидкой и налогом (self.tax_price_discounted), а так-же чтобы рассчитать
        кол-во заплаченного налога за один продукт (self.taxes)

        Возвращает:
            Decimal: Цена продукта с учётом скидки, округленная до двух знаков после запятой.
        """
        if self.has_discount:
            discount_factor = Decimal(1) - (Decimal(self.discount) / 100)
            return (self.price * discount_factor).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        return self.price

    @property
    def tax_price(self) -> Decimal:
        """
        Рассчитывает цену продукта с учётом налога на основе базовой цены.

        Для базовой цены продукта (без скидки) добавляется налог с учётом ставки НДС.
        Цена с налогом рассчитывается как:
        Цена с налогом = Базовая цена * (1 + Налоговая ставка / 100).

        Используется когда у продукта self.has_discount = False, чтобы отображать цену без скидки.

        Возвращает:
            Decimal: Цена продукта с учётом налога, округленная до двух знаков после запятой.
        """
        tax_percent = self._get_tax_percent()
        return (self.price * (Decimal(1) + tax_percent / 100)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def tax_price_discounted(self) -> Decimal:
        """
        Рассчитывает цену продукта с учётом налога и скидки.

        Для цены продукта после применения скидки добавляется налог с учётом ставки НДС.
        Цена с налогом и скидкой рассчитывается как:
        Цена с налогом и скидкой = (Цена со скидкой) * (1 + Налоговая ставка / 100).

        Возвращает:
            Decimal: Цена продукта с учётом как скидки, так и налога, округленная до двух знаков после запятой.
        """
        tax_percent = self._get_tax_percent()
        discounted_price = self.discount_price
        return (discounted_price * (Decimal(1) + tax_percent / 100)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def taxes(self) -> Decimal:
        """
        Рассчитывает сумму налога, которую платит клиент за продукт.

        Налог вычисляется как разница между ценой с налогом и скидкой и ценой со скидкой без налога.
        Сумма налога = Цена с налогом и скидкой - Цена со скидкой.

        Возвращает:
            Decimal: Сумма налога, которую платит клиент, округленная до двух знаков после запятой.
        """
        return self.tax_price_discounted - self.discount_price

    @property
    def has_discount(self) -> bool:
        """
        Проверяет, действует ли скидка на продукт.

        Скидка считается активной, если на текущую дату не истёк срок её действия.
        Если скидка активна, возвращается True, иначе — False.

        Возвращает:
            bool: True, если скидка активна, и False, если нет.
        """
        return self.discount and (timezone.now() < self.discount_expiration_datetime)

    @property
    def price_valid_until(self) -> datetime:
        """
        Определяет дату, до которой действительна цена на продукт.

        Если на товар действует скидка, то дата окончания действия цены — это дата истечения скидки.
        В противном случае дата окончания действия цены — это последний день текущего месяца.

        Возвращает:
            datetime: Дата, до которой действительна цена на продукт.
        """
        from calendar import monthrange

        if self.has_discount:
            return self.discount_expiration_datetime
        today = datetime.today()
        last_day = monthrange(today.year, today.month)[1]
        last_day_of_month = datetime(today.year, today.month, last_day)
        return last_day_of_month


class ItemReview(TimeStampAdbstractModel):
    author_name = models.CharField(
        default=_("Аноним"), max_length=80, verbose_name="Имя автора"
    )
    email = models.EmailField(blank=True, null=True, verbose_name="Email автора")
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Прошло модерацию?",
    )

    @property
    def rate_range(self) -> range:
        """
        Возвращает диапазон, который представляет количество отображаемых звёздочек.

        Этот диапазон создаётся на основе значения рейтинга (`self.rate`), и используется для отображения соответствующего
        количества звёздочек в интерфейсе. Если рейтинг равен 3, диапазон будет содержать числа от 0 до 2 (т.е. 3 звезды).

        Возвращает:
            range: Диапазон от 0 до (rate-1), где `rate` — это количество звёздочек для отображения.
        """
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
