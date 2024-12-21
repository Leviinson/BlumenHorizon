from decimal import Decimal
from typing import Any, Type

import stripe
from django.conf import settings
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView, FormView

from accounts.models import User
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.caching import set_or_get_from_cache
from core.services.dataclasses.related_model import RelatedModel
from core.services.mixins.views import CommonContextMixin
from core.services.utils import get_recommended_items_with_first_image

from .cart import BouquetCart, ProductCart
from .forms import OrderForm
from .models import Order, OrderBouquets, OrderProducts
from .services.mixins.edit import (
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    CartItemAddMixin,
    CartItemRemoveMixin,
    CartItemRemoveSingleMixin,
    CartProductEditMixin,
)

stripe.api_key = settings.STRIPE_API_KEY


class CartView(CommonContextMixin, FormView):
    template_name = "cart/index.html"
    form_class = OrderForm

    def form_valid(self, form: OrderForm):
        order = self.save_order(
            form,
            self.request,
        )

        currency_code = set_or_get_from_cache("currency_code", 60 * 15)
        domain = set_or_get_from_cache("domain", 60 * 15)
        line_items = self.generate_line_items_and_attach_first_images(
            order.products,
            order.bouquets,
            currency_code,
            domain,
        )

        self.add_order_in_session(self.request, order.code)
        self.success_url = self.generate_payment_page_url(
            domain,
            order.code,
            customer_email=order.email,
            line_items=line_items,
        )
        return super().form_valid(form)

    @staticmethod
    def generate_payment_page_url(
        domain: str,
        order_code: str,
        customer_email: str,
        line_items: list[dict[str, str | int]],
    ) -> str:
        checkout_session = stripe.checkout.Session.create(
            billing_address_collection="required",
            line_items=line_items,
            mode="payment",
            customer_email=customer_email,
            success_url=f"https://{domain}{reverse_lazy("cart:success-order", kwargs={"order_code": order_code})}",
            cancel_url=f"https://{domain}{reverse_lazy("cart:show")}",
            metadata={
                "order_code": order_code,
            },
            payment_method_types=[
                "card",
                "giropay",
                "ideal",
                "klarna",
                "sofort",
                "paypal",
                "revolut_pay",
                "link",
            ],
        )
        return checkout_session.url

    def generate_line_items_and_attach_first_images(
        self,
        order_products: BaseManager[OrderProducts],
        order_bouquets: BaseManager[OrderBouquets],
        currency: str,
        domain: str,
    ) -> tuple[
        QuerySet[OrderProducts], QuerySet[OrderBouquets], list[dict[str, str | int]]
    ]:
        line_items = []
        for order_product in order_products.all():
            order_product.product.first_image = order_product.product.images.first()
            line_items.append(
                self.create_line_item(
                    order_product, order_product.quantity, currency, domain
                )
            )
        for order_bouquet in order_bouquets.all():
            order_bouquet.product.first_image = order_bouquet.product.images.first()
            line_items.append(
                self.create_line_item(
                    order_bouquet, order_bouquet.quantity, currency, domain
                )
            )
        return line_items

    @staticmethod
    def create_line_item(
        order_product: OrderBouquets | OrderProducts,
        quantity: int,
        currency: str,
        domain: str,
    ) -> dict[str, str | int]:
        return {
            "price_data": {
                "currency": currency,
                "product_data": {
                    "name": f"{order_product.product.name}",
                    "images": [
                        f"https://{domain}{order_product.product.first_image.image.url}"
                    ],
                },
                "unit_amount_decimal": f"{order_product.product_tax_price_discounted * 100}",
            },
            "quantity": quantity,
        }

    @staticmethod
    def add_order_in_session(request: HttpRequest, order_code: str):
        if "orders" in request.session:
            request.session["orders"].append(order_code)
            request.session.save()
        else:
            request.session["orders"] = [
                order_code,
            ]
            request.session.save()

    def save_order(self, form: OrderForm, request: HttpRequest):
        from django.utils.translation import get_language

        language_code = get_language()
        products_cart = ProductCart(
            session=request.session, session_key="products_cart"
        )
        bouquets_cart = BouquetCart(
            session=request.session, session_key="bouquets_cart"
        )
        tax_percent = set_or_get_from_cache(
            "tax_percent",
            60 * 15,
        )
        return self.save_order_in_db(
            form,
            products_cart,
            bouquets_cart,
            tax_percent,
            request.user,
            request.session.session_key,
            language_code,
        )

    @staticmethod
    def save_order_in_db(
        form: OrderForm,
        products_cart: ProductCart,
        bouquets_cart: BouquetCart,
        tax_percent: int,
        user: User,
        session_key: Any,
        language_code: str,
    ) -> Order:
        order = form.save(
            products_cart=products_cart,
            bouquets_cart=bouquets_cart,
            tax_percent=tax_percent,
            session_key=session_key,
            language_code=language_code,
            user=user,
        )
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
                "delivery_date",
                "delivery_time",
                "message_card",
                "instructions",
                "tax",
                "sub_total",
                "grand_total",
                "created_at",
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
            )
            .get(pk=order.pk)
        )
        return order

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["products_cart"] = ProductCart(
            True, self.request.session, session_key="products_cart"
        )
        context["bouquets_cart"] = BouquetCart(
            True, self.request.session, session_key="bouquets_cart"
        )
        related_models = [
            RelatedModel(model="subcategory", attributes=["slug", "name"]),
            RelatedModel(model="subcategory__category", attributes=["slug"]),
        ]
        context["recommended_products"] = get_recommended_items_with_first_image(
            model=Product,
            image_model=ProductImage,
            related_models=related_models,
            image_filter_field="product",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
            limit=6,
        )
        context["recommended_bouquets"] = get_recommended_items_with_first_image(
            model=Bouquet,
            image_model=BouquetImage,
            related_models=related_models,
            image_filter_field="bouquet",
            order_fields=[
                "-amount_of_orders",
                "-amount_of_savings",
            ],
            limit=6,
        )

        tax_percent = self.current_site.extended.tax_percent
        grand_total = context["products_cart"].total + context["bouquets_cart"].total
        sub_total = grand_total / Decimal(1 + tax_percent / 100)
        tax = grand_total - sub_total
        context["tax"] = tax
        context["sub_total"] = sub_total
        context["grand_total"] = grand_total
        return context


class CartBouquetAddView(
    CartItemAddMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Букет "{product_name}" успешно добавлен в корзину.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка добавления букета в корзину.")


class CartProductAddView(
    CartItemAddMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Продукт "{product_name}" успешно добавлен в корзину.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка добавления продукта в корзину.")


class CartBouquetRemoveView(
    CartItemRemoveMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Букет "{product_name}" успешно убран из корзины.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка удаления букета из корзины.")


class CartProductRemoveView(
    CartItemRemoveMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Продукт "{product_name}" успешно убран из корзины.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка удаления продукта из корзины.")


class CartBouquetRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartBouquetEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Количество букета "{product_name}" успешно уменьшено.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка уменьшения количества букета в корзине.")


class CartProductRemoveSingleView(
    CartItemRemoveSingleMixin,
    CartProductEditMixin,
    CartEditAbstractMixin,
    BaseFormView,
):
    def get_success_message(self, product):
        return _('Количество продукта "{product_name}" успешно уменьшено.').format(
            product_name=product.name
        )

    def get_error_message(self):
        return _("Ошибка уменьшения количества продукта в корзине.")


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
                "created_at",
                "code",
                "grand_total",
                "email",
                "status",
                "delivery_date",
                "delivery_time",
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
