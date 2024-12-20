from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    BouquetSubcategory,
    CatalogPageModel,
    Color,
    Flower,
    IndividualQuestion,
    Product,
    ProductCategory,
    ProductImage,
    ProductSubcategory,
)


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "is_active",
                    "meta_tags",
                    "catalog_page_meta_tags",
                    "description",
                    "image",
                    "image_alt",
                    "amount_of_orders",
                    "amount_of_savings",
                ),
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "name_en",
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
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "is_active",
                    "meta_tags",
                    "image",
                    "image_alt",
                    "amount_of_orders",
                    "amount_of_savings",
                ),
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "name_en",
        "slug",
    )
    list_display = (
        "name",
        "slug",
        "category",
        "is_active",
    )
    ordering = ("category",)


class ProductImagesInLine(admin.StackedInline):
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
                    "sku",
                    "price",
                    "discount",
                    "discount_expiration_datetime",
                    "is_active",
                    "subcategory",
                    "amount_of_orders",
                    "amount_of_savings",
                    "description",
                    "specs",
                    "meta_tags",
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
        "name_en",
        "slug",
        "price",
    )
    list_display = (
        "name",
        "price",
        "discount",
        "slug",
        "is_active",
        "amount_of_orders",
        "amount_of_savings",
    )
    ordering = ("name",)


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "hex_code"),
            },
        ),
    )
    list_filter = ("name",)
    search_fields = (
        "name",
        "name_en",
        "hex_code",
    )
    list_display = (
        "name",
        "hex_code",
    )
    ordering = ("name",)


@admin.register(Flower)
class FlowerAdmin(TranslationAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": ("name",),
            },
        ),
    )
    list_filter = ("name",)
    search_fields = (
        "name",
        "name_en",
    )
    list_display = ("name",)
    ordering = ("name",)


class BouquetImagesInLine(admin.StackedInline):
    model = BouquetImage
    extra = 1
    max_num = 3


# class BouquetSizeImagesInLine(admin.TabularInline):
#     model = BouquetSizeImage
#     extra = 1
#     max_num = 3


# @admin.register(BouquetSize)
# class BouquetSizeAdmin(admin.ModelAdmin):
#     fields = (
#         "bouquet",
#         "amount_of_flowers",
#         "discount",
#         "discount_expiration_datetime",
#         "price",
#         "diameter",
#     )
#     list_display = (
#         "bouquet",
#         "amount_of_flowers",
#         "discount",
#         "discount_expiration_datetime",
#         "price",
#         "diameter",
#     )
#     inlines = [
#         BouquetSizeImagesInLine,
#     ]


# class BouquetSizesInLine(admin.StackedInline):
#     model = BouquetSize
#     extra = 1
#     max_num = 3
#     show_change_link = True


@admin.register(BouquetCategory)
class BouquetCategoryAdmin(TranslationAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "is_active",
                    "meta_tags",
                    "catalog_page_meta_tags",
                    "description",
                    "image",
                    "image_alt",
                    "amount_of_orders",
                    "amount_of_savings",
                ),
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "name_en",
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
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "is_active",
                    "meta_tags",
                    "image",
                    "image_alt",
                    "amount_of_orders",
                    "amount_of_savings",
                ),
            },
        ),
    )
    readonly_fields = (
        "amount_of_orders",
        "amount_of_savings",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "name_en",
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
        # BouquetSizesInLine,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "slug",
                    "sku",
                    "price",
                    "discount",
                    "discount_expiration_datetime",
                    "diameter",
                    "amount_of_savings",
                    "colors",
                    "flowers",
                    "is_active",
                    "amount_of_flowers",
                    "amount_of_orders",
                    "subcategory",
                    "description",
                    "specs",
                    "meta_tags",
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
        "diameter",
        "colors",
        "flowers",
        "price",
        "discount",
        "discount_expiration_datetime",
    )
    search_fields = (
        "name",
        "name_en",
        "slug",
        "price",
    )
    list_display = (
        "name",
        "price",
        "discount",
        "slug",
        "diameter",
        "amount_of_orders",
        "amount_of_savings",
        "amount_of_flowers",
        "is_active",
    )
    filter_horizontal = ("colors", "flowers")
    ordering = (
        "name",
        "price",
        "discount",
        "discount_expiration_datetime",
    )


@admin.register(IndividualQuestion)
class IndividualQuestionAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "contact_method",
        "recall_me",
        "product",
        "bouquet",
    )
    list_display = (
        "user",
        "contact_method",
        "recall_me",
        "product",
        "bouquet",
    )


@admin.register(CatalogPageModel)
class CatalogPageAdmin(TranslationAdmin):
    fields = (
        "meta_tags",
        "description",
    )
    list_display = ("id",)


# @admin.register(ProductsListPageModel)
# class ProductsListPageAdmin(TranslationAdmin):
#     fields = (
#         "meta_tags",
#         "json_ld",
#     )
#     list_display = ("id",)


# @admin.register(BouquetsListPageModel)
# class BouquetsListPageAdmin(TranslationAdmin):
#     fields = (
#         "meta_tags",
#         "json_ld",
#     )
#     list_display = ("id",)
