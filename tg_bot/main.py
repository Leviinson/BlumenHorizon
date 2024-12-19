import asyncio
import logging

from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message_to_telegram_async(chat_id, text):
    await bot.send_message(chat_id, text, parse_mode="Markdown")


def send_message_to_telegram(text: str, chat_id=settings.TELEGRAM_CHAT_ID):
    logger = logging.getLogger("telegramBot")

    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            asyncio.ensure_future(send_message_to_telegram_async(chat_id, text))
        else:
            loop.run_until_complete(send_message_to_telegram_async(chat_id, text))
    except Exception as e:
        logger.error(f"Error in send_message_to_telegram: {e}")
