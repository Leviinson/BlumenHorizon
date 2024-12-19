import asyncio
import logging

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message_to_telegram_async(chat_id, text):
    logger = logging.getLogger("telegramBot")

    try:
        await bot.send_message(chat_id, text, parse_mode="Markdown")
    except TelegramError as e:
        logger.error(msg=f"Error while sending message: {e}")


def send_message_to_telegram(chat_id, text):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(send_message_to_telegram_async(chat_id, text))
        else:
            asyncio.run(send_message_to_telegram_async(chat_id, text))
    except Exception as e:
        logging.error(f"Error in send_message_to_telegram: {e}")
