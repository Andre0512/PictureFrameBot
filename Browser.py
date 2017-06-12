#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webbrowser
import os
import Database


def read_images():
    folder = os.path.join(os.path.dirname(__file__), "pictures/")
    folder_list = os.listdir(folder)
    folder_list = [folder + file for file in folder_list]
    return folder_list


def insert_images(html, slide_id):
    db = Database.Get()
    image_list = []
    image_db_list = db.get_pictures(slide_id)
    image_db_list = ['./pictures/' + image for image in image_db_list]
    #link_list = read_images()
    delay_time = 1000
    for image in image_db_list:
        image_list.append('<img class ="mySlides" src="' + image + '" style="width:100%">')

    html = html.replace("@IMAGES", '\n'.join(image_list))
    html = html.replace("@DELAY", str(delay_time))
    return html


def write_file(html, html_out_file):
    out_file = open(html_out_file, 'w')
    out_file.write(html)
    out_file.close()


def read_file(html_in_file):
    in_file = open(html_in_file, 'r', encoding='utf-8')
    html = in_file.read()
    return html


def open_linux(html_file):
    webbrowser.register('midori', None, webbrowser.BackgroundBrowser('/usr/bin/midori'))
    browser = webbrowser.get('midori')
    browser.open(html_file)


def main(slide_id=0):
    html_in_file = os.path.join(os.path.dirname(__file__), 'std_form.html')
    html_out_file = os.path.join(os.path.dirname(__file__), 'slideshow.html')

    html = read_file(html_in_file)
    html = insert_images(html, slide_id)
    write_file(html, html_out_file)

    if not os.name == 'nt':
        open_linux(html_out_file)
    else:
        webbrowser.get('windows-default').open(html_out_file)


if __name__ == '__main__':
    main()
