#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import json
import requests
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = os.environ.get('API_KEY')


def start(bot, update):
    update.message.reply_text('Привет, это криптовалютный бот!\nПолучить список команд: /help')

def help(bot, update):
    update.message.reply_text('Yobit.net:\n\n/trx_usd\n/bcc_usd\n/xem_usd\n/zec_isd\n/eth_usd\n\nBinance: /btc_usdt')


def binanceGetPair(pair, bot, update):
    binHeadUri = 'https://api.binance.com/api/v1/ticker/price?symbol='
    url = binHeadUri + pair
    pairData = requests.get(url)
    try:
        res_obj = json.loads(pairData.text)
        price = res_obj['price']
        update.message.reply_text(pair + ': ' + str(price))
    except ValueError:
        update.message.reply_text('something wrong')


def btc_usdt(bot, update):
    binanceGetPair('BTCUSDT', bot, update)



def yobitGetPair(pair, bot, update):
    yobitHeadUri = 'https://yobit.net/api/2/'
    yobitTailUrl = '/ticker'
    url = yobitHeadUri + pair + yobitTailUrl
    pairData = requests.get(url)
    try:
        res_obj = json.loads(pairData.text)
        buy = res_obj['ticker']['buy']
        sell = res_obj['ticker']['sell']
        update.message.reply_text(pair + ': ' + 'buy: ' + str(buy) + ' sell: ' + str(sell))
    except ValueError:
        update.message.reply_text('something wrong')



def trx_usd(bot, update):
    yobitGetPair('trx_usd', bot, update)

def bcc_usd(bot, update):
    yobitGetPair('bcc_usd', bot, update)

def xem_usd(bot, update):
    yobitGetPair('xem_usd', bot, update)

def zec_usd(bot, update):
    yobitGetPair('zec_usd', bot, update)

def eth_usd(bot, update):
    yobitGetPair('eth_usd', bot, update)




def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("trx_usd", trx_usd))


        # on noncommand i.e message - echo the message on Telegram
        #dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()