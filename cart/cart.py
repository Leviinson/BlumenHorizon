from carton.cart import Cart
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage

from .services.mixins.base import CartMixin


class ProductCart(CartMixin, Cart):
    image_model = ProductImage
    session_key = "products_cart"

    def get_product_model(self):
        return Product


class BouquetCart(CartMixin, Cart):
    image_model = BouquetImage
    session_key = "bouquets_cart"

    def get_product_model(self):
        return Bouquet
