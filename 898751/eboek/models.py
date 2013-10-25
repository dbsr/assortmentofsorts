# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from flask.ext.login import UserMixin


class User(UserMixin):

    def __init__(self, user_dict):

        self.id = user_dict['id']
        self.name = user_dict['name']
        self.password = user_dict['password']
        self.mail = user_dict['mail']
        self.booklist = user_dict['booklist']
#    <p><h2>De boeken worden naar: {{ helper.user.email_encrypted[0] }} @ {{ helper.user.email_encrypted[1] }} . {{ helper.user.email_encrypted[2] }} verstuurd.</h2></p>

    def to_dict(self):

        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'mail': self.mail,
            'booklist': self.booklist
        }
