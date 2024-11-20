from django.contrib import admin

from .models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    IndividualOrder,
    MainPageModel,
    MainPageSliderImages,
    MainPageSeoBlock,
)


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(admin.ModelAdmin):
    fields = ["image", "image_alt", "is_active"]
    list_display = ["image", "image_alt", "is_active"]


@admin.register(MainPageSeoBlock)
class SeoBlockAdmin(admin.ModelAdmin):
    fields = ["image", "image_alt"]
    list_display = ["image", "image_alt"]


@admin.register(IndividualOrder)
class IndividualOrderAdmin(admin.ModelAdmin):
    fields = ["first_name", "contact_method", "recall_me", "user"]
    list_display = ["user", "first_name", "contact_method", "recall_me"]


@admin.register(MainPageModel)
class MainPageModelAdmin(admin.ModelAdmin):
    fields = [
        "meta_tags",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]


@admin.register(FAQPageModel)
class FAQPageModelAdmin(admin.ModelAdmin):
    fields = [
        "image",
        "image_alt_ru",
        "image_alt_en",
        "meta_tags_ru",
        "meta_tags_en",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]


@admin.register(ContactsPageModel)
class ContactsPageModelAdmin(admin.ModelAdmin):
    fields = [
        "image",
        "image_alt_ru",
        "image_alt_en",
        "meta_tags_ru",
        "meta_tags_en",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]


@admin.register(DeliveryPageModel)
class DeliveryPageModelAdmin(admin.ModelAdmin):
    fields = [
        "image",
        "image_alt_ru",
        "image_alt_en",
        "meta_tags_ru",
        "meta_tags_en",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]


@admin.register(AboutUsPageModel)
class AboutUsPageModelAdmin(admin.ModelAdmin):
    fields = [
        "image",
        "image_alt_ru",
        "image_alt_en",
        "meta_tags_ru",
        "meta_tags_en",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]
