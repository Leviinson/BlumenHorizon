from abc import ABC, abstractmethod
from typing import Type

from carton.cart import Cart
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from catalogue.models import Bouquet, Product
from core.services.mixins.views import CommonContextMixin

from .cart import BouquetCart, ProductCart
from .forms import CartForm


class CartView(CommonContextMixin, TemplateView):
    template_name = "cart/cart.html"


class BaseCartView(BaseFormView, ABC):
    form_class = CartForm
    http_method_names = ["post"]

    @abstractmethod
    def get_product(self, form):
        pass

    @abstractmethod
    def get_cart(self) -> Type[Cart]:
        pass

    def form_valid(self, form) -> JsonResponse:
        cart = self.get_cart()
        product = self.get_product(form)
        cart.add(product, price=product.price)
        return self._action_response(
            message=_("Продукт '{name}' успешно добавлен в корзину.").format(
                name=product.name
            ),
            status=201,
        )

    def form_invalid(self, form) -> JsonResponse:
        return self._error_response(
            message=_("Ошибка добавления продукта в корзину. Обновите страницу."),
            errors=form.errors,
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return self._error_response(
            message=_("Метод не разрешен. Используйте POST."),
            status=405,
        )

    def _action_response(self, message: str, status: int) -> JsonResponse:
        return JsonResponse(
            {
                "message": message,
                "status": "success",
            },
            status=status,
        )

    def _error_response(
        self, message: str, errors=None, status: int = 400
    ) -> JsonResponse:
        response_data = {
            "message": message,
            "status": "error",
        }
        if errors:
            response_data["errors"] = errors
        return JsonResponse(response_data, status=status)


class CartBouquetAdd(BaseCartView):
    def get_product(self, form):
        return get_object_or_404(
            Bouquet.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return BouquetCart(self.request.session, session_key="bouquets_cart")


class CartProductAdd(BaseCartView):

    def get_product(self, form):
        return get_object_or_404(
            Product.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return ProductCart(self.request.session, session_key="products_cart")
    
class BaseCartRemoveView(BaseFormView, ABC):
    form_class = CartForm
    http_method_names = ["post"]

    @abstractmethod
    def get_product(self, form):
        pass

    @abstractmethod
    def get_cart(self) -> Type[Cart]:
        pass

    def form_valid(self, form) -> JsonResponse:
        cart = self.get_cart()
        product = self.get_product(form)
        cart.remove(product)
        return self._action_response(
            message=_("Продукт '{name}' успешно удалён из корзины.").format(name=product.name),
            status=200,
        )

    def form_invalid(self, form) -> JsonResponse:
        return self._error_response(
            message=_("Ошибка удаления продукта из корзины. Обновите страницу."),
            errors=form.errors,
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return self._error_response(
            message=_("Метод не разрешен. Используйте POST."),
            status=405,
        )

    def _action_response(self, message: str, status: int) -> JsonResponse:
        return JsonResponse(
            {
                "message": message,
                "status": "success",
            },
            status=status,
        )

    def _error_response(self, message: str, errors=None, status: int = 400) -> JsonResponse:
        response_data = {
            "message": message,
            "status": "error",
        }
        if errors:
            response_data["errors"] = errors
        return JsonResponse(response_data, status=status)


class CartBouquetRemove(BaseCartRemoveView):
    def get_product(self, form):
        return get_object_or_404(
            Bouquet.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return BouquetCart(self.request.session, session_key="bouquets_cart")


class CartProductRemove(BaseCartRemoveView):
    def get_product(self, form):
        return get_object_or_404(
            Product.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return ProductCart(self.request.session, session_key="products_cart")

def cart_clear(request: HttpRequest) -> Type[JsonResponse]:
    if request.method == "POST":
        product_cart = ProductCart(request.session, session_key="products_cart")
        bouquet_cart = BouquetCart(request.session, session_key="bouquets_cart")
        for cart in (product_cart, bouquet_cart):
            cart.clear()
        return JsonResponse(
            {
                "message": _("Корзина успешно очищена."),
                "status": "success",
            },
            status=200,
        )
    return JsonResponse(
        {
            "message": _("Метод не разрешен. Используйте POST."),
            "status": "error",
        },
        status=405,
    )
