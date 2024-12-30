from modeltranslation.translator import TranslationOptions, register

from .models import (
    AboutUsPageModel,
    AGBPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    ImpressumPageModel,
    MainPageModel,
    MainPageSeoBlock,
    MainPageSliderImages,
    PrivacyAndPolicyPageModel,
    ReturnPolicyPageModel,
)


@register(MainPageSeoBlock)
class SeoBlockTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
    )


@register(MainPageSliderImages)
class MainPageSliderImageTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
    )


@register(MainPageModel)
class MainPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
        "json_ld_description",
    )


@register(FAQPageModel)
class FAQPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
    )


@register(ContactsPageModel)
class ContactsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
    )


@register(DeliveryPageModel)
class DeliveryPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
    )


@register(AboutUsPageModel)
class AboutUsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
    )


@register(AGBPageModel)
class AGBPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
    )


@register(PrivacyAndPolicyPageModel)
class PrivacyAndPolicyPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
    )


@register(ImpressumPageModel)
class ImpressumPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
    )


@register(ReturnPolicyPageModel)
class ReturnPolicyPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
    )
