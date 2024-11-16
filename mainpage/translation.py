from modeltranslation.translator import TranslationOptions, register

from .models import MainPageMetaTags, MainPageSliderImages, SeoBlock


@register(SeoBlock)
class SeoBlockTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(MainPageSliderImages)
class MainPageSliderImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(MainPageMetaTags)
class MainPageMetaTagsTranslationOptions(TranslationOptions):
    fields = ("meta_tags",)
