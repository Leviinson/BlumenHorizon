from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

from catalogue.models import Category


class CommonContextMixin:
    def get_context_data(self, *args, **kwargs):
        "Must be implemented and inherited by every view"
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = (
            Category.objects.filter(is_active=True)
            .only(
                "name",
                "slug",
            )
        )
        current_site: Site = get_current_site(self.request)
        if not context.get("site_name"):
            context["site_name"] = current_site.name
        context["currency_symbol"] = current_site.extended.currency_symbol
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context
