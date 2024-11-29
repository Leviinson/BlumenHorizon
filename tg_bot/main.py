import logging

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)
logger = logging.getLogger("telegramBot")


def send_message_to_telegram(chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except TelegramError as e:
        logger.log(level="ERROR", msg=f"Error while sending message: {e}")
