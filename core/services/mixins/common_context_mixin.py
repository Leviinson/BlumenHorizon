from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

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
            context["company_email"] = settings.EMAIL_HOST_USER
        context["currency_symbol"] = site_extended.currency_symbol
        context["currency_code"] = site_extended.currency_code
        context["country"] = site_extended.country
        context["country_code"] = site_extended.country_iso_3166_1_alpha_2
        context["city"] = site_extended.city
        context["socials_right_bottom"] = site_extended.socials.all()
        context["MEDIA_URL"] = settings.MEDIA_URL
        context["alert"] = site_extended.header_alert_message
        return context
