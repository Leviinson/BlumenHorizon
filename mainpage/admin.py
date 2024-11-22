from django.contrib import admin
from modeltranslation.admin import TranslationAdmin


from .models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    IndividualOrder,
    MainPageModel,
    MainPageSeoBlock,
    MainPageSliderImages,
)


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(TranslationAdmin):
    fields = ["image", "image_alt", "is_active"]
    list_display = ["image", "image_alt", "is_active"]


@admin.register(MainPageSeoBlock)
class SeoBlockAdmin(TranslationAdmin):
    fields = ["image", "image_alt"]
    list_display = ["pk", "image", "image_alt"]


@admin.register(IndividualOrder)
class IndividualOrderAdmin(admin.ModelAdmin):
    fields = ["first_name", "contact_method", "recall_me", "user"]
    list_display = ["user", "first_name", "contact_method", "recall_me"]


@admin.register(MainPageModel)
class MainPageModelAdmin(TranslationAdmin):
    fields = [
        "meta_tags",
        "json_ld",
        "description_ru",
        "description_en",
    ]
    list_display = ["id"]


@admin.register(FAQPageModel)
class FAQPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "json_ld",
        "description",
    ]
    list_display = ["id"]


@admin.register(ContactsPageModel)
class ContactsPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "json_ld",
        "description",
    ]
    list_display = ["id"]


@admin.register(DeliveryPageModel)
class DeliveryPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "json_ld",
        "description",
    ]
    list_display = ["id"]


@admin.register(AboutUsPageModel)
class AboutUsPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "json_ld",
        "description",
    ]
    list_display = ["id"]
