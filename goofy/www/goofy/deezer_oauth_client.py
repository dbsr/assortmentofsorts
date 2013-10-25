# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

from datetime import datetime, timedelta
import re
import logging

from pyoauth2 import utils, client


logger = logging.getLogger(__name__)


class DeezerClient(client.Client):

        def __init__(self, perms, *args, **kwargs):

            self.perms = perms

            client.Client.__init__(self, *args, **kwargs)

        @property
        def default_grant_type(self):

            return 'basic_access'

        def get_authorization_code_uri(self, **params):

            params.update({
                'app_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'perms': self.perms

            })

            return utils.build_url(self.authorization_uri, params)

        def get_token(self, code, **params):

            logger.info('Initiating token request using code: {!r}.'.format(
                code))

            params['code'] = code

            params.update({

                'code': code,
                'secret': self.client_secret,
                'app_id': self.client_id
            })

            resp = self.http_post(self.token_uri, params).content

            try:

                token, expires = re.findall(r'[^=]+=([^&]+)[^=]+=(.*)\n',
                                            resp)[0]

            except (TypeError, IndexError):

                logger.error('Token request failed, response: {!r}.'.format(
                    resp))

            else:

                return token, datetime.now() + timedelta(seconds=int(expires))
