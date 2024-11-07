from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    BouquetSubcategory,
    Color,
    Flower,
    Product,
    ProductCategory,
    ProductImage,
    ProductSubcategory,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
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


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(TranslationAdmin):
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
                    "amount_of_orders",
                    "amount_of_savings",
                    "specs",
                )
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = (
        "amount_of_orders",
        "amount_of_savings",
        "slug",
        "created_at",
        "updated_at",
        "is_active",
        "subcategory",
    )
    search_fields = (
        "name",
        "slug",
        "price",
    )
    list_display = (
        "name",
        "slug",
        "is_active",
        "amount_of_orders",
        "amount_of_savings",
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


@admin.register(BouquetCategory)
class BouquetCategoryAdmin(TranslationAdmin):
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


@admin.register(BouquetSubcategory)
class BouquetSubcategoryAdmin(TranslationAdmin):
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
                    "amount_of_orders",
                    "amount_of_savings",
                    "colors",
                    "flowers",
                )
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = (
        "amount_of_orders",
        "amount_of_savings",
        "is_active",
        "subcategory",
        "size",
        "colors",
        "flowers",
        "price",
        "discount",
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
        "amount_of_orders",
        "amount_of_savings",
        "amount_of_flowers",
        "is_active",
    )
    filter_horizontal = ("colors", "flowers")
    ordering = ("name", "price", "discount")
