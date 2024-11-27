from modeltranslation.translator import TranslationOptions, register

from .models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    BouquetSizeImage,
    BouquetsListPageModel,
    BouquetSubcategory,
    CatalogPageModel,
    Color,
    Flower,
    Product,
    ProductCategory,
    ProductImage,
    ProductsListPageModel,
    ProductSubcategory,
)


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "image_alt",
        "meta_tags",
        "json_ld",
    )


@register(ProductSubcategory)
class ProductSubcategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "image_alt",
        "meta_tags",
        "json_ld",
    )


@register(BouquetCategory)
class BouquetCategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "image_alt",
        "meta_tags",
        "json_ld",
    )


@register(BouquetSubcategory)
class BouquetSubcategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "image_alt",
        "meta_tags",
        "json_ld",
    )


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
        "description",
        "specs",
        "meta_tags",
        "json_ld",
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
        "meta_tags",
        "json_ld",
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


@register(CatalogPageModel)
class CatalogPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "json_ld",
    )


@register(ProductsListPageModel)
class ProductsListPageModelTranslationOptions(TranslationOptions):
    fields = ("meta_tags",)


@register(BouquetsListPageModel)
class BouquetsListPageModelTranslationOptions(TranslationOptions):
    fields = ("meta_tags",)
