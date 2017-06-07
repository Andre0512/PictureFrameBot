#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

import yaml
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def get_yml(file):
    result = {}
    with open(os.path.join(os.path.dirname(__file__), file), 'rb') as ymlfile:
        values = yaml.load(ymlfile)
        for k, v in values.items():
            result[k.decode('utf-8')] = dict_byte_to_str(v)
    return result


def dict_byte_to_str(v):
    result = {}
    if hasattr(v, 'items'):
        for key, value in v.items():
            if isinstance(value, bytes):
                value = value.decode('utf-8')
                value = str.replace(value, "\\n", "\n")
            result[key.decode('utf-8')] = value
    else:
        result = v.decode('utf-8')
        result = str.replace(result, "\\n", "\n")
    return result


def start(bot, update):
    update.message.reply_text('Hi!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def receive_photo(bot, update):
    photo_id = update.message.photo[-1].file_id
    photo_file = bot.getFile(photo_id)
    photo_file.download()


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    cfg = get_yml("./config.yml")
    strings = get_yml("language_strings/strings.yml")

    updater = Updater(cfg['telegram']['token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, receive_photo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
