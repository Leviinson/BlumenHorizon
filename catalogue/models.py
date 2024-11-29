from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from random import randint

from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from telegram.helpers import escape_markdown
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel
from tg_bot import send_message_to_telegram


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
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=4000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
        </script>""",
    )

    class Meta:
        abstract = True


class CatalogPageModel(models.Model):
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=4000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
        </script>""",
    )

    class Meta:
        verbose_name = "Мета-тег каталога категорий и подкатегорий"
        verbose_name_plural = "Мета-теги каталога категорий и подкатегорий"

    def __str__(self):
        return "Мета-теги каталога категорий и подкатегорий"


class CategoryAbstract(models.Model):
    code_value = models.CharField(max_length=50, unique=True, default=generate_sku)

    class Meta:
        abstract = True


class ProductsListPageModel(models.Model):
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=4000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
        </script>""",
    )

    class Meta:
        verbose_name = "Мета-тег списка всех продуктов"
        verbose_name_plural = "Мета-теги списка всех продуктов"

    def __str__(self):
        return "Мета-теги списка всех продуктов"


class BouquetsListPageModel(models.Model):
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )
    json_ld = models.TextField(
        verbose_name="JSON-LD",
        max_length=4000,
        default="""<script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "WebPage"
        }
        </script>""",
    )

    class Meta:
        verbose_name = "Мета-тег списка всех букетов"
        verbose_name_plural = "Мета-теги списка всех букетов"

    def __str__(self):
        return "Мета-теги списка всех букетов"


class ProductCategory(CategoryAbstract, TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)
    catalog_page_meta_tags = models.TextField(
        verbose_name="Мета-теги на странице категории со списком подкатегорий",
        max_length=4000,
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )

    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:products-category",
            kwargs={
                "category_slug": self.slug,
            },
        )
        return f"https://{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:products-category",
            kwargs={
                "category_slug": self.slug,
            },
        )


class ProductSubcategory(
    CategoryAbstract, TimeStampAdbstractModel, MetaDataAbstractModel
):
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="subcategories",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Подкатегория продукта"
        verbose_name_plural = "Подкатегории продуктов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:products-subcategory",
            kwargs={"category_slug": self.category.slug, "subcategory_slug": self.slug},
        )
        return f"https://{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:products-subcategory",
            kwargs={"category_slug": self.category.slug, "subcategory_slug": self.slug},
        )

    def clean_category(self):
        if self.category is None:
            self.is_active = False


class ProductAbstract(TimeStampAdbstractModel, MetaDataAbstractModel):
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

    def _get_tax_percent(self):
        site = (
            Site.objects.prefetch_related("extended")
            .only("extended__tax_percent")
            .first()
        )
        return Decimal(site.extended.tax_percent)

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


class Product(ProductAbstract):
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        related_name="products",
    )
    sku = models.CharField(max_length=25, unique=True, default=generate_sku, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:product-details",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "product_slug": self.slug,
            },
        )
        return f"https://{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:product-details",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "product_slug": self.slug,
            },
        )

    @property
    def is_bouquet(self) -> bool:
        return False


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        default="defaults/no-image.webp",
        verbose_name="Изображение продукта",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"

    def __str__(self):
        return f"{self.product.name} - Image"


class Color(models.Model):
    name = models.CharField(
        max_length=15,
        verbose_name="Название",
        unique=True,
    )
    hex_code = ColorField(
        verbose_name="HEX код цвета (#f4678a к примеру)",
        help_text="Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат).",
        unique=True,
    )

    class Meta:
        verbose_name = "Цвет букета"
        verbose_name_plural = "Цветовые гаммы букетов"

    def __str__(self):
        return f"{self.name} ({self.hex_code})"


class Flower(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="Название",
        unique=True,
    )

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Состав букетов"

    def __str__(self):
        return self.name


class BouquetCategory(CategoryAbstract, TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)
    catalog_page_meta_tags = models.TextField(
        verbose_name="Мета-теги на странице категории со списком подкатегорий",
        max_length=4000,
        default="""<title>Blumen Horizon | </title>
