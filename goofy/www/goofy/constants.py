# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os

DEEZER_OAUTH = {
    'client_id': '112701',
    'client_secret': 'HUSH',
    'redirect_uri': 'http://www.moscownights.nl/oauth',
    'authorization_uri': 'https://connect.deezer.com/oauth/auth.php',
    'token_uri': 'https://connect.deezer.com/oauth/access_token.php'
}

USER_AGENT = 'GOOFY/0.1 python/requests'

CACHE_PICKLE_FPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  '..', 'data/cache_pickle')
