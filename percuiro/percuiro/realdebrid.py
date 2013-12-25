# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import requests

from memoize import MemoizeDecorator, TTL_ONE_HOUR, TTL_TEN_MINUTES
import common
from secrets import REALDEBRID_USER, REALDEBRID_PASSWORD

REALDEBRID_URL = 'https://real-debrid.com/ajax'

realdebrid_session = requests.Session()


@MemoizeDecorator(common.DATA_DIR + '/realdebrid.json', TTL_ONE_HOUR)
def get_auth_cookies():
    realdebrid_session.get(
        '{}/login.php'.format(REALDEBRID_URL),
        params={
            'user': REALDEBRID_USER,
            'pass': REALDEBRID_PASSWORD
        })
    # Because the memoize dec uses JSON to store data we need to convert
    # the cookiejar to a dictionary
    return requests.utils.dict_from_cookiejar(realdebrid_session.cookies)


@MemoizeDecorator(common.DATA_DIR + 'unrestrict.json', TTL_TEN_MINUTES)
def unrestrict(link):
    if 'auth' not in realdebrid_session.cookies:
        realdebrid_session.cookies = requests.utils.cookiejar_from_dict(
            get_auth_cookies())
    req = realdebrid_session.get(
        '{}/unrestrict.php'.format(REALDEBRID_URL),
        params={
            'link': link
        })
    resp = req.json()
    if resp.get('error'):
        print resp
    else:
        return resp['main_link']
