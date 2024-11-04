from django.contrib.sites.shortcuts import get_current_site
from django.db.models import OuterRef, Subquery
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView

from cart.cart import BouquetCart, ProductCart
from catalogue.models import Bouquet, BouquetImage
from core.services.mixins.views import CommonContextMixin

from .models import MainPageSliderImages


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
        first_image_subquery = BouquetImage.objects.filter(
            **{
                "bouquet": OuterRef("pk"),
            }
        ).order_by("id")[:1]
        bouquets = (
            Bouquet.objects.select_related("subcategory", "subcategory__category")
            .only(
                "name",
                "price",
                "slug",
                "subcategory__slug",
                "subcategory__category__slug",
            )
            .annotate(
                first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            )
            .order_by("amount_of_orders", "amount_of_savings")
            .all()
        )
        context["recommended_products"] = bouquets
        context["products_cart"] = ProductCart(
            self.request.session, session_key="products_cart"
        )
        context["bouquets_cart"] = BouquetCart(
            self.request.session, session_key="bouquets_cart"
        )
        return context
