from modeltranslation.translator import TranslationOptions, register

from .models import ExtendedSite


@register(ExtendedSite)
class SiteExtensionsTranslationOptions(TranslationOptions):
    fields = (
        "country",
        "city",
        "header_alert_message",
        "parent_organization_url",
    )
