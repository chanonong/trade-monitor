import asyncio
import threading
from binance import AsyncClient, BinanceSocketManager
from models import WsResponse
import requests
from telegram.ext import Updater, CommandHandler
import logging
from config_manager import ConfigManager
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.error)

def chat_id(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat: {update.effective_chat.id}")

def parse_markdown(message):
    return message.replace('-', '\-') \
                    .replace('_', '\_') \
                    .replace('|', '\|') \
                    .replace('*', '\*') \
                    .replace('.', '\.')

def send_telegram_message(message, chat_ids=[]):
    for chat_id in chat_ids:
        try:
            updater.bot.send_message(chat_id=chat_id, text=parse_markdown(message), parse_mode='MarkdownV2')
        except Exception as e:
            logging.error(f"Error sending message to chat ID {chat_id}: {e}")

async def binance_listen(api_key, api_secret, chat_ids):
    binance = await AsyncClient.create(api_key, api_secret)
    bsm = BinanceSocketManager(binance)
    async with bsm.futures_user_socket() as ms:
        while True:
            msg = await ms.recv()
            ws = WsResponse(msg)
            send_telegram_message(str(ws), chat_ids)
    await binance.close_connection()

def start_binance_listener(api_key, api_secret, chat_ids):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(binance_listen(api_key, api_secret, chat_ids))

if __name__ == "__main__":
    cm = ConfigManager('config.json')
    configs = cm.get_configs()

    TOKEN = configs['tg_token']
    
    # Set up the Telegram bot
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    chat_id_handler = CommandHandler("chat_id", chat_id)
    dispatcher.add_handler(chat_id_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()

    # Start Binance listeners in separate threads
    threads = []
    for exchange in configs['exchanges']:
        thread = threading.Thread(target=start_binance_listener, args=(exchange['key'], exchange['secret'], exchange['chat_ids']))
        thread.start()
        threads.append(thread)

    # Wait for threads to finish (if needed)
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        logging.info("Stopping listeners.")
