from django.contrib.sites.shortcuts import get_current_site


class CommonContextMixin:
    def get_context_data(self, *args, **kwargs):
        "Must be implemented and inherited by every view"
        context = super().get_context_data(*args, **kwargs)
        if not context.get("site_name"):
            context["site_name"] = get_current_site(self.request).name
        return context
