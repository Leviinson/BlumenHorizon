from modeltranslation.translator import TranslationOptions, register

from .models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    BouquetSizeImage,
    BouquetSubcategory,
    Color,
    Flower,
    Product,
    ProductCategory,
    ProductImage,
    ProductSubcategory,
)


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "image_alt")


@register(ProductSubcategory)
class ProductSubcategoryTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "image_alt")


@register(BouquetCategory)
class BouquetCategoryTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "image_alt")


@register(BouquetSubcategory)
class BouquetSubcategoryTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "image_alt")


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


@register(BouquetImage)
class BouquetImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(ProductImage)
class ProductImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(BouquetSizeImage)
class BouquetSizeImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)
