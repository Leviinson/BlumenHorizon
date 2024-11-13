from modeltranslation.translator import TranslationOptions, register

from .models import MainPageSliderImages, SeoBlock


@register(SeoBlock)
class SeoBlockTranslationOptions(TranslationOptions):
    fields = ("image_alt",)


@register(MainPageSliderImages)
class MainPageSliderImageTranslationOptions(TranslationOptions):
    fields = ("image_alt",)
