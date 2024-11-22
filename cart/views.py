from decimal import Decimal
from typing import Type

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView, FormView

from core.services.mixins.views import CommonContextMixin

from .cart import BouquetCart, ProductCart
from .forms import OrderForm
from .models import Order
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
        site = get_current_site(self.request)
        products_cart = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        bouquets_cart = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )
        order = form.save(
            products_cart=products_cart,
            bouquets_cart=bouquets_cart,
            tax_percent=site.extended.tax_percent,
            commit=True,
            user=self.request.user,
        )
        products_cart.clear()
        bouquets_cart.clear()

        order = (
            Order.objects.prefetch_related(
                "products",
                "products__product",
                "bouquets",
                "bouquets__product",
                "products__product__subcategory",
                "bouquets__product__subcategory",
                "products__product__images",
                "bouquets__product__images",
                "bouquets__product__colors",
                "bouquets__product__subcategory__category",
                "products__product__subcategory__category",
            )
            .only(
                "code",
                "name",
                "email",
                "address_form",
                "name",
                "country",
                "city",
                "street",
                "building",
                "postal_code",
                "flat",
                "tax",
                "sub_total",
                "grand_total",
                "recipient_address_form",
                "recipient_name",
                "recipient_phonenumber",
                "products__quantity",
                "bouquets__quantity",
                "products__product__name",
                "products__product__discount",
                "products__product__price",
                "products__product__discount_expiration_datetime",
                "products__product__slug",
                "products__product__subcategory__slug",
                "products__product__subcategory__category__slug",
                "bouquets__product__name",
                "bouquets__product__discount",
                "bouquets__product__price",
                "bouquets__product__discount_expiration_datetime",
                "bouquets__product__slug",
                "bouquets__product__subcategory__slug",
                "bouquets__product__subcategory__category__slug",
                "bouquets__product__colors__name",
                "created_at",
            )
            .get(pk=order.pk)
        )
        currency_symbol = site.extended.currency_symbol
        site_name = site.name
        domain = site.domain
        mail_subject = _("{site_name} | Подтверждение заказа {order_code}").format(
            site_name=site_name, order_code=order.code
        )
        html_message = render_to_string(
            "cart/order_confirmation.html",
            {
                "site_name": site_name,
                "domain": domain,
                "MEDIA_URL": settings.MEDIA_URL,
                "name": order.name,
                "address_form": order.address_form,
                "order_code": order.code,
                "order_date": order.created_at,
                "order_products": order.products,
                "order_bouquets": order.bouquets,
                "recipient_name": order.recipient_name,
                "recipient_phonenumber": order.recipient_phonenumber,
                "country": order.country,
                "city": order.city,
                "street": order.street,
                "building": order.building,
                "flat": order.flat,
                "tax": order.tax,
                "sub_total": order.sub_total,
                "grand_total": order.grand_total,
                "currency": currency_symbol,
                "postal_code": order.postal_code,
            },
        )
        plain_message = strip_tags(html_message)
        self.success_url = reverse_lazy(
            "cart:success-order", kwargs={"order_code": order.code}
        )
        email = EmailMultiAlternatives(mail_subject, plain_message, to=[order.email])
        email.attach_alternative(html_message, "text/html")
        if email.send():
            pass
        else:
            pass

        if "orders" in self.request.session:
            self.request.session["orders"].append(order.code)
            self.request.session.save()
        else:
            self.request.session["orders"] = [
                order.code,
            ]
            self.request.session.save()
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["products_cart"] = ProductCart(
            True, self.request.session, session_key="products_cart"
        )
        context["bouquets_cart"] = BouquetCart(
            True, self.request.session, session_key="bouquets_cart"
        )
        sub_total = context["products_cart"].total + context["bouquets_cart"].total
        tax = sub_total * Decimal(self.current_site.extended.tax_percent / 100)
        context["tax"] = tax
        context["sub_total"] = sub_total
        context["grand_total"] = sub_total + tax
        return context


class CartBouquetAddView(
    CartItemAddMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Букет {product_name} успешно добавлен в корзину.".format(product_name=product.name))

    def get_error_message(self):
        return _("Неизвестная ошибка добавления букета в корзину.")


class CartProductAddView(
    CartItemAddMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Продукт {product_name} успешно добавлен в корзину.".format(product_name=product.name))

    def get_error_message(self):
        return _("Ошибка добавления продукта в корзину.")


class CartBouquetRemoveView(
    CartItemRemoveMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Букет {product_name} успешно убран из корзины.")

    def get_error_message(self):
        return _("Ошибка уменьшения количества букета в корзине.")


class CartProductRemoveView(
    CartItemRemoveMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Продукт {product_name} успешно убран из корзины.".format(product_name=product.name))

    def get_error_message(self):
        return _("Ошибка уменьшения количества продукта в корзине.")


class CartBouquetRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Букет {product_name} успешно удалён из корзины.".format(product_name=product.name))

    def get_error_message(self):
        return _("Ошибка удаления букета из корзины.")


class CartProductRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _("Продукт {product_name} успешно удалён из корзины.".format(product_name=product.name))

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
    http_method_names = [
        "get",
    ]

    def get(self, request, *args, **kwargs):
        self.order_code = self.kwargs["order_code"]
        try:
            self.order = Order.objects.only(
                "created_at", "code", "grand_total", "email", "status"
            ).get(code=self.order_code)
        except Order.DoesNotExist:
            return HttpResponseForbidden()

        if (orders := request.session.get("orders")) and self.order_code in orders:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["order"] = self.order
        context["iban"] = self.current_site.extended.iban
        context["account_name"] = self.current_site.extended.account_name
        return context
