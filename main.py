import asyncio
from binance import AsyncClient, BinanceSocketManager
from models import WsResponse
import requests
import time
from datetime import datetime
from telegram.ext import Updater, CommandHandler
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from config_manager import ConfigManager
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "5173401188:AAEOtTrM2Sqkx7XQFnCX5HmXfB510h-oPLE"

def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=context.error)

def chat_id(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat: {update.effective_chat.id}")

def parse_markdown(message):
    return message.replace('-','\-') \
                    .replace('_', '\_') \
                    .replace('|', '\|') \
                    .replace('*', '\*') \
                    .replace('.', '\.')


async def binance_listen(api_key, api_secret, chat_ids):
    binance = await AsyncClient.create(api_key, api_secret)
    bsm = BinanceSocketManager(binance)
    async with bsm.futures_user_socket() as ms:
        while True:
            msg = await ms.recv()
            ws = WsResponse(msg)
            send_telegram_message(str(ws), chat_ids)
    await binance.close_connection()


if __name__ == "__main__":
    cm = ConfigManager('config.json')
    configs = cm.get_configs()

    TOKEN = configs['tg_token']
    # start tg-bot
    # set ups
    updater = Updater(token=TOKEN, use_context=True)
    # commands
    chat_id_handler = CommandHandler("chat_id", chat_id)

    # init commands
    dispatcher = updater.dispatcher
    dispatcher.add_handler(chat_id_handler)
    dispatcher.add_error_handler(error)
    # start
    updater.start_polling()

    def send_telegram_message(message, chat_ids=[]):
        for chat_id in chat_ids:
            try:
                # updater.bot.send_message(chat_id=chat_id, text=parse_markdown(message), parse_mode='MarkdownV2')
                updater.bot.send_message(chat_id=chat_id, text=message)
            except Exception as e:
                print(e)
                continue

    for exchange in configs['exchanges']:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            print(f'run {exchange["name"]}')
            asyncio.run(binance_listen(exchange['key'], exchange['secret'], exchange['chat_ids']))
        except KeyboardInterrupt:
            pass


