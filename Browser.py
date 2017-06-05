#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import webbrowser
import subprocess
import os


def insert_images(html):
    image_list = []
    link_list = ["https://ifsstech.files.wordpress.com/2008/10/169.jpg",
                 "https://designshack.net/wp-content/uploads/16-9.jpg",
                 "https://upload.wikimedia.org/wikipedia/commons/7/7c/Aspect_ratio_16_9_example.jpg"]
    delay_time = 1000
    for image in link_list:
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
    fscreen = "./Fullscreen"
    first = False
    if not os.path.isfile(fscreen):
        first = True
        os.environ["DISPLAY"] = ":0"

    webbrowser.register('midori', None, webbrowser.BackgroundBrowser('/usr/bin/midori'))
    browser = webbrowser.get('midori')
    browser.open(html_file)
    if first:
        subprocess.call('xte "key F11" -x:0', shell=True)
        open(fscreen, 'a').close()


def main():
    html_in_file = 'std_form.html'
    html_out_file = 'test.html'

    html = read_file(html_in_file)
    html = insert_images(html)
    write_file(html, html_out_file)

    if not os.name == 'nt':
        open_linux(html_out_file)
    else:
        webbrowser.get('windows-default').open(html_out_file)


if __name__ == '__main__':
    main()
