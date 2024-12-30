from django.db.models import OuterRef, Subquery
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from catalogue.models import (
    Bouquet,
    BouquetImage,
    BouquetsListPageModel,
    Product,
    ProductImage,
    ProductsListPageModel,
)


class ListViewMixin:
    allow_empty = True
    paginate_by = 8
    image_model: type[ProductImage] | type[BouquetImage]
    page_model: type[ProductsListPageModel] | type[BouquetsListPageModel]

    SORT_OPTIONS = [
        {"name": _("Цена по убыванию"), "value": "pd"},
        {"name": _("Цена по возрастанию"), "value": "pi"},
        {"name": _("По алфавиту"), "value": "alph"},
        {"name": _("Со скидкой"), "value": "disc"},
    ]

    def get_queryset(self):
        from django.utils.translation import get_language

        language = get_language()
        selected_option = self.get_selected_option_for_sorting(self.request.GET)
        queryset = self.get_queryset_for_sorting()
        sorted_queryset = self.sort_queryset_by_selected_option(
            queryset,
            selected_option,
            self.image_model,
            language,
        )
        return sorted_queryset

    @staticmethod
    def get_selected_option_for_sorting(get_params: dict[str, str]):
        return get_params.get("sort", "pd")

    def get_queryset_for_sorting(self) -> QuerySet[Product | Bouquet]:
        return super().get_queryset()

    def sort_queryset_by_selected_option(
        self,
        queryset: QuerySet[Product | Bouquet],
        selected_option: str,
        image_model: ProductImage | BouquetImage,
        language: str,
    ) -> QuerySet[Bouquet | Product]:
        sorted_queryset = self.order_queryset_by_selected_option(
            queryset,
            selected_option,
        )
        queryset_with_active_items = self.filter_queryset_by_active_items(
            sorted_queryset,
        )
        result = self.attach_first_image_to_queryset_items(
            queryset_with_active_items,
            image_model,
            language,
        )
        return result

    @staticmethod
    def order_queryset_by_selected_option(
        queryset: QuerySet[Bouquet | Product], selected_option: str
    ) -> QuerySet[Bouquet | Product]:
        match selected_option:
            case "pd":
                queryset = queryset.order_by("-price")
            case "pi":
                queryset = queryset.order_by("price")
            case "alph":
                queryset = queryset.order_by("name")
            case "disc":
                queryset = queryset.order_by("-discount")
        return queryset

    @staticmethod
    def filter_queryset_by_active_items(
        queryset: QuerySet[Bouquet | Product],
    ) -> QuerySet[Bouquet | Product]:
        queryset = queryset.filter(
            is_active=True,
            subcategory__is_active=True,
            subcategory__category__is_active=True,
        )
        return queryset

    def attach_first_image_to_queryset_items(
        self,
        queryset: QuerySet[Bouquet | Product],
        image_model: ProductImage | BouquetImage,
        language: str,
    ) -> QuerySet[Bouquet | Product]:
        first_image_subquery = image_model.objects.filter(item=OuterRef("pk")).order_by(
            "id"
        )[:1]
        queryset = queryset.annotate(
            first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            first_image_alt=Subquery(
                first_image_subquery.values(f"image_alt_{language}")[:1]
            ),
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sort_options"] = self.SORT_OPTIONS
        page: ProductsListPageModel | BouquetsListPageModel = (
            self.page_model.objects.first()
        )
        context["meta_tags"] = page.meta_tags
        return context


class ProductListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cart"] = ProductCart(
            session=self.request.session, session_key=ProductCart.session_key
        )
        context["add_to_cart_uri"] = reverse_lazy("cart:product-add")
        context["remove_from_cart_uri"] = reverse_lazy("cart:product-remove")
        return context


class BouquetListViewMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cart"] = BouquetCart(
            session=self.request.session, session_key=BouquetCart.session_key
        )
        context["add_to_cart_uri"] = reverse_lazy("cart:bouquet-add")
        context["remove_from_cart_uri"] = reverse_lazy("cart:bouquet-remove")
        return context
