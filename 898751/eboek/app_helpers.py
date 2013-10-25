# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import re
from time import ctime

from pymongo import MongoClient
from flask.ext.login import UserMixin

import eboek

con = MongoClient('192.168.1.147', eboek.MONGODB_PORT)

dbh = con['eboek']

num_books = dbh.books.count()

books_per_page = 24

num_pages = num_books / float(books_per_page)

if max(num_pages, int(num_pages)) == num_pages:

    num_pages += 1

num_pages = int(num_pages)

nav_top = {}


for i, x in enumerate([a['author']['sort'][0].upper() for a in
                       dbh.books.find().sort('author.sort', 1)]):

    if not nav_top.get(x, False):

        nav_top[x] = 1 + (i / books_per_page)

        if x == 'Z':

            break


def get_page(page_num):

    query = dbh.books.find().sort('author.sort', 1).limit(books_per_page).skip(
        books_per_page * (page_num - 1))

    return build_page(query)


def build_page(query):

    books = []

    row = []

    for i, b in enumerate(query):

        if i % 6 == 0:

            books.append(row)

            row = []

        row.append(b)

    books.append(row)

    return books


def get_nav_bot(cur_page):

    has_next = lambda x, y: x + y if x + y < num_pages else None

    has_prev = lambda x, y: x - y if x - y > 0 else None

    pagination = {
        'cur_page': cur_page,
        'last_page': num_pages,
        'next_page': has_next(cur_page, 1),
        'prev_page': has_prev(cur_page, 1),
        'list': [
            has_prev(cur_page, 30),
            has_prev(cur_page, 15),
            has_prev(cur_page, 5),
            cur_page,
            has_next(cur_page, 5),
            has_next(cur_page, 15),
            has_next(cur_page, 30),
        ]
    }

    return pagination


def get_results(query):

    terms = [
        t.strip() for t in query.split() if len(t) > 2 and t not in
        eboek.STOPWORDS and re.search(r'[a-zA-Z]', t)
    ]

    q = dbh.books.find({'$and': [{'keywords': t.lower()} for t in terms]})

    return build_page(q)


def get_users():

    class User(UserMixin):

        def __init__(self, id, name, password):

            self.id = id
            self.name = name
            self.password = password

    users = {}

    for user in dbh.users.find():

        del user['_id']

        u = User(id=user['id'], name=user['name'],
                 password=user['password'])

        users[u.id] = u

    return users


def validate_and_log(ip, name, password):

    users = get_users()

    user = None

    for k, v in users.items():

        if v.name == name and v.password == password:

            user = users[k]

    if user:

        status = 'accepted'

        password = '*****'

    else:

        status = 'failed'

    with open(eboek.LOG_LOG, 'a') as log:

        log.write(
            "{time} [{ip}] authentication [{status}] for [{name}] with "
            "[{password}].\n".format(time=ctime(), ip=ip, status=status,
                                     name=name, password=password)
        )

    return user


def add_user(name, password):

    id = dbh.users.count() + 1

    dbh.users.insert({
        'name': name,
        'password': password,
        'id': id
    })

    return dbh.users.find_one({'id': id})
