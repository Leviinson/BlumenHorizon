from django.contrib.sessions.backends.base import SessionBase
from django.db.models import OuterRef, Subquery
from django.db.models.query import QuerySet

from carton.cart import Cart
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage


class CartMixin:
    image_model: ProductImage | BouquetImage = None
    image_model_related_name: str = ""

    def __init__(
        self,
        with_images: bool = False,
        session: SessionBase = None,
        session_key: str = None,
        *args,
        **kwargs,
    ):
        self.with_images = with_images
        return super().__init__(session, session_key, *args, **kwargs)

    def get_quantity(self, product):
        if product in self.products:
            return self._items_dict[product.pk].quantity

    def get_subtotal(self, product):
        if product in self.products:
            return self._items_dict[product.pk].subtotal

    def filter_products(
        self, queryset: QuerySet[Product | Bouquet]
    ) -> QuerySet[Product | Bouquet]:
        qs = super().filter_products(queryset)
        optimized_queryset: QuerySet = qs.select_related(
            "subcategory", "subcategory__category"
        )
        from django.utils.translation import get_language

        language = get_language()
        if self.with_images:
            first_image_subquery = self.image_model.objects.filter(
                **{
                    self.image_model_related_name: OuterRef("pk"),
                }
            ).order_by("id")[:1]
            optimized_queryset = optimized_queryset.annotate(
                first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
                first_image_alt=Subquery(
                    first_image_subquery.values(f"image_alt_{language}")[:1]
                ),
            )
        optimized_queryset = optimized_queryset.only(
            "name",
            "slug",
            "price",
            "discount",
            "discount_expiration_datetime",
            "is_active",
            "subcategory__is_active",
            "subcategory__category__is_active",
            "subcategory__slug",
            "subcategory__category__slug",
        )
        return optimized_queryset


class ProductCart(CartMixin, Cart):
    image_model = ProductImage
    image_model_related_name = "product"

    def get_product_model(self):
        return Product


class BouquetCart(CartMixin, Cart):
    image_model = BouquetImage
    image_model_related_name = "bouquet"

    def get_product_model(self):
        return Bouquet
