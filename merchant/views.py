import logging
import os

import stripe
import stripe.error
import stripe.webhook
from django.utils.translation import activate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from cart.models import Order
from core.services.utils.carts import clear_user_cart
from tg_bot.main import send_message_to_telegram

from .services import OrderRepository, send_order_confirmation_email

logger = logging.getLogger("django_stripe")


class OrderNotFound(Exception):
    """Исключение, которое генерируется при отсутствии заказа с указанным кодом."""

    pass


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


@api_view(["POST"])
def stripe_webhook(request: Request):
    """
    Обрабатывает webhook от Stripe для подтверждения платежей.

    Параметры:
    - request (Request): Объект HTTP-запроса, содержащий данные webhook от Stripe.

    Действия:
    - Проверяет подпись webhook.
    - Извлекает код заказа из данных события.
    - Отправляет подтверждение заказа на email пользователя.
    - Обновляет статус заказа в базе данных.
    - Очищает корзину пользователя.

    Возвращает:
    - Response: HTTP-ответ с кодом состояния:
      - 200: Если webhook обработан успешно.
      - 400: Если проверка подписи или данных не удалась.
      - 500: Если возникла внутренняя ошибка сервера.

    Исключения:
    - OrderNotFound: Если заказ с указанным кодом не найден.
    """
    try:
        try:
            event_dict = stripe.Webhook.construct_event(
                request.body,
                request.headers.get("STRIPE_SIGNATURE"),
                os.getenv("STRIPE_WEBHOOK_SECRET"),
            ).to_dict()
        except ValueError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid payload", status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid signature", status.HTTP_400_BAD_REQUEST)

        try:
            order_code = OrderRepository.get_order_code(event_dict)
            order = get_order_by_code(order_code)
        except Order.DoesNotExist:
            send_message_to_telegram(
                "Пришла оплата на страйп с недействительным кодом заказа."
            )
            raise OrderNotFound(
                f"Пришла оплата на страйп с недействительным кодом заказа:\n\n{event_dict}"
            )

        activate(order.language_code)
        order_products = order.products.all()
        order_bouquets = order.bouquets.all()
        for order_product in order_products:
            order_product.product.first_image = order_product.product.images.first()
        for order_bouquet in order_bouquets:
            order_bouquet.product.first_image = order_bouquet.product.images.first()

        send_order_confirmation_email(order, order_products, order_bouquets)
        update_order_status(order)

        try:
            clear_user_cart(order.session_key)
        except Exception as e:
            logger.debug(e)

    except Exception as e:
        logger.debug(e, stack_info=True)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)
