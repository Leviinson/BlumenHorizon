import logging
from abc import ABC, abstractmethod
from typing import Type

from django.db import transaction
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from catalogue.models import Bouquet, Product
from core.services.mixins.views import CommonContextMixin

from .cart import BouquetCart, ProductCart
from .forms import CartForm
from .services.dataclasses import CartAction


class CartView(CommonContextMixin, TemplateView):
    template_name = "cart/index.html"
    extra_context = {"title": _("Корзина товаров")}

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


class CartEditAbstractMixin(ABC):
    cart_action: CartAction = None
    form_class = CartForm
    http_method_names = ["post"]
    success_message = ""
    error_message = ""

    @abstractmethod
    def get_product(self, form: CartForm):
        pass

    @abstractmethod
    def get_cart(self) -> Type[ProductCart | BouquetCart]:
        pass

    @abstractmethod
    def get_remaining_cart(self) -> Type[ProductCart | BouquetCart]:
        pass

    @abstractmethod
    def get_success_message(self, product: Product | Bouquet):
        pass

    @abstractmethod
    def get_error_message(self) -> str:
        pass

    def form_valid(self, form) -> JsonResponse:
        cart = self.get_cart()
        remaining_cart = self.get_remaining_cart()
        product: Product | Bouquet = self.get_product(form)
        match self.cart_action.action:
            case "add":
                with transaction.atomic():
                    cart.add(product, price=product.price)
                    product.amount_of_savings += 1
                    product.save(update_fields=["amount_of_savings"])
            case "remove":
                cart.remove(product)
            case "remove_single":
                cart.remove_single(product)
            case _:
                logger = logging.getLogger("django.request")
                logger.log(level="ERROR", msg="Wrong cart action selected.")
                return self._error_response(
                    _(
                        "Ой-ой, мы неправильно обработали Вашу корзину. Скоро администрация это исправит!"
                    )
                )

        return self._action_response(
            message=self.get_success_message(product),
            status=201,
            grand_total=cart.total + remaining_cart.total,
            quantity=cart.get_quantity(product),
            subtotal=cart.get_subtotal(product),
            count=cart.count + remaining_cart.count,
        )

    def form_invalid(self, form) -> JsonResponse:
        return self._error_response(
            message=self.get_error_message(),
            errors=form.errors,
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return self._error_response(
            message=_("Метод не разрешен. Используйте POST."),
            status=405,
        )

    def _action_response(
        self,
        message: str,
        status: int,
        grand_total: float,
        subtotal: float,
        quantity: int,
        count: int,
    ) -> JsonResponse:
        return JsonResponse(
            {
                "message": message,
                "status": "success",
                "grand_total": grand_total,
                "subtotal": subtotal,
                "quantity": quantity,
                "count": count,
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


class CartItemAddMixin:
    cart_action = CartAction("add")


class CartItemRemoveMixin:
    cart_action = CartAction("remove")


class CartItemRemoveSingleMixin:
    cart_action = CartAction("remove_single")


class CartBouquetEditMixin:
    def get_product(self, form):
        return get_object_or_404(
            Bouquet.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return BouquetCart(session=self.request.session, session_key="bouquets_cart")

    def get_remaining_cart(self):
        return ProductCart(session=self.request.session, session_key="products_cart")


class CartProductEditMixin:
    def get_product(self, form):
        return get_object_or_404(
            Product.objects.only("slug", "price", "name"),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return ProductCart(session=self.request.session, session_key="products_cart")

    def get_remaining_cart(self):
        return BouquetCart(session=self.request.session, session_key="bouquets_cart")


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
                "message": _("Корзина очищена"),
                "status": "success",
                "grand_total": product_cart.total + bouquet_cart.total,
                "count": product_cart.count + bouquet_cart.count,
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
