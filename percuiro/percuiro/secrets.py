# -*- coding: utf-8 -*-
# dydrmntion@gmail.com

import json

SECRETS_FPATH = '/home/dbsr/.dev_secrets.json'

with open(SECRETS_FPATH) as f:
    secrets = json.load(f)


REALDEBRID_USER = secrets['REALDEBRID']['USER']
REALDEBRID_PASSWORD = secrets['REALDEBRID']['PASSWORD']
