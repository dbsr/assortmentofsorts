# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from flask.ext.login import LoginManager, login_user

from db import Handler
from models import User
import config

# Initiate the login manager
login_manager = LoginManager()

LoginManager.login_view = 'login'


def load_users():
    with Handler('eboek') as dbh:
        users = dict(
            (int(user['id']), User(user)) for user in dbh.users.find())

    return users


@login_manager.user_loader
def load_user(userid):
    users = load_users()
    return users[int(userid)]


def get_user(userid):
    users = load_users()
    return users[int(userid)]


def validate_login(username, password, remote_addr):

    for k, user in load_users().items():

        if user.name == username and user.password == password:

            print user

            login_user(user)

            status = True

        else:

            status = False

    with open(config.AUTH_LOG, 'a') as log:

        line = '[{}] [login: {}] [user: {}] [password: {}]\n'.format(
            remote_addr, repr(status), username, password)

        log.write(line)

    return status
