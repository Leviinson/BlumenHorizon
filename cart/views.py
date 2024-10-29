from typing import Type

from carton.cart import Cart
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import BaseFormView

from catalogue.models import Bouquet, Product

from .forms import ProductForm


class CartItemAdd(BaseFormView):
    form_class = ProductForm
    http_method_names = ["post"]

    def form_valid(self, form) -> JsonResponse:
        cart = Cart(self.request.session)
        if form.cleaned_data["is_bouquet"]:
            product = get_object_or_404(
                Bouquet.objects.only("slug", "price", "name"),
                slug=form.cleaned_data["product_or_bouquet_slug"],
            )
        else:
            product = get_object_or_404(
                Product.objects.only("slug", "price", "name"),
                slug=form.cleaned_data["product_or_bouquet_slug"],
            )
        cart.add(product, price=product.price)
        return JsonResponse(
            {
                "message": _(f"Продукт '{product.name}' успешно добавлен в корзину."),
                "status": "success",
            },
            status=201,
        )

    def form_invalid(self, form) -> JsonResponse:
        return JsonResponse(
            {
                "message": _(
                    "Ошибка добавления продукта в корзину. Обновите страницу."
                ),
                "errors": form.errors,
                "status": "error",
            },
            status=400,
        )
    
    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
                {
                    "message": _("Метод не разрешен. Используйте POST."),
                    "status": "error",
                },
                status=405,
            )


class CartItemRemove(BaseFormView):
    form_class = ProductForm
    http_method_names = ["post"]

    def form_valid(self, form) -> JsonResponse:
        cart = Cart(self.request.session)
        if form.cleaned_data["is_bouquet"]:
            product = get_object_or_404(
                Bouquet.objects.only("slug", "price", "name"),
                slug=form.cleaned_data["product_or_bouquet_slug"],
            )
        else:
            product = get_object_or_404(
                Product.objects.only("slug", "price", "name"),
                slug=form.cleaned_data["product_or_bouquet_slug"],
            )
        cart.remove(product)
        return JsonResponse(
            {
                "message": _(f"Продукт '{product.name}' успешно удалён из корзины."),
                "status": "success",
            },
            status=200,
        )

    def form_invalid(self, form) -> JsonResponse:
        return JsonResponse(
            {
                "message": _("Ошибка удаления продукта из корзины. Обновите страницу."),
                "errors": form.errors,
                "status": "error",
            },
            status=400,
        )
    
    def http_method_not_allowed(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(
                {
                    "message": _("Метод не разрешен. Используйте POST."),
                    "status": "error",
                },
                status=405,
            )


def cart_clear(request: HttpRequest) -> Type[JsonResponse]:
    if request.method == "POST":
        cart = Cart(request.session)
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
