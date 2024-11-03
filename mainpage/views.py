from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from catalogue.models import Bouquet
from core.services.mixins.views import CommonContextMixin

from .models import MainPageSliderImages


# Create your views here.
class MainPageView(CommonContextMixin, TemplateView):
    template_name = "mainpage/index.html"
    http_method_names = ["get"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = _(
            f"Цветы {get_current_site(self.request).extended.city} с доставкой"
        )
        context["slider_images"] = MainPageSliderImages.objects.filter(
            is_active=True
        ).all()
        bouquets = Bouquet.objects.all()

        paginator = Paginator(bouquets, 4)
        product_chunks = [
            paginator.page(i).object_list for i in range(1, paginator.num_pages + 1)
        ]
        context["recommended_products"] = product_chunks
        return context
