from colorfield.fields import ColorField
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

    class Meta:
        abstract = True


class ProductCategory(MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )

    class Meta:
        verbose_name = _("Категория продукта")
        verbose_name_plural = _("Категории продуктов")

    def __str__(self):
        return self.name


class ProductSubcategory(MetaDataAbstractModel):
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

    class Meta:
        verbose_name = _("Подкатегория продукта")
        verbose_name_plural = _("Подкатегории продуктов")

    def __str__(self):
        return self.name

    def clean_category(self):
        if self.category is None:
            self.is_active = False


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


class Product(ProductAbstract):
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.PROTECT,
        verbose_name=_("Подкатегория"),
        related_name="products",
    )

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
        upload_to="products_media/%Y-%m-%d/",
        verbose_name=_("Изображение"),
    )

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
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")

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
        verbose_name_plural = _("Цветы")

    def __str__(self):
        return self.name


class BouquetCategory(MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )

    class Meta:
        verbose_name = _("Категория букета")
        verbose_name_plural = _("Категории букетов")

    def __str__(self):
        return self.name


class BouquetSubcategory(MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
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
    size = models.IntegerField(
        verbose_name=_("Диаметр букета"),
    )
    amount_of_flowers = models.IntegerField(
        verbose_name=_("Количество цветов в букете")
    )
    colors = models.ManyToManyField(
        Color,
        related_name="bouquets",
        verbose_name=_("Цвета"),
        help_text=_("Выберите какого цвета букет."),
    )
    flowers = models.ManyToManyField(
        Flower,
        related_name="bouquets",
        verbose_name=_("Цветы"),
        help_text=_("Выберите какие цветы в букете."),
    )

    class Meta:
        verbose_name = _("Букет")
        verbose_name_plural = _("Букеты")

    def __str__(self):
        return f"{self.name} ({self.size} см, {self.amount_of_flowers} цветов)"

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


class BouquetImage(models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("Букет"),
    )
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        verbose_name=_("Изображение"),
    )

    class Meta:
        verbose_name = _("Изображение букета")
        verbose_name_plural = _("Изображения букетов")

    def __str__(self):
        return f"{self.bouquet.name} - Image"
