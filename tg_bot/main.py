import logging

import asyncio
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)
logger = logging.getLogger("telegramBot")


async def send_message_to_telegram(chat_id, text):
    try:
        await bot.send_message(chat_id, text, parse_mode="Markdown")
    except TelegramError as e:
        logger.error(msg=f"Error while sending message: {e}")

def send_message_to_telegram(chat_id, text):
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(send_message_to_telegram(chat_id, text))
