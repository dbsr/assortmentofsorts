# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import re
from random import randint

from bson.objectid import ObjectId

from eboek import config, db, common, auth


class Helper(object):

    books_per_page = config.BOOKS_PER_PAGE

    def __init__(self, query, user, current_page=1):

        self.user = user

        self.current_page = int(current_page)

        self.num_books = self._get_num_books()

        if self.num_books == 0:

            return

        self.num_pages = (self.num_books / self.books_per_page) + 1

        self.pagination = self._build_pagination()

        self.books = self._build_page(query)

    def _build_page(self, query):

        books = []

        row = []

        for i, b in enumerate(query):

            if b['_id'] in self.user.booklist:

                b['in_booklist'] = True

            if i % 6 == 0:

                books.append(row)

                row = []

            row.append(b)

        books.append(row)

        return books

    def _get_num_books(self):

        return

    def _build_pagination(self):

        has_next = lambda x, y: x + y if x + y < self.num_pages else None

        has_prev = lambda x, y: x - y if x - y > 0 else None

        return {
            'cur_page': self.current_page,
            'last_page': self.num_pages,
            'next_page': has_next(self.current_page, 1),
            'prev_page': has_prev(self.current_page, 1),
            'list': [
                has_prev(self.current_page, 30),
                has_prev(self.current_page, 15),
                has_prev(self.current_page, 5),
                self.current_page,
                has_next(self.current_page, 5),
                has_next(self.current_page, 15),
                has_next(self.current_page, 30),
            ]
        }


class BrowseHelper(Helper):

    def __init__(self, user, current_page=1):

        with db.Handler() as dbh:

            query = dbh.books.find().sort('author.sort', 1).limit(
                self.books_per_page).skip(self.books_per_page *
                                          (current_page - 1))

        Helper.__init__(self, query, user, current_page)

    def _get_num_books(self):

        with db.Handler() as dbh:

            return dbh.books.count()


class SearchHelper(Helper):

    def __init__(self, search_terms, user, current_page=1):

        self.search_terms = search_terms

        terms = [t.strip().lower() for t in search_terms.split() if len(t) > 2
                 and t.lower() not in common.STOPWORDS
                 and re.search(r'[a-zA-Z]', t)]

        q = db.build_query('and', {'keywords': terms})

        with db.Handler() as dbh:

            self.query = dbh.books.find(q).sort('author.sort', 1)

        Helper.__init__(self, self.query, user, current_page)

    def _get_num_books(self):

        num_books = self.query.count()

        self.books_per_page = num_books

        return num_books


class BookListHelper(Helper):

    def __init__(self, user, current_page=1):

        self.user = user

        q = db.build_query('or', {'_id': self.user.booklist})

        with db.Handler() as dbh:

            self.query = dbh.books.find(q).sort('author.sort', 1)

        Helper.__init__(self, self.query, user, current_page)

        self.user.email_encrypted = self._get_enc_email()

    def _get_enc_email(self):

        mail = self.user.mail

        n = range(0, len(mail) - 1)

        k = [n.pop(randint(0, len(n) - 1)) for i in range(len(mail) / 2)]

        enc = ' '.join(map(lambda x: x if mail.index(x) in k else '_', mail))

        encoded = [
            enc[:(mail.index('@') * 2) - 1],
            enc[(mail.index('@') * 2) + 1:(mail.index('.') * 2) - 1],
            enc[(mail.index('.') * 2) + 1:]
        ]

        return encoded

    def _get_num_books(self):

        self.books_per_page = len(self.user.booklist)

        return len(self.user.booklist)


class ModalBookListHelper(object):

    def __init__(self, user_id):

        self.user = auth.get_user(user_id)

        self.books = self._get_booklist_books()

    def _get_booklist_books(self):

        if self.user.booklist:

            q = db.build_query('or', {'_id': self.user.booklist})

            with db.Handler() as dbh:

                return list(dbh.books.find(q))

        else:

            return []

    def set_modal(self, book_id):

        _id = ObjectId(book_id)

        self.modal = {}

        with db.Handler() as dbh:

            self.modal['book'] = dbh.books.find_one({'_id': _id})

        if _id in self.user.booklist:

            self.modal['label'] = 'alert alert-error'

            self.modal['txt_action'] = ('Het volgende boek uit je boekenlijst'
                                        ' verwijderen?')

            self.modal['form_action'] = 'remove=' + book_id

            self.modal['button_value'] = 'Verwijderen'

        else:

            self.modal['label'] = 'alert alert-success'

            self.modal['txt_action'] = ('Het volgende boek toevoegen aan je'
                                        ' boekenlijst?')

            self.modal['form_action'] = 'add=' + book_id

            self.modal['button_value'] = 'Toevoegen'

    def remove(self, book_id):

        if book_id == 'all':

            self.user.booklist = []

        else:

            self.user.booklist.remove(ObjectId(book_id))

        db.update_user(self.user.to_dict())

    def append(self, book_id):

        self.user.booklist.append(ObjectId(book_id))

        db.update_user(self.user.to_dict())
