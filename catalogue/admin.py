from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    Bouquet,
    BouquetImage,
    Category,
    Color,
    Flower,
    Product,
    ProductImage,
    Subcategory,
)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    fieldsets = ((None, {"fields": ("name", "slug", "is_active", "image")}),)
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
    )
    list_display = (
        "name",
        "slug",
        "is_active",
    )
    ordering = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(TranslationAdmin):
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "is_active", "image")}),
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "slug",
    )
    list_display = (
        "name",
        "slug",
        "category",
        "is_active",
    )
    ordering = ("category",)


class ProductImagesInLine(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 3


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [
        ProductImagesInLine,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "price",
                    "discount",
                    "is_active",
                    "subcategory",
                    "description",
                    "specs",
                )
            },
        ),
    )
    list_filter = (
        "slug",
        "created_at",
        "updated_at",
        "is_active",
        "subcategory",
    )
    search_fields = (
        "name",
        "slug",
        "price"
    )
    list_display = (
        "name",
        "slug",
        "is_active",
    )
    ordering = ("name",)


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    fieldsets = ((None, {"fields": ("name", "hex_code")}),)
    list_filter = ("name",)
    search_fields = (
        "name",
        "hex_code",
    )
    list_display = (
        "name",
        "hex_code",
    )
    ordering = ("name",)


@admin.register(Flower)
class FlowerAdmin(TranslationAdmin):
    fieldsets = ((None, {"fields": ("name",)}),)
    list_filter = ("name",)
    search_fields = ("name",)
    list_display = ("name",)
    ordering = ("name",)


class BouquetImagesInLine(admin.TabularInline):
    model = BouquetImage
    extra = 1
    max_num = 3


@admin.register(Bouquet)
class BouquetAdmin(TranslationAdmin):
    inlines = [
        BouquetImagesInLine,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "price",
                    "discount",
                    "is_active",
                    "subcategory",
                    "description",
                    "specs",
                    "size",
                    "amount_of_flowers",
                    "colors",
                    "flowers",
                )
            },
        ),
    )
    list_filter = (
        "is_active",
        "subcategory",
        "size",
        "colors",
        "flowers",
        "price",
        "discount"
    )
    search_fields = (
        "name",
        "slug",
        "price",
    )
    list_display = (
        "name",
        "slug",
        "size",
        "amount_of_flowers",
        "is_active",
    )
    filter_horizontal = ("colors", "flowers")
    ordering = ("name", "price", "discount")
