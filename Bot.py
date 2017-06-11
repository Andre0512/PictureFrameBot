#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sqlite3
import sys
import yaml
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
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
    reply_markup = ReplyKeyboardMarkup([["➕ " + strings['create_slideshow']]])
    update.message.reply_text('Hi ' + update.message.from_user.first_name + " ✌🏻", reply_markup=reply_markup)
    db_out = Database.Set()
    db_in = Database.Get()
    if not db_in.check_account(update):
        db_out.insert_account(update)


def echo(bot, update, chat_data):
    if update.message.text == "➕ " + strings['create_slideshow']:
        name = create_slideshow(update, chat_data)
        reply_text = strings['creating'] + " 😊"
        reply_text = reply_text.replace("@name",name)
        update.message.reply_text(reply_text)
    else:
        update.message.reply_text(update.message.text)


def create_slideshow(update, chat_data):
    db = Database.Set()
    user_id = update.message.from_user.id
    chat_data['slide_id'], slide_name = db.insert_slideshow(user_id)
    return slide_name


def slideshow(bot, update):
    Browser.main()
    update.message.reply_text(strings['start_show'] + ' 😁')


def receive_photo(bot, update, chat_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    photo_id = update.message.photo[-1].file_id
    photo_file = bot.getFile(photo_id)
    photo_file.download(os.path.join(os.path.dirname(__file__), "pictures/" + timestamp + ".jpg"))
    keyboard = [[InlineKeyboardButton(strings['complete'] + " ✔", callback_data='complete')]]
    update.message.reply_text(strings["received"] + ' 🙂', reply_markup=InlineKeyboardMarkup(keyboard))
    db = Database.Set()
    db.insert_pictures(update.message.from_user.id, chat_data['slide_id'], timestamp + '.jpg')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def button(bot, update, chat_data):
    update.callback_query.answer()
    if update.callback_query.data == "complete":
        update.callback_query.message.edit_text("x")
        del chat_data

def main():
    yaml.add_constructor(u'tag:yaml.org,2002:str', custom_str_constructor)
    cfg = get_yml("./config.yml")
    global strings
    strings = get_yml("./language_strings/strings.yml")

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'database.db')):
        print(strings['create_db'])
        createDB()

    if sys.argv[1:] and sys.argv[1:][0] == 'ssh':
        os.environ["DISPLAY"] = ":0"

    updater = Updater(cfg['telegram']['token'])

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("exec", slideshow))

    dp.add_handler(MessageHandler(Filters.text, echo, pass_chat_data=True))
    dp.add_handler(MessageHandler(Filters.photo, receive_photo, pass_chat_data=True))
    dp.add_handler(CallbackQueryHandler(button, pass_chat_data=True))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
