from typing import Type

from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView, FormView

from core.services.mixins.views import CommonContextMixin

from .cart import BouquetCart, ProductCart
from .forms import OrderForm
from .services.mixins import (
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    CartItemAddMixin,
    CartItemRemoveMixin,
    CartItemRemoveSingleMixin,
    CartProductEditMixin,
)


class CartView(CommonContextMixin, FormView):
    template_name = "cart/index.html"
    form_class = OrderForm

    def form_valid(self, form: OrderForm):
        product_cart = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        bouquet_cart = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        order = form.save(
            products=product_cart.products,
            bouquets=bouquet_cart.products,
            commit=True,
            user=self.request.user,
        )
        product_cart.clear()
        bouquet_cart.clear()

        if "orders" in self.request.session:
            self.request.session["orders"].append(order.code)
        else:
            self.request.session["orders"] = [order.code,]
        self.success_url = reverse_lazy("cart:success-order", kwargs={"order_code": order.code})
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["products_cart"] = ProductCart(
            True, self.request.session, session_key="products_cart"
        )
        context["bouquets_cart"] = BouquetCart(
            True, self.request.session, session_key="bouquets_cart"
        )
        grand_total = context["products_cart"].total + context["bouquets_cart"].total
        context["grand_total"] = grand_total
        return context


class CartBouquetAddView(
    CartItemAddMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Букет {product.name} успешно добавлен в корзину.")

    def get_error_message(self):
        return _("Неизвестная ошибка добавления букета в корзину.")


class CartProductAddView(
    CartItemAddMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Продукт {product.name} успешно добавлен в корзину.")

    def get_error_message(self):
        return _("Ошибка добавления продукта в корзину.")


class CartBouquetRemoveView(
    CartItemRemoveMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Букет {product.name} успешно убран из корзины.")

    def get_error_message(self):
        return _("Ошибка уменьшения количества букета в корзине.")


class CartProductRemoveView(
    CartItemRemoveMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Продукт {product.name} успешно убран из корзины.")

    def get_error_message(self):
        return _("Ошибка уменьшения количества продукта в корзине.")


class CartBouquetRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Букет {product.name} успешно удалён из корзины.")

    def get_error_message(self):
        return _("Ошибка удаления букета из корзины.")


class CartProductRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _(f"Продукт {product.name} успешно удалён из корзины.")

    def get_error_message(self):
        return _("Ошибка удаления продукта из корзины.")


def cart_clear(request: HttpRequest) -> Type[JsonResponse]:
    if request.method == "POST":
        product_cart = ProductCart(session=request.session, session_key="products_cart")
        bouquet_cart = BouquetCart(session=request.session, session_key="bouquets_cart")
        for cart in (product_cart, bouquet_cart):
            cart.clear()
        return JsonResponse(
            {
                "detail": _("Корзина очищена"),
                "status": "success",
                "grand_total": product_cart.total + bouquet_cart.total,
                "count": product_cart.count + bouquet_cart.count,
            },
            status=200,
        )
    return JsonResponse(
        {
            "detail": _("Метод не разрешен. Используйте POST."),
            "status": "error",
        },
        status=405,
    )


class SuccessOrderView(CommonContextMixin, TemplateView):
    template_name = "cart/success_order.html"
