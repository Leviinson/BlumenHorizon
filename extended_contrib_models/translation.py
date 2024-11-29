from modeltranslation.translator import TranslationOptions, register

from .models import ExtendedSite


@register(ExtendedSite)
class SiteExtensionsTranslationOptions(TranslationOptions):
    fields = (
        "country",
        "city",
        "country_iso_3166_1_alpha_2",
        "header_alert_message",
    )
