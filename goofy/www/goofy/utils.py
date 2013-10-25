# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import logging
from datetime import datetime, timedelta
import cPickle
import urllib
import re

import requests

from goofy import constants

logger = logging.getLogger(__name__)


class ApiCache(object):

    def __init__(self, api_name):

        self.api_name = api_name

        self.pickle_fpath = '{0}_{1}'.format(constants.CACHE_PICKLE_FPATH,
                                             self.api_name)

        self.cache = self._load_pickle()

    def _load_pickle(self):

        if not os.path.isfile(self.pickle_fpath):

            return {}

        else:

            with open(self.pickle_fpath) as f:

                return cPickle.load(f)

    def _store_pickle(self):

        with open(self.pickle_fpath, 'w') as f:

            cPickle.dump(self.cache, f)

    def from_cache(self, request):

        try:
            # Response for this request in cache?
            expires, response = self.cache[request.url]

        except KeyError:
            # No.
            pass

        else:

            if expires < datetime.now():
                # Response has expired, purge it from cache
                del self.cache[request.url]

            else:

                return response

    def to_cache(self, response):

        if response.status_code == 200 and not hasattr(
                response, '_from_cache') or re.search('oauth|token'):

            if response.headers.get('expires'):

                _expires = datetime.strptime(response.headers['expires'],
                                             "%a, %d %b %Y %H:%M:%S %Z")

            else:

                _expires = datetime.now() + timedelta(days=1)

            self.cache[response.url] = (_expires, response._content)

            self._store_pickle()

            return response

#
#class DeezerOauth(object):
#
#    app_id = constants.DEEZER_APP_ID
#
#    url = 'https://connect.deezer.com/oauth/'
#
#    redirect_url = 'http://www.moscownights.nl/deezer_oauth/'
#
#    def get_oauth_url(self):
#
#        return self.url + 'auth.php?' + urllib.urlencode({
#            'redirect_uri': self.redirect_url,
#            'app_id': self.app_id,
#            'perms': 'manage_library'
#        })
#
#    def request_token(self, code):
#
#        logger.info('Initiating token request with code: {0!r}.'.format(code))
#
#        params = {
#            'code': code,
#            'app_id': self.app_id,
#            'secret': constants.DEEZER_SECRET
#        }
#
#        req = requests.get(self.url + 'access_token.php?', params=params)
#
#        try:
#
#            self.access_token = req.content.split('&')[0].split('=')[1]
#
#        except IndexError:
#
#            self.access_token = False
