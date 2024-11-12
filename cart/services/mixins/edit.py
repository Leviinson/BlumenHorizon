import logging
from abc import ABC, abstractmethod
from typing import Type

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from cart.cart import BouquetCart, ProductCart
from cart.forms import CartForm
from cart.services.dataclasses import CartAction
from catalogue.models import Bouquet, Product


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
    
    def form_valid(self, form: CartForm) -> JsonResponse:
        cart = self.get_cart()
        remaining_cart = self.get_remaining_cart()
        product: Product | Bouquet = self.get_product(form)

        match self.cart_action.action:
            case "add":
                with transaction.atomic():
                    cart.add(
                        product,
                        price=product.discount_price,
                    )
                    product.amount_of_savings += 1
                    product.subcategory.amount_of_savings += 1
                    product.subcategory.save(update_fields=["amount_of_savings"])
                    product.subcategory.category.amount_of_savings += 1
                    product.subcategory.category.save(
                        update_fields=["amount_of_savings"]
                    )
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
            detail=self.get_success_message(product),
            status=201,
            grand_total=cart.total + remaining_cart.total,
            quantity=cart.get_quantity(product),
            subtotal=cart.get_subtotal(product),
            count=cart.count + remaining_cart.count,
        )

    def form_invalid(self, form) -> JsonResponse:
        return self._error_response(
            detail=self.get_error_message(),
            errors=form.errors,
            status=400,
        )

    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return self._error_response(
            detail=_("Метод не разрешен. Используйте POST."),
            status=405,
        )

    def _action_response(
        self,
        detail: str,
        status: int,
        grand_total: float,
        subtotal: float,
        quantity: int,
        count: int,
    ) -> JsonResponse:
        return JsonResponse(
            {
                "detail": detail,
                "status": "success",
                "grand_total": grand_total,
                "subtotal": subtotal,
                "quantity": quantity,
                "count": count,
            },
            status=status,
        )

    def _error_response(
        self, detail: str, errors=None, status: int = 400
    ) -> JsonResponse:
        response_data = {
            "detail": detail,
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
            Bouquet.objects.select_related("subcategory", "subcategory__category").only(
                "slug",
                "price",
                "discount",
                "name",
                "amount_of_savings",
                "subcategory__amount_of_savings",
                "subcategory__category__amount_of_savings",
            ),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return BouquetCart(session=self.request.session, session_key="bouquets_cart")

    def get_remaining_cart(self):
        return ProductCart(session=self.request.session, session_key="products_cart")


class CartProductEditMixin:
    def get_product(self, form):
        return get_object_or_404(
            Product.objects.select_related("subcategory", "subcategory__category").only(
                "slug",
                "price",
                "discount",
                "name",
                "amount_of_savings",
                "subcategory__amount_of_savings",
                "subcategory__category__amount_of_savings",
            ),
            slug=form.cleaned_data["product_slug"],
        )

    def get_cart(self):
        return ProductCart(session=self.request.session, session_key="products_cart")

    def get_remaining_cart(self):
        return BouquetCart(session=self.request.session, session_key="bouquets_cart")
