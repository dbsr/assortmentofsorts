# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
from datetime import datetime
import logging
import re
from zipfile import ZipFile, ZIP_DEFLATED

import sqlite3 as sqlite
from pymongo import Connection
from bson.objectid import ObjectId
import Image

import eboek

logger = logging.getLogger(__name__)


def main(query=[]):

    mongo_con = Connection(host=eboek.MONGODB_HOST, port=27017)

    dbh = mongo_con['eboek']

    pre_count = dbh.books.count()

    for book in sqlite_get_books(query):

        doc = tuple_to_dict(book)

        dbh.books.update(
            {'author': doc['author'],
             'title': doc['title'],
             'meta.lang': doc['meta']['lang']
             }, doc, upsert=True)

    logger.info('Inserted {} books in the database.'.format(
        dbh.books.count() - pre_count))


def sqlite_get_books(query):

    db = sqlite.connect(eboek.CALIBRE_DATABASE)
    cur = db.cursor()

    sql = '''
        SELECT books.title, books.pubdate, books.path, books.has_cover,
               authors.name, authors.sort, books_languages_link.lang_code,
               data.format, data.uncompressed_size, data.name, series.name
            FROM books
              JOIN books_authors_link ON books_authors_link.book = books.id
              JOIN authors ON authors.id = books_authors_link.author
              JOIN books_languages_link ON books_languages_link.book = books.id
              JOIN data ON data.book = books.id
              JOIN series ON series.id = books.series_index '''

    make_q = lambda dct: dct.keys()[0] + ' = ' + str(dct.values()[0])

    sql += ' AND '.join(make_q(x) for x in query)

    cur.execute(sql)

    for b in cur.fetchall():

        yield b


def tuple_to_dict(sqlite_tuple):

    (TITLE, PUB_DATE, PATH, HAS_COVER, AUTHOR, AUTHOR_SORT, LANG, FORMAT, SIZE,
     DATA_NAME, SERIE) = range(11)

    to_datetime = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M') if s else s

    lang_code = ['EN', 'NL']

    _id = ObjectId()

    _path = (os.path.join(sqlite_tuple[PATH], sqlite_tuple[DATA_NAME]) +
             '.' + sqlite_tuple[FORMAT].lower())

    book = {
        '_id': _id,
        'author': {
            'name': sqlite_tuple[AUTHOR],
            'sort': sqlite_tuple[AUTHOR_SORT].lower()
        },
        'title': sqlite_tuple[TITLE],
        'meta': {
            'pub_date': to_datetime(sqlite_tuple[PUB_DATE][:-9]),
            'serie': sqlite_tuple[SERIE],
            'format': sqlite_tuple[FORMAT],
            'lang': lang_code[sqlite_tuple[LANG]],
            'description': get_description(_path)
        },
        'data': {
            'size': sqlite_tuple[SIZE],
        },
        'date_added': datetime.now(),
        'assets': {
            'thumb_uri': create_thumbnail(sqlite_tuple[HAS_COVER], _path, _id)
        }
    }

    book['keywords'] = get_keywords(book)
    zip_book(book, sqlite_tuple[PATH])

    return book


def create_thumbnail(has_cover, bpath, bid):

    if not has_cover:

        return 'nocover.jpg'

    cover_uri = os.path.join(eboek.BOOKS_DIR, os.path.dirname(bpath),
                             'cover.jpg')
    thumb_name = str(bid) + '.jpg'
    thumb_size = 200, 300

    try:

        img = Image.open(cover_uri)
        img.thumbnail(thumb_size)
        img.save(os.path.join(eboek.THUMBS, thumb_name), 'JPEG')

    except IOError as e:

        logger.error(e.strerror + cover_uri)

    else:

        return thumb_name


def get_description(bpath):

    metadata = os.path.join(eboek.BOOKS_DIR, os.path.dirname(bpath),
                            'metadata.opf')

    if os.path.isfile(metadata):

        with open(metadata) as f:

            description = re.search(r'<dc:description>(.*)</dc:description>',
                                    f.read())

            if description:

                description = re.sub(r'[^ ]*&[^ ]*', '', description.group(1))

                return re.sub(r'[ ]{2,}', ' ', description).strip()


def get_keywords(book):

    keywords = []

    for keyword in book['title'].split() + book['author']['name'].split():

        if (keyword.lower() not in eboek.STOPWORDS and len(keyword) > 2 and
                re.search(r'[a-zA-Z]', keyword)):

            keywords.append(keyword.lower())

    return keywords


def zip_book(book, bpath):

    with ZipFile(os.path.join(eboek.BOOKS_DIR,
                              str(book['_id']) + '.zip'), 'w') as zf:

        fpath = os.path.join(eboek.BOOKS_DIR, bpath)

        for f in [os.path.join(fpath, x) for x in os.listdir(fpath)]:

            zf.write(f, arcname=os.path.join(bpath, os.path.basename(f)),
                     compress_type=ZIP_DEFLATED)
