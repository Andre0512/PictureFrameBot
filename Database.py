#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sqlite3


class Get:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'database.db'))
        self.cur = self.con.cursor()

    def check_account(self, update):
        self.cur.execute("SELECT * FROM users WHERE user_id=" + str(update.message.from_user.id) + ";")
        l = len(self.cur.fetchall())
        if l == 0:
            return False
        return True

    def check_slideshow(self, slide_id):
        self.cur.execute(
            "SELECT ss.name, COUNT(p.id) FROM slideshows ss INNER JOIN pictures p on ss.id=p.slide_id WHERE p.slide_id=" + str(
                slide_id))
        name, number = [[item[0], item[1]] for item in self.cur.fetchall()][0]
        return [name, number]

    def get_pictures(self, slide_id):
        self.cur.execute(
            "SELECT p.name FROM  pictures p INNER JOIN slideshows ss  on ss.id=p.slide_id WHERE p.slide_id=" + str(
                slide_id))
        name = [item[0] for item in self.cur.fetchall()]
        return name

    def get_slides(self, user_id):
        self.cur.execute(
            "SELECT ss.name, ss.private, u.first_name, ss.id, (SELECT COUNT(id) FROM pictures WHERE slide_id = ss.id) "
            "FROM pictures p LEFT JOIN slideshows ss ON ss.id=p.slide_id LEFT JOIN users u ON u.user_id=ss.user_id WHERE "
            "ss.user_id=" + str(user_id) + " OR ss.private = 1 GROUP BY ss.id")
        slide_shows = [[item[0], item[1], item[2], item[3], item[4]] for item in self.cur.fetchall()]
        return slide_shows

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
        self.cur.execute("SELECT MAX(id) FROM slideshows;")
        max_id = [item[0] for item in self.cur.fetchall()][0]
        return max_id if max_id is not None else 0

    def insert_slideshow(self, user_id):
        max_id = self.__slideshow_max_id()
        name = "Slideshow " + str(max_id + 1)
        query = "INSERT INTO slideshows(user_id,name) VALUES (?, ?);"
        self.cur.execute(query, (user_id, name))
        self.con.commit()
        return [max_id, name]

    def insert_pictures(self, user_id, slide_id, name):
        query = "INSERT INTO pictures(user_id, slide_id, name) VALUES (?, ?, ?);"
        self.cur.execute(query, (user_id, slide_id, name))
        self.con.commit()

    def __del__(self):
        self.con.close()
