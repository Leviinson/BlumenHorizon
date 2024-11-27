from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from cart.cart import BouquetCart, ProductCart
from catalogue.models import (
    Bouquet,
    BouquetCategory,
    BouquetImage,
    Product,
    ProductCategory,
    ProductImage,
)
from core.services.dataclasses.related_model import RelatedModel
from core.services.get_recommended_items import get_recommended_items_with_first_image
from core.services.mixins.views import CommonContextMixin

from .forms import IndividualOrderForm
from .models import (
    AboutUsPageModel,
    ContactsPageModel,
    DeliveryPageModel,
    FAQPageModel,
    MainPageModel,
    MainPageSeoBlock,
    MainPageSliderImages,
)


class MainPageView(CommonContextMixin, TemplateView):
    template_name = "mainpage/index.html"
    http_method_names = ["get"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["slider_images"] = MainPageSliderImages.objects.filter(
            is_active=True
        ).all()

        related_models = [
            RelatedModel(model="subcategory", attributes=["slug", "name"]),
            RelatedModel(model="subcategory__category", attributes=["slug"]),
        ]
        bouquets = get_recommended_items_with_first_image(
            model=Bouquet,
            image_model=BouquetImage,
            related_models=related_models,
            image_filter_field="bouquet",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
        )
        products = get_recommended_items_with_first_image(
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
        context["seo_block"] = MainPageSeoBlock.objects.first()
        context["products_categories"] = (
            ProductCategory.objects.filter(is_active=True)
            .prefetch_related("subcategories")
            .only(
                "name",
                "slug",
                "code_value",
                "subcategories__code_value",
                "subcategories__slug",
                "subcategories__name",
            )
        )
        context["bouquets_categories"] = (
            BouquetCategory.objects.filter(is_active=True)
            .prefetch_related("subcategories")
            .only(
                "name",
                "slug",
                "code_value",
                "subcategories__code_value",
                "subcategories__slug",
                "subcategories__name",
            )
        )
        page_model = MainPageModel.objects.first()
        context["meta_tags"] = page_model.meta_tags
        context["json_ld_description"] = page_model.json_ld_description
        context["description"] = page_model.description
        context["contact_us_absolute_url"] = self.request.build_absolute_uri(
            reverse_lazy("mainpage:contact")
        )
        context["delivery_absolute_url"] = self.request.build_absolute_uri(
            reverse_lazy("mainpage:delivery")
        )
        context["individual_order_negotiate_url"] = self.request.build_absolute_uri(
            reverse_lazy("mainpage:individual-order-negotiate")
        )
        return context


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


class AboutUsView(CommonContextMixin, TemplateView):
    template_name = "mainpage/filler.html"
    http_method_names = [
        "get",
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = AboutUsPageModel.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        context["url"] = reverse_lazy("mainpage:about")
        return context


class AboutDeliveryView(CommonContextMixin, TemplateView):
    template_name = "mainpage/filler.html"
    http_method_names = [
        "get",
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = DeliveryPageModel.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        context["url"] = reverse_lazy("mainpage:delivery")
        return context


class ContactUsView(CommonContextMixin, TemplateView):
    template_name = "mainpage/filler.html"
    http_method_names = [
        "get",
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = ContactsPageModel.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        context["url"] = reverse_lazy("mainpage:contact")
        return context


class FAQView(CommonContextMixin, TemplateView):
    template_name = "mainpage/filler.html"
    http_method_names = [
        "get",
    ]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page = FAQPageModel.objects.first()
        context["page"] = page
        context["meta_tags"] = page.meta_tags
        return context
