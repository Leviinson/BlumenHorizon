from modeltranslation.translator import TranslationOptions, register

from .models import Category, Subcategory, Product, Color, Flower, Bouquet


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "slug",
    )


@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
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
