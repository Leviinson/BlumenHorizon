from typing import Literal

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import OuterRef, Subquery
from django.db.models.manager import BaseManager
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from cart.cart import BouquetCart, ProductCart
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.mixins.views import CommonContextMixin

from .forms import IndividualOrderForm
from .models import MainPageSliderImages, SeoBlock
from .services.dataclasses.related_model import RelatedModel


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

        related_models = [
            RelatedModel(model="subcategory", attributes=["slug"]),
            RelatedModel(model="subcategory__category", attributes=["slug"]),
        ]
        bouquets = self.get_recommended_items_with_first_image(
            model=Bouquet,
            image_model=BouquetImage,
            related_models=related_models,
            image_filter_field="bouquet",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        products = self.get_recommended_items_with_first_image(
            model=Product,
            image_model=ProductImage,
            related_models=related_models,
            image_filter_field="product",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )

        context["recommended_bouquets"] = bouquets
        context["recommended_products"] = products
        context["products_cart"] = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        context["bouquets_cart"] = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        context["individual_order_form"] = IndividualOrderForm()
        context["seo_block"] = SeoBlock.objects.first()
        return context

    def get_recommended_items_with_first_image(
        self,
        model: Product | Bouquet,
        image_model: ProductImage | BouquetImage,
        related_models: list[RelatedModel],
        image_filter_field: Literal["product"] | Literal["bouquet"],
        order_fields: list[str],
    ) -> BaseManager[Product] | BaseManager[Bouquet]:
        """
        A function to retrieve objects with an annotated first image.

        :param model: The model for which the query is executed (e.g., Bouquet or Product).
        :param image_model: The image model that will be used for the subquery (e.g., BouquetImage or ProductImage).
        :param related_models: A dictionary where the key is the related model and the value is a list of attributes for that model.
                            For example, {"subcategory": ["slug"], "subcategory__category": ["slug"]}.
        :param filter_field: The field to bind the subquery to (e.g., 'bouquet' for BouquetImage).
        :param order_fields: A list of fields to order the result by.
        :return: A queryset with annotated objects.
        """

        first_image_subquery = (
            image_model.objects.filter(**{image_filter_field: OuterRef("pk")})
            .order_by("id")[:1]
            .values("image")
        )
        select_related_fields = []
        for related_model in related_models:
            for attr in related_model.attributes:
                select_related_fields.append(f"{related_model.model}__{attr}")

        return (
            model.objects.select_related(*[rm.model for rm in related_models])
            .only(
                "name",
                "price",
                "slug",
                *select_related_fields,
            )
            .annotate(first_image_uri=Subquery(first_image_subquery))
            .order_by(*order_fields)[:12]
        )


class IndividualOrderView(CreateView):
    form_class = IndividualOrderForm
    http_method_names = ["post"]

    def form_valid(self, form: IndividualOrderForm):
        form.save(commit=True, user=self.request.user)
        return JsonResponse(
            {
                "detail": _("Мы скоро с Вами свяжемся, а пока выпейте чаю 😊"),
                "status": "success",
            },
            status=201,
        )

    def form_invalid(self, form):
        return JsonResponse(
            {
                "detail": _("Вы неправильно заполнили форму:"),
                "errors": form.errors.as_json(),
                "status": 400,
            },
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
            {
                "detail": _("Метод не разрешен. Используйте POST."),
                "status": 405,
            },
            status=405,
        )
