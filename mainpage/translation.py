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
    fields = ("image_alt",)


@register(MainPageSliderImages)
class MainPageSliderImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(MainPageModel)
class MainPageModelTranslationOptions(TranslationOptions):
    fields = (
        "meta_tags",
        "description",
    )


@register(FAQPageModel)
class FAQPageModelTranslationOptions(TranslationOptions):
    fields = ("image_alt", "meta_tags", "description")


@register(ContactsPageModel)
class ContactsPageModelTranslationOptions(TranslationOptions):
    fields = ("image_alt", "meta_tags", "description")


@register(DeliveryPageModel)
class DeliveryPageModelTranslationOptions(TranslationOptions):
    fields = ("image_alt", "meta_tags", "description")


@register(AboutUsPageModel)
class AboutUsPageModelTranslationOptions(TranslationOptions):
    fields = ("image_alt", "meta_tags", "description")
