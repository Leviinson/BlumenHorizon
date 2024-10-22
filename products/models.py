import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel


class MetaDataAbstractModel(models.Model):
    name = models.CharField(
        verbose_name=_("Название"),
        max_length=20,
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


class Category(MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name


class Subcategory(MetaDataAbstractModel):
    image = models.ImageField(
        verbose_name=_("Картинка"),
        upload_to="subcategories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Категория"),
    )

    class Meta:
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")

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
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.DO_NOTHING, verbose_name=_("Подкатегория")
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
    class Meta:
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")

    def get_absolute_url(self):
        return "products/%s/" % self.slug


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name=_("Продукт"),
    )
    image = models.ImageField(
        upload_to="products/%Y-%m-%d/",
        verbose_name=_("Изображение"),
        default="defaults/no-image.webp",
    )

    class Meta:
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продуктов")

    def __str__(self):
        return f"{self.product.name} - Image"


def validate_hex_color(value):
    if not re.match(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", value):
        raise ValidationError(
            _('Введите корректный HEX-код цвета, начинающийся с "#".')
        )


class Color(models.Model):
    name = models.CharField(max_length=15)
    hex_code = models.CharField(
        max_length=7,
        validators=[validate_hex_color],
        help_text=_(
            "Введите HEX-код цвета, например: #FFFFFF (белый) или #FFF (сокращённый формат)."
        ),
    )

    class Meta:
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")

    def __str__(self):
        return f"{self.name} ({self.hex_code})"


class Flower(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("Цветок")
        verbose_name_plural = _("Цветы")

    def __str__(self):
        return self.name


class Bouquet(ProductAbstract):
    size = models.IntegerField(verbose_name=_("Диаметр букета"))
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

    def get_absolute_url(self):
        return "bouquets/%s/" % self.slug


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
