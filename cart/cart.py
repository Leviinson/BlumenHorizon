from carton.cart import Cart

from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from django.db.models import OuterRef, Subquery


class CartMixin:
    image_model: ProductImage | BouquetImage = None
    image_model_related_name: str = ""

    def get_quantity(self, product):
        if product in self.products:
            return self._items_dict[product.pk].quantity

    def get_subtotal(self, product):
        if product in self.products:
            return self._items_dict[product.pk].subtotal

    def filter_products(self, queryset):
        first_image_subquery = self.image_model.objects.filter(
            **{
                self.image_model_related_name: OuterRef("pk"),
            }
        ).order_by("id")[:1]
        queryset = (
            queryset.select_related("subcategory", "subcategory__category")
            .only(
                "name",
                "slug",
                "price",
                "is_active",
                "subcategory__is_active",
                "subcategory__category__is_active",
            )
            .annotate(
                first_image_uri=Subquery(first_image_subquery.values("image")[:1]),
            )
        )
        qs = super().filter_products(queryset)
        return qs


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
