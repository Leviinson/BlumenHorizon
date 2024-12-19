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
        "json_ld",
    )


@register(DeliveryPageModel)
class DeliveryPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
        "json_ld",
    )


@register(AboutUsPageModel)
class AboutUsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "description",
        "json_ld",
    )


@register(AGBPageModel)
class AboutUsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
        "json_ld",
    )


@register(PrivacyAndPolicyPageModel)
class AGBPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
        "json_ld",
    )


@register(ImpressumPageModel)
class ImpressumPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
        "json_ld",
    )


@register(ReturnPolicyPageModel)
class ReturnPolicyPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
        "json_ld",
    )
