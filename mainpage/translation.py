from modeltranslation.translator import TranslationOptions, register

from .models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    MainPageModel,
    MainPageSeoBlock,
    MainPageSliderImages,
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
        "json_ld",
        "description",
    )


@register(FAQPageModel)
class FAQPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "json_ld",
        "description",
    )


@register(ContactsPageModel)
class ContactsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "json_ld",
        "description",
    )


@register(DeliveryPageModel)
class DeliveryPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "json_ld",
        "description",
    )


@register(AboutUsPageModel)
class AboutUsPageModelTranslationOptions(TranslationOptions):
    fields = (
        "image_alt",
        "image",
        "meta_tags",
        "json_ld",
        "description",
    )
