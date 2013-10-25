# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os

_here = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# app settings
DB_HOST = '192.168.1.147'
BOOKS_PER_PAGE = 36

# uwsgi/production
AUTH_LOG = os.path.join(_here, '../log/auth.log')
APP_LOG = os.path.join(_here, '../log/app.log')
SECRET_KEY = '#\xffj\xb9\x80\xb5\x92$~\x84Z\xe4\xfb[\xba\xb4\xc1\rp~S\x83t\xe6l'
