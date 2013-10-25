# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
from zipfile import ZipFile
from StringIO import StringIO
import re

import Image
from bson.objectid import ObjectId

import eboek
from eboek.app_helpers import dbh

BOOKDIR = '/home/dbsr/.config/Dropbox/Apps/eboek (1)'



def process_book(book_zip):

    _id = ObjectId(os.path.basename(book_zip).strip('.zip'))

    with ZipFile(book_zip) as zf:

        nl = zf.namelist()

        l_sort = lambda x: x[-1].lower() + ',' + ' '.join(x[:-1]).lower()

        name = nl[0].split('/')[0]

        sort = l_sort(name.split())

        title = nl[0].split('/')[1].split(' (')[0]

        cover = [f for f in nl if os.path.basename(f) == 'cover.jpg']

        if cover:
            has_cover = 1
            data = StringIO(zf.read(cover[0]))
            thumb_name = str(_id) + '.jpg'
            thumb_size = 200, 300

            try:

                img = Image.open(data)
                img.thumbnail(thumb_size)
                img.save(os.path.join('/home/dbsr/src/eboek/thumbs',
                                      thumb_name), 'JPEG')

            except IOError:

                print 'NAJ'

        else:

            has_cover = 0

    keywords = {}

    for keyword in title.split() + name.split():

        if (keyword.lower() not in eboek.STOPWORDS and len(keyword) > 2 and
                re.search(r'[a-zA-Z]', keyword)):

            keywords[keyword.lower()] = 1

    keywords = keywords.keys()

    return {
        '_id': _id,
        'title': title,
        'author': {
            'name': name,
            'sort': sort},
        'keywords': keywords,
        'has_cover': has_cover
    }


def do():

    for i, b in enumerate(
        [os.path.join(BOOKDIR, f) for f in os.listdir(BOOKDIR) if f[-4:] == '.zip']):

        print i

        dbh.books.insert(process_book(b))
