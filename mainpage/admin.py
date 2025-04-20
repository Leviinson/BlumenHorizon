from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from extended_contrib_models.models import Filial

from .models import (
    AboutUsPageModel,
    AGBPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    ImpressumPageModel,
    IndividualOrder,
    MainPageModel,
    MainPageSeoBlock,
    MainPageSliderImages,
    PrivacyAndPolicyPageModel,
    ReturnPolicyPageModel,
)


@admin.register(MainPageSliderImages)
class MainPageSliderAdmin(TranslationAdmin):
    fields = ["image", "image_alt", "is_active"]
    list_display = ["pk", "image", "image_alt", "is_active"]


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
        "json_ld_description",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(FAQPageModel)
class FAQPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(ContactsPageModel)
class ContactsPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(DeliveryPageModel)
class DeliveryPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(AboutUsPageModel)
class AboutUsPageModelAdmin(TranslationAdmin):
    fields = [
        "image",
        "image_alt",
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(AGBPageModel)
class AGBPageModelAdmin(TranslationAdmin):
    fields = [
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(PrivacyAndPolicyPageModel)
class PrivacyAndPolicyPageModelAdmin(TranslationAdmin):
    fields = [
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(ImpressumPageModel)
class ImpressumPageModelAdmin(TranslationAdmin):
    fields = [
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(ReturnPolicyPageModel)
class ReturnPolicyPageModelAdmin(TranslationAdmin):
    fields = [
        "meta_tags",
        "description",
    ]
    list_display = ["__str__"]


@admin.register(Filial)
class FilialModelAdmin(TranslationAdmin):
    fields = ["title", "url"]
    list_display = ["__str__"]
