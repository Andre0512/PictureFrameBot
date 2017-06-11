#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sqlite3
import yaml
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import datetime
import Browser
import Database


def custom_str_constructor(loader, node):
    return loader.construct_scalar(node).encode('utf-8')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def createDB():
    fd = open(os.path.join(os.path.dirname(__file__), 'Create.sql'), 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database.db'))
    c = conn.cursor()
    for command in sqlCommands:
        c.execute(command)
    conn.close()


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
    db_out = Database.Set()
    db_in = Database.Get()
    if not db_in.check_account(update):
        db_out.insert_account(update)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def slideshow(bot, update):
    Browser.main()
    update.message.reply_text(strings['start_show'] + ' 😁')


def receive_photo(bot, update):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    photo_id = update.message.photo[-1].file_id
    photo_file = bot.getFile(photo_id)
    photo_file.download(os.path.join(os.path.dirname(__file__), "pictures/" + timestamp + ".jpg"))
    update.message.reply_text(strings["received"] + ' 🙂')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    yaml.add_constructor(u'tag:yaml.org,2002:str', custom_str_constructor)
    cfg = get_yml("./config.yml")
    global strings
    strings = get_yml("./language_strings/strings.yml")

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'database.db')):
        print(strings['create_db'])
        createDB()

    updater = Updater(cfg['telegram']['token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("exec", slideshow))

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, receive_photo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
