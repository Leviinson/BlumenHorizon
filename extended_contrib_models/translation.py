from modeltranslation.translator import TranslationOptions, register

from .models import ExtendedSite


@register(ExtendedSite)
class SiteExtensionsTranslationOptions(TranslationOptions):
    fields = (
        "header_alert_message",
    )
