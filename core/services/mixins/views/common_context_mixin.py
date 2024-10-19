from abc import ABC

from django.contrib.sites.shortcuts import get_current_site


class CommonContextMixin(ABC):
    def get_context_data(self, *args, **kwargs):
        "Must be implemented and inherited by every view"
        context = super().get_context_data(*args, **kwargs)
        context["site"] = get_current_site(self.request).name
        return context
