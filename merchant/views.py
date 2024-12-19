import logging
import os

import stripe
import stripe.error
import stripe.webhook
from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from cart.cart import BouquetCart, ProductCart
from cart.models import Order
from merchant.services import send_order_confirmation_email
from tg_bot.main import send_message_to_telegram


class OrderNotFound(Exception):
    pass


@api_view(["POST"])
def stripe_webhook(request: Request):
    logger = logging.getLogger("django_stripe")
    try:
        payload = request.body
        sig_header = request.headers.get("STRIPE_SIGNATURE")
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
            )
        except ValueError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid payload", status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            logger.debug(e, stack_info=True)
            return Response("Invalid signature", status.HTTP_400_BAD_REQUEST)

        event_dict = event.to_dict()
        order_code = event_dict["data"]["object"]["meta_data"]["order_code"]
        try:
            order = Order.objects.only(
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
                "currency",
            ).get(code=order_code)
        except Order.DoesNotExist:
            send_message_to_telegram(
                "Пришла оплата на страйп с недействительным кодом заказа."
            )
            raise OrderNotFound(
                f"Пришла оплата на страйп с недействительным кодом заказа:\n\n{event_dict}"
            )
        order.status = order.STATUS_CHOICES[0][0]
        try:
            session = Session.objects.filter(expite_date__lt=timezone.now()).get(
                session_key=order.session_key
            )
            products_cart = ProductCart(True, session, session_key="products_cart")
            bouquets_cart = BouquetCart(True, session, session_key="bouquets_cart")
            products_cart.clear()
            bouquets_cart.clear()
        except Session.DoesNotExist:
            pass
        send_order_confirmation_email(order, order.products, order.bouquets)

    except Exception as e:
        logger.debug(e, stack_info=True)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)
