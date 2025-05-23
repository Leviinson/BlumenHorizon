import asyncio
import logging
import os

from django.conf import settings
from telegram import Bot

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message_to_telegram_async(chat_id, text):
    try:
        await bot.send_message(chat_id, text, parse_mode="Markdown")
    except Exception as e:
        logger = logging.getLogger("telegramBot")
        logger.error(
            f"Error sending message to chat_id {chat_id}: {e}", stack_info=True
        )


async def send_messages_to_multiple_chat_ids(chat_ids, text):
    tasks = [send_message_to_telegram_async(chat_id, text) for chat_id in chat_ids]
    await asyncio.gather(*tasks)


def send_message_to_telegram(text: str):
    """
    Sends a message to multiple chat_ids using asyncio.
    :param text: The message text to send.
    :param chat_ids: A list of chat IDs to send the message to.
    """
    logger = logging.getLogger("telegramBot")
    telegram_chat_ids = os.getenv("TELEGRAM_CHAT_IDS", "")
    chat_ids_list = telegram_chat_ids.split(",") if telegram_chat_ids else []
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            asyncio.ensure_future(
                send_messages_to_multiple_chat_ids(chat_ids_list, text)
            )
        else:
            loop.run_until_complete(
                send_messages_to_multiple_chat_ids(chat_ids_list, text)
            )
    except Exception as e:
        logger.error(f"Error in send_message_to_telegram: {e}")
