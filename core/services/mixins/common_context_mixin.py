import os
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language

from extended_contrib_models.models import ExtendedSite


class CommonContextMixin:
    def get_context_data(self, *args, **kwargs):
        "Must be implemented and inherited by every view"
        context = super().get_context_data(*args, **kwargs)
        current_site = self.current_site = get_current_site(self.request)
        site_extended: ExtendedSite = self.current_site.extended
        if not context.get("site_name"):
            context["site_name"] = current_site.name
            context["domain_name"] = current_site.domain
            context["company_email"] = site_extended.email
        context["gtag_id"] = os.getenv("GTAG_ID")
        context["merchant_id"] = os.getenv("MERCHANT_ID")
        context["currency_symbol"] = site_extended.currency_symbol
        context["currency_code"] = site_extended.currency_code
        context["socials_right_bottom"] = site_extended.socials.all()
        context["MEDIA_URL"] = settings.MEDIA_URL
        context["alert"] = site_extended.header_alert_message
        return context


class CanonicalsContextMixin:
    def get_context_data(self, *args, **kwargs):
        """
        Наследуется каждым контроллером, который требует
        генерации canonical/alternate/x-default ссылок.
        """
        context = super().get_context_data(*args, **kwargs)

        current_lang_code = get_language()
        context["canonical_link"] = self.get_canonical_link(current_lang_code)
        context["alternate_links"] = self.get_alternate_links(
            current_lang_code,
            settings.LANGUAGES,
        )
        context["xdefault_link"] = self.get_xdefault_link(settings.LANGUAGES[0][0])
        return context
