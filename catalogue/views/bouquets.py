from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import ContextMixin, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

from cart.cart import BouquetCart
from core.services.mixins.views import CommonContextMixin

from ..filters import BouquetFilter
from ..models import Bouquet, BouquetImage, BouquetsSizes, Color, Flower
from ..services.views import DetailViewMixin, ListViewMixin


class NonExistentSizeSelected(Exception):
    pass


class BouquetView(
    DetailViewMixin,
    CommonContextMixin,
    DetailView,
):
    model = Bouquet
    queryset = (
        Bouquet.objects.filter(is_active=True)
        .prefetch_related(
            "images",
            "colors",
            "flowers",
            "sizes",
        )
        .select_related(
            "subcategory",
            "subcategory__category",
        )
        .only(
            "name",
            "slug",
            "price",
            "amount_of_flowers",
            "description",
            "specs",
            "images",
            "discount",
            "subcategory__slug",
            "subcategory__name",
            "subcategory__category__slug",
            "subcategory__category__name",
            "colors__name",
            "colors__hex_code",
            "flowers__name",
        )
    )
    context_object_name = "product"
    slug_url_kwarg = "bouquet_slug"
    template_name = "products/bouquets/bouquet_detail.html"
    detail_url_name = "bouquet-details"
    category_url_name = "bouquets-category"
    subcategory_url_name = "bouquets-subcategory"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            context = self.get_context_data(object=self.object)
        except NonExistentSizeSelected:
            pass
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bouquets_cart"] = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        context["selected_bouquet_size"] = self.__get_bouquet_size(
            self.request, self.object
        )
        return context

    @staticmethod
    def __get_bouquet_size(
        request: HttpRequest, bouquet_obj: Bouquet
    ) -> None | BouquetsSizes | NonExistentSizeSelected:
        """
        Determines the bouquet size selected by the user and returns
        the size object if it exists.

        :param request: The HttpRequest object containing GET parameters,
        where the selected bouquet size may be specified.
        :param object: The Bouquet object containing associated sizes.
        :return:
            - `BouquetsSizes` object if the selected size exists for this bouquet.

            - `None` if no size is specified in the request.

        :raises NonExistentSizeSelected: If the requested size
        does not exist for the bouquet.
        """
        if bouquet_size := request.GET.get("size"):
            if bouquet_size_obj := bouquet_obj.sizes.filter(
                diameter=bouquet_size
            ).first():
                return bouquet_size_obj
            raise NonExistentSizeSelected()
        else:
            return None


class BouquetListView(
    ListViewMixin,
    CommonContextMixin,
    FilterView,
    TemplateResponseMixin,
    ContextMixin,
):
    model = Bouquet
    queryset = Bouquet.objects.select_related(
        "subcategory__category",
    ).only(
        "slug",
        "name",
        "price",
        "images",
        "discount",
        "subcategory__slug",
        "subcategory__category__slug",
        "colors__name",
        "colors__hex_code",
        "flowers__name",
    )
    context_object_name = "products"
    template_name = "products/bouquets/bouquet_list.html"
    filterset_class = BouquetFilter
    extra_context = {"title": _("Каталог букетов")}
    image_model = BouquetImage
    image_model_related_name = "bouquet"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["colors"] = Color.objects.only("name", "hex_code").all()
        context["flowers"] = Flower.objects.only("name").all()
        context["bouquets_cart"] = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        return context
