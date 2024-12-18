from decimal import Decimal
from typing import Type

import stripe
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Prefetch
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView, FormView

from accounts.models import User
from catalogue.models import Bouquet, BouquetImage, Product, ProductImage
from core.services.caching import set_or_get_from_cache
from core.services.dataclasses.related_model import RelatedModel
from core.services.decorators.db.db_queries import inspect_db_queries
from core.services.get_recommended_items import get_recommended_items_with_first_image
from core.services.mixins.views import CommonContextMixin
from extended_contrib_models.models import ExtendedSite

from .cart import BouquetCart, ProductCart
from .forms import OrderForm
from .models import Order, OrderBouquets, OrderProducts
from .services.mixins import (
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

    @inspect_db_queries
    def form_valid(self, form: OrderForm):
        site = (
            ExtendedSite.objects.select_related("site")
            .only(
                "site__name",
                "site__domain",
                "tax_percent",
                "currency_code",
                "currency_symbol",
            )
            .first()
        )
        name = site.site.name
        domain = site.site.domain
        tax_percent = set_or_get_from_cache(
            "tax_percent",
            60 * 15,
        )
        currency_code = site.currency_code.lower()
        currency_symbol = site.currency_symbol

        products_cart = ProductCart(
            session=self.request.session, session_key="products_cart"
        )
        bouquets_cart = BouquetCart(
            session=self.request.session, session_key="bouquets_cart"
        )

        order = self.save_order_in_db(
            form,
            products_cart,
            bouquets_cart,
            tax_percent,
            self.request.user,
        )

        order_products, order_bouquets, line_items = (
            self.generate_line_items_and_attach_first_images(
                order.products,
                order.bouquets,
                currency_code,
                domain,
            )
        )

        # self.send_order_confirmation_email(
        #     order,
        #     order_products,
        #     order_bouquets,
        #     currency_symbol,
        #     name,
        #     domain,
        # )
        self.add_order_in_session(self.request, order)
        self.success_url = self.generate_payment_page_url(order.email, line_items)
        return super().form_valid(form)

    @staticmethod
    def generate_payment_page_url(
        customer_email: str, line_items: list[dict[str, str | int]]
    ) -> str:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            customer_email=customer_email,
            success_url="https://blumenhorizon.de/contact/",
            cancel_url="https://blumenhorizon.de/delivery/",
            metadata={
                "test4": "asd",
            },
            billing_address_collection="required",
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
        return order_products, order_bouquets, line_items

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
    def send_order_confirmation_email(
        order: Order,
        order_products: QuerySet[OrderProducts],
        order_bouquets: QuerySet[OrderBouquets],
        currency_symbol: str,
        site_name: str,
        domain: str,
    ):
        # TODO: перенести в celery
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
                "address_form": dict(Order.ADDRESS_FORM_CHOICES).get(
                    order.address_form, "Dear"
                ),
                "order_code": order.code,
                "order_date": order.created_at,
                "order_products": order_products,
                "order_bouquets": order_bouquets,
                "recipient_name": order.recipient_name,
                "recipient_phonenumber": order.recipient_phonenumber,
                "country": order.country,
                "city": order.city,
                "street": order.street,
                "building": order.building,
                "flat": order.flat,
                "delivery_date": order.delivery_date,
                "delivery_time": order.delivery_time,
                "message_card": order.message_card,
                "instructions": order.instructions,
                "tax": order.tax,
                "sub_total": order.sub_total,
                "grand_total": order.grand_total,
                "currency": currency_symbol,
                "postal_code": order.postal_code,
            },
        )
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(mail_subject, plain_message, to=[order.email])
        email.attach_alternative(html_message, "text/html")
        if email.send():
            pass
        else:
            pass

    @staticmethod
    def add_order_in_session(request: HttpRequest, order: Order):
        if "orders" in request.session:
            request.session["orders"].append(order.code)
            request.session.save()
        else:
            request.session["orders"] = [
                order.code,
            ]
            request.session.save()

    @staticmethod
    def save_order_in_db(
        form: OrderForm,
        products_cart: ProductCart,
        bouquets_cart: BouquetCart,
        tax_percent: int,
        user: User,
    ) -> Order:
        order = form.save(
            products_cart=products_cart,
            bouquets_cart=bouquets_cart,
            tax_percent=tax_percent,
            commit=True,
            user=user,
        )
        product_images_prefetch = Prefetch(
            "product_images",
            queryset=ProductImage.objects.only("id", "image", "image_alt"),
            to_attr="prefetched_images",  # Поле для доступа к изображениям
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
        context["grand_total"] = sub_total + tax
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
