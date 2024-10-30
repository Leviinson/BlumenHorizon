from carton.cart import Cart

from catalogue.models import Bouquet, Product


class ProductCart(Cart):
    def get_product_model(self):
        return Product

class BouquetCart(Cart):
    def get_product_model(self):
        return Bouquet
    