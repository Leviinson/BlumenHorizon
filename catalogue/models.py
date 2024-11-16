from decimal import ROUND_HALF_UP, Decimal
from random import choices
from string import ascii_uppercase, digits

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel


class MetaDataAbstractModel(models.Model):
    name = models.CharField(
        verbose_name=_("Название"),
        max_length=40,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Название в ссылке"),
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активный?"),
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
    meta_tags = HTMLField(verbose_name="Мета-теги")

    class Meta:
        abstract = True


class CatalogPageModel(models.Model):
    meta_tags = HTMLField(verbose_name="Мета-теги")

class CategoryPageModel(models.Model):
    meta_tags = HTMLField(verbose_name="Мета-теги")


class ProductCategory(TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = _("Категория продукта")
        verbose_name_plural = _("Категории продуктов")

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse_lazy(
            "catalogue:products-category",
            kwargs={
                "category_slug": self.slug,
            },
        )

class ProductSubcategory(TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.PROTECT,
        verbose_name=_("Категория"),
        related_name="subcategories",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = _("Подкатегория продукта")
        verbose_name_plural = _("Подкатегории продуктов")

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse_lazy(
            "catalogue:products-subcategory",
            kwargs={"category_slug": self.category.slug, "subcategory_slug": self.slug},
        )

    def clean_category(self):
        if self.category is None:
            self.is_active = False


def generate_sku():
    sku = "".join(choices(ascii_uppercase + digits, k=6))
    return sku


class ProductAbstract(TimeStampAdbstractModel, MetaDataAbstractModel):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена"),
        help_text=_(
            "Цена продукта до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99"
        ),
    )
    discount = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name=_("Скидка"),
        null=True,
        default=0,
    )
    description = HTMLField(
        verbose_name=_("Описание"),
    )
    specs = HTMLField(
        verbose_name=_("Характеристики"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def clean_subcategory(self):
        if self.subcategory is None:
            self.is_active = False

    @property
    def discount_price(self) -> float:
        discount = Decimal(self.discount)
        result = self.price * (1 - discount / 100) if discount else self.price
        return result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Product(ProductAbstract):
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.PROTECT,
        verbose_name=_("Подкатегория"),
        related_name="products",
    )
    sku = models.CharField(max_length=6, unique=True, default=generate_sku, null=True)

    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def get_detail_url(self):
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
        verbose_name=_("Продукт"),
    )
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        default="defaults/no-image.webp",
        verbose_name="Изображение продукта",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продуктов")

    def __str__(self):
        return f"{self.product.name} - Image"


class Color(models.Model):
    name = models.CharField(
        max_length=15,
        verbose_name=_("Название"),
        unique=True,
    )
    hex_code = ColorField(
        verbose_name=_("HEX код цвета (#f4678a к примеру)"),
        help_text=_(
            "Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат)."
        ),
        unique=True,
    )

    class Meta:
        verbose_name = _("Цвет букета")
        verbose_name_plural = _("Цветовые гаммы букетов")

    def __str__(self):
        return f"{self.name} ({self.hex_code})"


class Flower(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name=_("Название"),
        unique=True,
    )

    class Meta:
        verbose_name = _("Цветок")
        verbose_name_plural = _("Состав букетов")

    def __str__(self):
        return self.name


class BouquetCategory(TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = _("Категория букета")
        verbose_name_plural = _("Категории букетов")

    def __str__(self):
        return self.name

    def get_detail_url(self):
        return reverse_lazy(
            "catalogue:bouquets-category",
            kwargs={
                "category_slug": self.slug,
            },
        )


class BouquetSubcategory(TimeStampAdbstractModel, MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)
    category = models.ForeignKey(
        BouquetCategory,
        on_delete=models.PROTECT,
        verbose_name=_("Категория"),
        related_name="subcategories",
    )

    class Meta:
        verbose_name = _("Подкатегория букета")
        verbose_name_plural = _("Подкатегории букетов")

    def __str__(self):
        return self.name

    def get_detail_url(self):
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
        verbose_name=_("Подкатегория"),
        related_name="bouquets",
    )
    amount_of_flowers = models.IntegerField(
        verbose_name=_("Количество цветов в букете")
    )
    diameter = models.IntegerField(verbose_name=_("Диаметр букета"))
    colors = models.ManyToManyField(
        Color,
        related_name="bouquet",
        verbose_name=_("Цветовые гаммы букетов"),
        help_text=_("Выберите какого цвета букет."),
    )
    flowers = models.ManyToManyField(
        Flower,
        related_name="bouquets",
        verbose_name=_("Состав букетов"),
        help_text=_("Выберите какие цветы в букете."),
    )
    sku = models.CharField(max_length=6, unique=True, default=generate_sku, null=True)

    class Meta:
        verbose_name = _("Букет")
        verbose_name_plural = _("Букеты")

    def __str__(self):
        return f"{self.name} ({self.diameter} см, {self.amount_of_flowers} цветов)"

    def get_detail_url(self):
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
        Bouquet, related_name="sizes", verbose_name=_("Букет"), on_delete=models.CASCADE
    )
    amount_of_flowers = models.IntegerField(
        verbose_name=_("Количество цветов в букете")
    )
    diameter = models.IntegerField(verbose_name=_("Диаметр букета"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Цена размера"),
        help_text=_(
            "Цена размера до 10ти значений, два из которых плавающая запятая. Т.е. до 99999999.99"
        ),
    )
    discount = models.IntegerField(
        validators=(
            MinValueValidator(0),
            MaxValueValidator(100),
        ),
        verbose_name=_("Скидка"),
        null=True,
        default=0,
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
        verbose_name=_("Букет"),
    )
    image = models.ImageField(
        upload_to="bouquets/%Y-%m-%d/",
        verbose_name=_("Изображение букета"),
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

    class Meta:
        verbose_name = _("Изображение букета")
        verbose_name_plural = _("Изображения букетов")

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
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=100)

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
        verbose_name=_("Способ связи с клиентом"),
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
