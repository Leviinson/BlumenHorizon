import logging
import os

from django.utils.translation import activate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from stripe import SignatureVerificationError, Webhook

from cart.models import Order
from core.services.utils.carts import clear_user_cart

from ..exceptions import OrderNotFound
from .order_confirmation import send_order_confirmation_email
from .order_repository import OrderRepository
from .types import StripeEventDict


def get_order_by_code(order_code: str) -> Order:
    """
    Возвращает заказ из базы данных по указанному коду заказа.

    Параметры:
    - order_code (str): Код заказа для поиска.

    Возвращает:
    - Order: Экземпляр модели заказа.

    Исключения:
    - Order.DoesNotExist: Если заказ с указанным кодом не найден.
    """
    return Order.objects.only(
        "session_key",
        "email",
        "created_at",
        "name",
        "address_form",
        "recipient_name",
        "recipient_phonenumber",
        "country",
        "city",
        "street",
        "building",
        "flat",
        "postal_code",
        "delivery_date",
        "delivery_time",
        "message_card",
        "instructions",
        "tax",
        "sub_total",
        "grand_total",
        "language_code",
    ).get(code=order_code)


def update_order_status(order: Order) -> None:
    """
    Обновляет статус заказа на "обработан".

    Параметры:
    - order (Order): Экземпляр модели заказа, который нужно обновить.
    """
    order.status = order.STATUS_CHOICES[0][0]
    order.save(update_fields=["status"])


def verify_stripe_webhook(
    request: Request,
) -> tuple[StripeEventDict | None, Response | None]:
    """Проверяет подпись и извлекает событие из webhook-запроса."""
    try:
        return (
            Webhook.construct_event(
                request.body,
                request.headers.get("STRIPE_SIGNATURE"),
                os.getenv("STRIPE_WEBHOOK_SECRET"),
            ).to_dict(),
            None,
        )
    except ValueError as e:
        logging.getLogger("django_stripe_debug").debug(e, stack_info=True)
        return None, Response("Invalid payload", status=status.HTTP_400_BAD_REQUEST)
    except SignatureVerificationError as e:
        logging.getLogger("django_stripe_debug").debug(e, stack_info=True)
        return None, Response("Invalid signature", status=status.HTTP_400_BAD_REQUEST)


def process_order(event_dict):
    """Извлекает код заказа и обновляет его статус."""
    try:
        order_code = OrderRepository.get_order_code(event_dict)
        if not order_code:
            raise OrderNotFound(
                f"Пришла оплата на Stripe с отсутствующим кодом заказа:\n\n{event_dict}"
            )
        order = get_order_by_code(order_code)
        return order
    except Order.DoesNotExist:
        raise OrderNotFound(
            f"Пришла оплата на Stripe с недействительным кодом заказа:\n\n{event_dict}"
        )


def handle_order_confirmation(order):
    """Отправляет подтверждение заказа и обновляет его статус."""
    activate(order.language_code)
    order_products = order.products.all()
    order_bouquets = order.bouquets.all()
    for order_product in order_products:
        order_product.product.first_image = order_product.product.images.first()
    for order_bouquet in order_bouquets:
        order_bouquet.product.first_image = order_bouquet.product.images.first()

    send_order_confirmation_email(order, order_products, order_bouquets)
    update_order_status(order)


def try_clear_cart(order):
    """Пытается очистить корзину пользователя."""
    try:
        clear_user_cart(order.session_key)
    except Exception as e:
        logging.getLogger("django_stripe_debug").debug(e, stack_info=True)