<meta name="description" content="Описание">""",
    )

    class Meta:
        verbose_name = "Категория букета"
        verbose_name_plural = "Категории букетов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:bouquets-category",
            kwargs={
                "category_slug": self.slug,
            },
        )
        return f"https://{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:bouquets-category",
            kwargs={
                "category_slug": self.slug,
            },
        )


class BouquetSubcategory(
    CategoryAbstract, TimeStampAdbstractModel, MetaDataAbstractModel
):
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)
    category = models.ForeignKey(
        BouquetCategory,
        on_delete=models.PROTECT,
        verbose_name="Категория",
        related_name="subcategories",
    )

    class Meta:
        verbose_name = "Подкатегория букета"
        verbose_name_plural = "Подкатегории букетов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:bouquets-subcategory",
            kwargs={
                "category_slug": self.category.slug,
                "subcategory_slug": self.slug,
            },
        )
        return f"https://www.{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:bouquets-subcategory",
            kwargs={
                "category_slug": self.category.slug,
                "subcategory_slug": self.slug,
            },
        )

    def clean_category(self):
        if self.category is None:
            self.is_active = False


class Bouquet(ProductAbstract):
    subcategory = models.ForeignKey(
        BouquetSubcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        related_name="bouquets",
    )
    amount_of_flowers = models.IntegerField(verbose_name="Количество цветов в букете")
    diameter = models.IntegerField(verbose_name="Диаметр букета")
    colors = models.ManyToManyField(
        Color,
        related_name="bouquet",
        verbose_name="Цветовые гаммы букетов",
        help_text="Выберите какого цвета букет.",
    )
    flowers = models.ManyToManyField(
        Flower,
        related_name="bouquets",
        verbose_name="Состав букетов",
        help_text="Выберите какие цветы в букете.",
    )
    sku = models.CharField(max_length=25, unique=True, default=generate_sku, null=True)

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"

    def __str__(self):
        return f"{self.name} ({self.diameter} см, {self.amount_of_flowers} цветов)"

    def get_absolute_url(self):
        site = Site.objects.only("domain").first()
        relative_url = reverse_lazy(
            "catalogue:bouquet-details",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "bouquet_slug": self.slug,
            },
        )
        return f"https://{site.domain}{relative_url}"

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:bouquet-details",
            kwargs={
                "category_slug": self.subcategory.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "bouquet_slug": self.slug,
            },
        )

    @property
    def is_bouquet(self) -> bool:
        return True


class BouquetSize(models.Model):
    bouquet = models.ForeignKey(
        Bouquet, related_name="sizes", verbose_name="Букет", on_delete=models.CASCADE
    )
    amount_of_flowers = models.IntegerField(verbose_name="Количество цветов в букете")
    diameter = models.IntegerField(verbose_name="Диаметр букета")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена размера",
        help_text="Цена размера до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99",
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

    @property
    def discount_price(self) -> float:
        discount = Decimal(self.discount)
        result = self.price * (1 - discount / 100) if discount else self.price
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    class Meta:
        verbose_name = "Размер букета"
        verbose_name_plural = "Размеры букетов"

    def __str__(self):
        return f"{self.diameter}cm, {self.price}у.е."


class BouquetImage(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Букет",
    )
    image = models.ImageField(
        upload_to="bouquets/%Y-%m-%d/",
        verbose_name="Изображение букета",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение букета"
        verbose_name_plural = "Изображения букетов"

    def __str__(self):
        return f"{self.bouquet.name} - Image"


class BouquetSizeImage(models.Model):
    bouquet_size = models.ForeignKey(
        BouquetSize,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Размер букета",
    )
    image = models.ImageField(
        upload_to="bouquets/sizes/%Y-%m-%d/",
        verbose_name="Изображение размера букета",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)

    class Meta:
        verbose_name = "Изображение размера букета"
        verbose_name_plural = "Изображения размеров букетов"


class IndividualQuestion(TimeStampAdbstractModel, models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="individual_questions",
        verbose_name="Связанный аккаунт",
        null=True,
        blank=False,
    )
    contact_method = models.TextField(
        max_length=100,
        verbose_name="Способ связи с клиентом",
    )
    recall_me = models.BooleanField(
        verbose_name="Разрешил ли клиент звонить ему", default=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="individual_question",
        verbose_name="Связанный продукт",
        null=True,
        blank=True,
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.SET_NULL,
        related_name="individual_question",
        verbose_name="Связанный букет",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Индивидуальный вопрос о продукте"
        verbose_name_plural = "Индивидуальные вопросы о продуктах"

    def __str__(self):
        return f"{self.user if self.user else "Неизвестный пользователь"}"


@receiver(post_save, sender=IndividualQuestion)
def order_created(sender, instance: IndividualQuestion, created, **kwargs):
    if created:

        individual_order = instance
        text = (
            f"*Индивидуальный заказ!* 🎉\n\n"
            f"*ID заказа*: `{individual_order.id}`\n"
            f"*Продукт*: `{individual_order.product.name if individual_order.product.name else individual_order.bouquet.name}\n"
            f"*Способ связи:*: `\n\n{escape_markdown(individual_order.contact_method)}`\n"
            f"Вперёд за работу! 🚀"
        )

        chat_id = settings.TELEGRAM_CHAT_ID
        send_message_to_telegram(chat_id, text)