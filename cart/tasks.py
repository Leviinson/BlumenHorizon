from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.helpers import escape_markdown

from tg_bot import send_message_to_telegram

from .models import Order


@receiver(post_save, sender=Order)
def order_created(sender, instance: Order, created, **kwargs):
    
    if created:
        order = instance
        text = (
            f"*Новый заказ оформлен!* 🎉\n\n"
            f"*ID заказа*: `{order.id}`\n"
            f"*Стоимость*: `{order.grand_total} EUR`\n"
            f"*Страна*: `{escape_markdown(order.country)}`\n"
            f"*Город*: `{escape_markdown(order.city)}`\n\n"
            f"Вперёд за работу! 🚀"
        )
        
        chat_id = settings.TELEGRAM_CHAT_ID
        send_message_to_telegram(chat_id, text)