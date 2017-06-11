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


class Get:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database.db'))
        self.cur = self.con.cursor()

    def check_account(self, update):
        self.con.execute("SELECT * FROM users WHERE user_id LIKE " + str(update.message.from_user.id) + ";")
        l = len(self.cur.fetchall())
        if l == 0:
            return False
        return True

    def __del__(self):
        self.con.close()


class Set:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database.db'))
        self.cur = self.con.cursor()

    def insert_account(self, update):
        user = update.message.from_user
        query = "INSERT INTO users(user_id,first_name,last_name,username,language) VALUES (?, ?, ?, ?, ?);"
        self.cur.execute(query, (user.id, user.first_name, user.last_name, user.username, user.language_code))
        self.con.commit()

    def __slideshow_max_id(self):
        self.con.execute("SELECT MAX(.rowid) FROM slideshows;")
        max_id = [item[0] for item in self.cur.fetchall()]
        return max_id[0]

    def insert_slideshow(self, user_id):
        name = "Slideshow" + self.__slideshow_max_id()
        query = "INSERT INTO slideshows(user_id,name) VALUES (?, ?);"
        self.cur.execute(query, (user_id, name))
        self.con.commit()

    def __del__(self):
        self.con.close()
