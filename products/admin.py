from django.contrib import admin
from parler.admin import TranslatableAdmin

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
class CategoryAdmin(TranslatableAdmin):
    fieldsets = ((None, {"fields": ("slug", "is_active", "image")}),)
    list_filter = ("is_active",)
    search_fields = ("translations__name", "slug",)
    list_display = ("name", "slug", "is_active",)
    ordering = ("name",)


@admin.register(Subcategory)
class SubcategoryAdmin(TranslatableAdmin):
    fieldsets = (
        (None, {"fields": ("slug", "category", "is_active", "image")}),
    )
    list_filter = ("is_active",)
    search_fields = ("translations__name", "slug",)
    list_display = ("name", "slug", "category", "is_active",)
    ordering = ("category",)


class ProductImagesInLine(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 3


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    inlines = [ProductImagesInLine]
    fieldsets = (
        (None, {
            "fields": (
                "slug",
                "is_active",
                "subcategory",
                "description",
                "specs",
            )
        }),
    )
    list_filter = (
        "slug",
        "created_at",
        "updated_at",
        "is_active",
        "subcategory",
    )
    search_fields = ("translations__name", "slug", "description",)
    list_display = ("name", "slug", "is_active",)
    ordering = ("name",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "hex_code")}),)
    list_filter = ("name",)
    search_fields = ("name", "hex_code",)
    list_display = ("name", "hex_code",)
    ordering = ("name",)


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
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
class BouquetAdmin(TranslatableAdmin):
    inlines = [BouquetImagesInLine]
    fieldsets = (
        (None, {
            "fields": (
                "slug",
                "is_active",
                "subcategory",
                "description",
                "specs",
                "size",
                "amount_of_flowers",
                "colors",
                "flowers",
            )
        }),
    )
    list_filter = (
        "is_active",
        "subcategory",
        "size",
        "colors",
        "flowers",
    )
    search_fields = ("translations__name", "slug", "description",)
    list_display = ("name", "slug", "size", "amount_of_flowers", "is_active",)
    filter_horizontal = ("colors", "flowers")
    ordering = ("name",)