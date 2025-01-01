from django.db import models
from django.urls import reverse_lazy
from tinymce.models import HTMLField

from core.base_models import TimeStampAdbstractModel

from ..services import (
    CategoryAbstractModel,
    MetaDataAbstractModel,
    ProductAbstractModel,
    generate_sku,
)


class ProductsListPageModel(models.Model):
    meta_tags = models.TextField(
        verbose_name="Мета-теги",
        max_length=1000,
        default="""<title> | BlumenHorizon</title>
<meta name="description" content="Описание">""",
    )

    class Meta:
        verbose_name = "Мета-тег списка всех продуктов"
        verbose_name_plural = "Мета-теги списка всех продуктов"

    def __str__(self):
        return "Мета-теги списка всех продуктов"


class ProductCategory(
    CategoryAbstractModel, TimeStampAdbstractModel, MetaDataAbstractModel
):
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="categories/%Y-%m-%d",
        default="defaults/no-image.webp",
    )
    image_alt = models.CharField(verbose_name="Описание картинки", max_length=200)
    catalog_page_meta_tags = models.TextField(
        verbose_name="Мета-теги на странице категории со списком подкатегорий",
        max_length=4000,
        default="""<title> | BlumenHorizon</title>
<meta name="description" content="Описание">""",
    )
    description = HTMLField(verbose_name="Описание на странице категории", null=True)

    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "7. Категории продуктов"

    def __str__(self):
        return self.name

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:products-category",
            kwargs={
                "category_slug": self.slug,
            },
        )


class ProductSubcategory(
    CategoryAbstractModel, TimeStampAdbstractModel, MetaDataAbstractModel
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
        verbose_name_plural = "8. Подкатегории продуктов"

    def __str__(self):
        return self.name

    def get_relative_url(self):
        return reverse_lazy(
            "catalogue:products-subcategory",
            kwargs={"category_slug": self.category.slug, "subcategory_slug": self.slug},
        )

    def clean_category(self):
        if self.category is None:
            self.is_active = False


class Product(ProductAbstractModel):
    subcategory = models.ForeignKey(
        ProductSubcategory,
        on_delete=models.PROTECT,
        verbose_name="Подкатегория",
        related_name="products",
    )
    sku = models.CharField(max_length=25, unique=True, default=generate_sku, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "6. Продукты"

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
