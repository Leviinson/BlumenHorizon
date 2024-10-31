from carton.cart import Cart

from catalogue.models import Bouquet, Product

class CartMixin:
    def get_quantity(self, product):
        if product in self.products:
            return self._items_dict[product.pk].quantity
        
    def get_subtotal(self, product):
        if product in self.products:
            return self._items_dict[product.pk].subtotal

class ProductCart(CartMixin, Cart):
    def get_product_model(self):
        self.set_quantity
        return Product


class BouquetCart(CartMixin, Cart):
    def get_product_model(self):
        return Bouquet
