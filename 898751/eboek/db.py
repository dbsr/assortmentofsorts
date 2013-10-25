# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from pymongo import MongoClient

from config import DB_HOST


class Handler(object):

    def __init__(self, db='eboek'):

        self.con = MongoClient(host=DB_HOST)

        self.dbh = self.con[db]

    def __enter__(self):

        return self.dbh

    def __exit__(self, *args):

        self.con.close()


def build_query(operator, kv_dict):

    conditionals = []

    for k, v in kv_dict.items():

        if not isinstance(v, list):

            v = [v]

        conditionals.extend([{k: _v} for _v in v])

    return {'$' + operator: conditionals}


def update_user(user):

    with Handler() as dbh:

        dbh.users.update({'id': user['id']}, user)
