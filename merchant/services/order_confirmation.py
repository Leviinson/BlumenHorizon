from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from cart.models import Order, OrderBouquets, OrderProducts
from core.services.caching import set_or_get_from_cache


def send_order_confirmation_email(
    order: Order,
    order_products: QuerySet[OrderProducts],
    order_bouquets: QuerySet[OrderBouquets],
):
    currency_symbol = set_or_get_from_cache("currency_symbol", 60 * 15)
    site_name = set_or_get_from_cache("site_name", 60 * 15)
    domain = set_or_get_from_cache("domain", 60 * 15)
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
            "postal_code": order.postal_code,
            "delivery_date": order.delivery_date,
            "delivery_time": order.delivery_time,
            "message_card": order.message_card,
            "instructions": order.instructions,
            "tax": order.tax,
            "sub_total": order.sub_total,
            "grand_total": order.grand_total,
            "currency": currency_symbol,
        },
    )
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(mail_subject, plain_message, to=[order.email])
    email.attach_alternative(html_message, "text/html")
    if email.send():
        pass
    else:
        pass
