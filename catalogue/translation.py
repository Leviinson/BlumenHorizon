from modeltranslation.translator import TranslationOptions, register

from .models import (
    Bouquet,
    BouquetCategory,
    BouquetSubcategory,
    Color,
    Flower,
    Product,
    ProductCategory,
    ProductSubcategory,
)


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
    )


@register(ProductSubcategory)
class ProductSubcategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
    )


@register(BouquetCategory)
class BouquetCategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
    )


@register(BouquetSubcategory)
class BouquetSubcategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
    )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "description",
        "specs",
    )


@register(Flower)
class FlowerTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Bouquet)
class BouquetTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "description",
        "specs",
    )
